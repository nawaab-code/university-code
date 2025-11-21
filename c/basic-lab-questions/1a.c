// C-Program to calculate the sum of three numbers
// C-Program to demonstrate a Simple Calculator

#include<stdio.h>

void add()
{
    float sum = 0;
    float temp = 0;
    printf("Please enter three values:\n");
    for (int i = 0; i < 3; i++)
    {
        printf("Enter a value:\t");
        scanf("%f",&temp);
        sum += temp;
    }
    printf("Sum of the numbers:\t%f\n",sum);
}

void simple()
{
    float one, two;

    printf("Enter First digit:\t");
    scanf("%f",&one);
    printf("Enter Second digit:\t");
    scanf("%f", &two);

    char ch;
    printf("Enter + for sum, - for negation, * for multiplication, / for division.:\t");
    scanf(" %c", &ch);

    switch (ch)
    {
    case '+':
        printf("The sum of two operands: %f\n", one + two);
        break;

    case '-':
        printf("The subraction of two oprands: %f\n", one - two);
        break;
        
    case '*':
        printf("The multiplication of two oprands: %f\n", one * two);
        break;

    case '/':
        printf("The division of two oprands: %f\n", one / two);
        break;

    default:
        printf("Invalid Input, try again");
        break;
    }

    
}

int main()
{
    add();
    simple();

    return 0;
}
