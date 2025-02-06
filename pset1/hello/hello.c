#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // getting input from the user and priting it
    string name = get_string("What is your name?\n");
    printf("hello, %s\n", name);
}
