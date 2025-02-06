#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // getting the input from the user
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height <= 0 || height > 8);

    // iterating for each row
    for (int row = 0; row < height; row++)
    {
        // creating the first hashes and spaces in front of them
        for (int space = 0; space < height; space++)
        {
            if (row + space < height - 1)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        // printing two spaces between brick of hashes
        printf("  ");
        // printing the second brick of hashes
        for (int column = 0; column < height; column++)
        {
            if (column <= row)
            {
                printf("#");
            }
        }
        
        // taking the command line to the next line
        printf("\n");
    }
}