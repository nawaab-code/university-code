// Find whether a prime number of not using function without arguments and without return type.
#include <stdio.h>

int factorial(int number)
{
    int fact = 1;
    for (int i = 1; i <= number; i++)
    {
        fact = fact * i;
    }
    return fact;
}

int main()
{
    int number = 0;
    printf("Enter a number: ");
    scanf("%d", &number);
    if (number > 0)
        printf("Factorial of the given number: %d", factorial(number));
    else
        printf("Invalid Input.");
}