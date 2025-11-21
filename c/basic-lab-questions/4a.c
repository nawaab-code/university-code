//Write a program to print a number series from 1 to a user defined limit in a form or right angle triangle
#include <stdio.h>
#include<stdlib.h>
#include<math.h>
int main()
{
    int limit;
    printf("Please enter the limit in form of rows: \t");
    scanf("%d",&limit);
    printf("\n");

    int run=1;
    for (int i = 1; i <= limit; i++)
    {
        for (int k = 1; k<=i; k++)
        {
            printf(" %d",run);
            run++;
        }
        printf("\n");
        }
    return 0;
}