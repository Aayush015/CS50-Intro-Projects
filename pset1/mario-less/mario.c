
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // getting input from the user
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height <= 0 || height >= 9);

    // creating a wall of hashes
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height; j++)
        {
            // we use height-1 because counting starts at 0
            if (i + j < height - 1)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        // new line after end of the line
        printf("\n");
    }
}
