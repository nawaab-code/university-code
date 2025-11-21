#include <stdio.h>
#include <math.h>

int factorial(int fact)
{
    if(fact<1)
        return 1;
    else
        return fact * factorial(fact - 1);
}

int main()
{
    int fact;
    printf("Please enter a number: ");
    scanf("%d", &fact);

    printf("The factorial of the number %d is %d.", fact,factorial(fact));
    return 0;
}