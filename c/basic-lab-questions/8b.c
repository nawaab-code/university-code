#include<stdio.h>
#include<stdlib.h>

int main()
{
    char first[100];
    char second[100];

    printf("Enter the first string:\t");
    gets(first);

    printf("Enter the second string:\t");
    gets(second);

    int i = 0;
    while (first[i] ==second[i] && first[i]!='\0' && second[i]!='\0')
    {
        i += 1;
    }

    if(first[i]==second[i])
        printf("They are same");
    else
        printf("They are not similar");
}