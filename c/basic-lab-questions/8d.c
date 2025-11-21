#include<stdio.h>
#include<stdlib.h>

int main()
{
    char first[100];
    char second[100];

    printf("Enter the string:\t");
    gets(first);

    printf("Enter the substring string:\t");
    gets(second);
    int check = 0;
    int k = 0;
    int i = 0;
    while(first[i] != '\0')
    {
        if(first[i]==second[k])
        {
            k += 1;
            if (second[k] == '\0')
                check = 1;
        }
        else
            k = 0;
        i += 1;
    }

    if(check==1)
        printf("Substring Present.");
    else
        printf("Substring Not Present.");
}