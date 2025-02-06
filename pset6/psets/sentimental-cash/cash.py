from cs50 import get_float


def main():
    # get the input from the user
    change = get_float("Change owed: ")
    while (change <= 0):
        change = get_float("Change owed: ")

    # change dollar value to cents value
    change = change * 100

    # calculate the quarters needed
    quarters = calculate_quarters(change)
    change = change - 25 * quarters

    # calculate the dimes
    dimes = calculate_dimes(change)
    change = change - 10 * dimes

    # calculate the nickels
    nickels = calculate_nickels(change)
    change = change - 5 * nickels

    # calculate total coins needed
    coins = int(change + quarters + dimes + nickels)
    print(f"{coins}")


def calculate_quarters(change):
    return int(change / 25)


def calculate_dimes(change):
    return int(change/10)


def calculate_nickels(change):
    return int(change/5)


def calculate_pennies(change):
    return change


if __name__ == "__main__":
    main()
    