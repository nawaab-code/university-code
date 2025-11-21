#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int main()
{
    char first[100];
    char second[100];
    char third[200];
    char combine[200];

    printf("Enter the first string:\t");
    gets(first);

    printf("Enter the second string:\t");
    gets(second);

    if(strcmp(first,second)==0)
        printf("String are siliar.\n");
    else
        printf("Strings are different.\n");

    strcpy(third,second);
    printf("Copied String:\t%s\n", third);

    strcat(first,second);
    printf("Combined String as one:\t%s\n",first);

    printf("Length:\t%zu\n", strlen(second));

    if(strstr(first,second)==NULL)
        printf("string not found");
    else
        printf("String found");
}