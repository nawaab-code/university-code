#include <stdio.h>
#include <stdlib.h>

int main()
{
    char first[100]; // Entering the first sentence
    printf("Enter the first String: ");
    fgets(first, sizeof(first), stdin);

    char second[100]; // Entering the second sentence
    printf("Enter the Second String: ");
    fgets(second, sizeof(second), stdin);

    // Remove newline from first string
    for (int i = 0; first[i] != '\0'; i++)
    {
        if (first[i] == '\n')
        {
            first[i] = '\0';
            break;
        }
    }

    char final[200];// Creates an array to store the newly formed string

    int i = 0; //Copies first string to the new string array
    for (i = 0; first[i] != '\0'; i++)
        final[i] = first[i];
    final[i] = ' ';
    i += 1;

    int j = 0;//Copies second string to the array
    for (j = 0; second[j] != '\0'; j++)
    {
        final[i + j] = second[j];
    }
    final[i + j] = '\0';

    printf("The Combined String: %s", final);

    return 0;
}