// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <cs50.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// keep track of the total number of words
int tot_num_words = 0;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int hash_tab_value = hash(word);
    node *cursor = table[hash_tab_value];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int hash = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        hash += (toupper(word[i]) - 'A');
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the file as a read mode
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Unable to open the file");
        return false;
    }
    // Store the file's content as a string using word
    char word[LENGTH];
    while (fscanf(file, "%s", word) != EOF)
    {
        // malloc for each node in the hash table
        node *n = malloc(sizeof(node));
        // set the next node to null so that it doesn't store any garbage value
        n->next = NULL;
        if (n == NULL)
        {
            unload();
            return false;
        }
        int hash_value = hash(word);
        strcpy(n->word, word);
        if (table[hash_value] == NULL)
        {
            table[hash_value] = n;
        }
        else
        {
            n->next = table[hash_value];
            table[hash_value] = n;
        }
        tot_num_words++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return tot_num_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    node *cursor = NULL;
    node *tmp = NULL;
    for (int i = 0; i < N; i++)
    {
        cursor = table[i];
        // free each linked list in the hash table
        while (cursor != NULL)
        {
            tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
        // free that particular hash table itself after the linked list has been freed
        table[i] = NULL;
    }
    return true;
}