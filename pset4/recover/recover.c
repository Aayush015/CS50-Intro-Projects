#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// make the block size of 512 as a global variable
#define BLOCK_SIZE 512

/**
 * Function to check if the particular buffer contains the header for the start
 * of a jpeg file.
*/
int is_jpeg_header(unsigned char buffer[])
{
    // Check if the buffer contains a JPEG header
    return (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0);
}

/**
 * main to execute the code
*/
int main(int argc, char *argv[])
{
    // check if the program is executed with proper arguments
    if (argc < 2)
    {
        printf("Usage: ./memory_recovery <memory card name>\n");
        return 1;
    }

    // open the card file from the server as a read
    FILE *memory_card = fopen(argv[1], "rb");
    if (memory_card == NULL)
    {
        printf("Error opening the specified file.\n");
        return 1;
    }

    // create a buffer of size 512
    unsigned char buffer[BLOCK_SIZE];
    int jpeg_counter = 0;
    // each jpeg file present in the memory card
    FILE *jpeg_file = NULL;

    // read the file of 512 bytes from the memory card until it exists
    while (fread(buffer, sizeof(unsigned char), BLOCK_SIZE, memory_card) == BLOCK_SIZE)
    {
        if (is_jpeg_header(buffer))
        {
            if (jpeg_file != NULL)
            {
                // Close the previously found JPEG file
                fclose(jpeg_file);
            }

            char filename[8];
            // write the name of the file as a number of jpeg found using jpeg_counter
            sprintf(filename, "%03i.jpg", jpeg_counter);
            // write with the above file name into that particular jpeg
            jpeg_file = fopen(filename, "wb");

            if (jpeg_file == NULL)
            {
                printf("Error creating JPEG file.\n");
                fclose(memory_card);
                return 1;
            }
            jpeg_counter++;
        }

        if (jpeg_file != NULL)
        {
            // Write the buffer content to the JPEG file
            fwrite(buffer, sizeof(unsigned char), BLOCK_SIZE, jpeg_file);
        }
    }
    if (jpeg_file != NULL)
    {
        // Close the last JPEG file
        fclose(jpeg_file);
    }
    // close the card.raw file when we are done reading till the end
    fclose(memory_card);
    return 0;
}