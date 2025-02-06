from cs50 import get_string


def main():
    input = get_string("Text: ")

    L = (count_letters(input)/count_words(input)) * 100
    S = (count_sentences(input)/count_words(input)) * 100

    # calculate the index
    index = round(0.0588 * L - 0.296 * S - 15.8)

    # calculate the grade level
    if (index >= 16):
        print("Grade 16+")
    elif (index < 1):
        print("Before Grade 1")
    else:
        print(f"Grade {index}")

# count the total num of letters in the input


def count_letters(input):
    count = 0
    for i in range(len(input)):
        if (input[i].isalpha()):
            count += 1
    return count


# count the total num of words starting with 1
def count_words(input):
    space = " "
    count = 1
    for i in range(len(input)):
        if (input[i] == space):
            count += 1
    return count


# count the total sentences in input
def count_sentences(input):
    count = 0
    for i in range(len(input)):
        if (input[i] == '.' or input[i] == '!' or input[i] == '?'):
            count += 1
    return count


# start the program with the current module
if __name__ == "__main__":
    main()
