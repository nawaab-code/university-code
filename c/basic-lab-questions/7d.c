// Find whether a prime number of not using function without arguments and without return type.
#include <stdio.h>

void prime()
{
    int number = 0;
    printf("Enter a number: ");
    scanf("%d", &number);

    int check = 0;
    for (int i = 1; i <= number; i++)
    {
        if (number % i == 0)
            check += 1;
    }
    if (check == 2)
        printf("Prime Number.");
    else
        printf("Not a Prime Number");
}

int main()
{
    prime();
}