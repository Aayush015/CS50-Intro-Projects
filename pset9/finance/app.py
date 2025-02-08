import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Create history table if not already exists
db.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            shares INTEGER NOT NULL,
            price NUMERIC NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
""")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    holdings = db.execute("""
        SELECT symbol, SUM(shares) as total_shares
        FROM history
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, session["user_id"])
    total_portfolio_value = user_cash
    for holding in holdings:
        quote_result = lookup(holding["symbol"])
        holding["name"] = quote_result["symbol"]
        holding["price"] = quote_result["price"]
        holding["total_value"] = holding["total_shares"] * quote_result["price"]
        total_portfolio_value += holding["total_value"]
    return render_template("index.html", user_cash=user_cash, holdings=holdings, total_portfolio_value=total_portfolio_value)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide stock symbol", 400)
        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("number of shares must be a positive integer", 400)
        if not shares:
            return apology("must provide number of shares", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("Invalid symbol", 400)
        cost = shares * quote["price"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        if cost > user_cash:
            return apology("Insufficient fund", 400)

        # update the user cash now
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])
        # keep transaction history
        db.execute("INSERT INTO history(user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], quote["symbol"], shares, quote["price"])
        flash(f"Successfully bought {shares} shares worth ${cost:.2f}!")
        return redirect("/")
    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transc_history = db.execute("""
        SELECT symbol, shares, price, timestamp
        FROM history
        WHERE user_id = ?
    """, session["user_id"])
    for transaction in transc_history:
        quote = lookup(transaction["symbol"])
        transaction["name"] = quote["symbol"]
    return render_template("history.html", transc_history = transc_history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Ensure Symbol is exists
        query = lookup(request.form.get("symbol"))
        if not (query):
            return apology("INVALID SYMBOL")
        else:
            return render_template("quoted.html", query=query)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Must Give Username")

        if not password:
            return apology("Must Give Password")

        if not confirmation:
            return apology("Must Give Confirmation")

        if password != confirmation:
            return apology("Password Do Not Match", 400)

        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            session["user_id"] = new_user
            return redirect("/", 200)
        except:
            return apology("Username already exists")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide stock symbol", 400)
        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("number of shares must be a positive integer", 400)
        if not shares:
            return apology("must provide number of shares", 400)

        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("stock symbol not found", 400)
        holdings = db.execute("""
            SELECT SUM(shares) as total_shares
            FROM history
            WHERE user_id = ? AND symbol = ?
            GROUP BY symbol
        """, session["user_id"], quote["symbol"])
        if not holdings or holdings[0]["total_shares"] < shares:
            return apology("insufficient shares to sell", 400)
        sale_value = shares * quote["price"]
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sale_value, session["user_id"])
        db.execute("INSERT INTO history (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                    session["user_id"], quote["symbol"], -shares, quote["price"])
        flash(f"Successfully sold {shares} shares worth ${sale_value:.2f}!")
        return redirect("/")
    else:
        symbols = db.execute("""
            SELECT symbol
            FROM history
            WHERE user_id = ?
            GROUP BY symbol
            HAVING SUM(shares) > 0
        """, session["user_id"])
        return render_template("sell.html", holdings=symbols)


# Personal touch of letting user add more cash if they need
@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
            if amount <= 0:
                raise ValueError
        except ValueError:
            return apology("amount must be a positive number", 400)

        # Update the user's cash balance
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, session["user_id"])
        flash(f"Successfully added ${amount:.2f} to your account!")
        return redirect("/")
    else:
        return render_template("deposit.html")
