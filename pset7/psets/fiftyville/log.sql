-- Keep a log of any SQL queries you execute as you solve the mystery.
-- main description
SELECT description
FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28;

-- description from Humprehy Street
SELECT description
FROM crime_scene_reports
WHERE month = 7 AND day = 28
AND street = "Humphrey Street";

-- money withdrawn from atm by diff people
SELECT name
FROM people
WHERE id = (
    SELECT person_id
    FROM bank_accounts
    JOIN atm_transactions atm
    WHERE month = 7 AND day = 28
    AND year = 2021 AND atm_location = 'Leggett Street'
);

-- Get the id of New York City
SELECT destination_airport_id, full_name, city
FROM flights
JOIN airports ON airports.id = flights.id
WHERE month = 7 AND day = 28
AND year = 2021;

-- license plate of all the people who had flight to New York City
SELECT name, license_plate
FROM people
WHERE passport_number IN (
    SELECT p.passport_number
    FROM passengers p
    JOIN flights b ON b.id = p.flight_id
    WHERE b.year = 2021 AND b.month = 7 AND b.day = 28 AND b.destination_airport_id = 8
);