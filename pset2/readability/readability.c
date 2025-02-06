#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

// setting up the prototype for the function we are using
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string prompt = get_string("Text: ");

    // L and S represent average number of letters per 100 words and sentences resp.
    float L = ((float)  count_letters(prompt) / (float) count_words(prompt)) * 100;
    float S = ((float) count_sentences(prompt) / (float) count_words(prompt)) * 100;
    // formula to calculate the grade level
    float index = 0.0588 * L - 0.296 * S - 15.8;
    int average = round(index);

    // only giving the grade level if it's between 1-16.
    if (average >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (average < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n",  average);
    }
}

// function to calculate the number of letters in the given text
int count_letters(string text)
{
    int count = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isalpha(text[i]))
        {
            count++;
        }
    }
    return count;
}

// function to calculate the number of words
int count_words(string text)
{
    // Initializing words as 1 because the first word is counted as one
    int count = 1;
    string space = " ";
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (text[i] == ' ')
        {
            count++;
        }
    }
    return count;
}

// function to calculate the number of sentences in the text
int count_sentences(string text)
{
    int count = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            count++;
        }
    }
    return count;
}