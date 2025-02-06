#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

// used to take the command line arguments
int main(int argc, string argv[])
{
    // p will be used as an input for plaintext
    string p;
    // runs only if there are two inputs otherwise shows an error
    if (argc == 2)
    {
        // to check if both of the given arguments are digits
        for (int i = 0, len = strlen(argv[1]); i < len; i++)
        {
            if (!isdigit(argv[1][i]))
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        // if given argument is a digit then changing that to int
        int keyword = atoi(argv[1]);
        p = get_string("plaintext:  ");
        for (int j = 0, length = strlen(p); j < length; j++)
        {
            if (isupper(p[j]))
            {
                // to check if the cipher letter is out of the boundary of english alphabet
                if (p[j] + keyword > 'Z')
                {
                    // set position back to starting from A
                    p[j] = ((p[j] + keyword - 'A') % 26) + 'A';
                }
                else
                {
                    p[j] += keyword % 26;
                }
            }
            // Implementation for lowercase alphabets
            if (islower(p[j]))
            {
                if (p[j] + keyword > 'z')
                {
                    p[j] = ((p[j] + keyword - 'a') % 26) + 'a';
                }
                else
                {
                    p[j] += keyword % 26;
                }
            }

        }
        printf("ciphertext:  %s\n", p);
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

}