import csv
import sys


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # TODO: Read database file into a variable
    database = []
    with open(sys.argv[1], "r") as database_file:
        # open the database_file into reader and append that in a array called database
        reader = csv.DictReader(database_file)
        for row in reader:
            database.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as sequence_file:
        sequence = sequence_file.read()

    # TODO: Find longest match of each STR in DNA sequence
    # keep the database into a list excluding the first key called 'name'
    str = list(database[0].keys())[1:]
    matching_str = {}
    for i in range(len(str)):
        # make a dictionary with number of match in the sequence and with name as key
        matching_str[str[i]] = longest_match(sequence, str[i])

    # TODO: Check database for matching profiles
    # all_match keeps track of the number of matches between the sequence and database file data
    for name in database:
        all_match = 0
        for sub_str in str:
            # if the data does not match
            if matching_str[sub_str] != int(name[sub_str]):
                break
            # add to all_match if the data matches
            all_match += 1
        # at the end of the loop, check if every strs' matched
        if all_match == len(str):
            print(name["name"])
            sys.exit(0)

    # there's no match after checking the whole loop
    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
