// Finding factorial of a number using loop

#include <stdio.h>
#include <math.h>

int main()
{
    int base;
    int factorial=1;

    printf("Please enter a number for factorial.");
    scanf("%d",&base);

    if (base==0)
    {
        printf("The Factorial of the number %d is: 0",base);
        return 0;
    }

    for (int i = 1; i <=base; i++)
    {
        factorial = i * factorial;
    }

    printf("The Factorial of the number %d is: %d", base, factorial);

    return 0;
}