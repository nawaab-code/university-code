// Checking for palindrome number with using while loop.

#include <stdio.h>
#include <math.h>

int palindrome()
{
    int number;
    printf("Please enter a number to be checked: ");
    scanf("%d", &number);

    int temporary = number;
    int new = 0;
    while (temporary > 0)
    {
        new = (new * 10) + temporary % 10;
        temporary = temporary / 10;
    }
    if (number==new)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

int main()
{
    if(palindrome()==1)
    printf("The number is palindrome");
    else
    printf("The number is not a palindrome.");
}