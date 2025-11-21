#include<stdio.h>
#include<stdlib.h>
#include<math.h>

int main()
{
    int decimal;
    printf("Please enter a decimal number:\t");
    scanf("%d",&decimal);

    int binary = 0;
    printf("\nBinary Equivalent:\t");
    while (decimal > 0)
    {
        binary = (binary*10)+(decimal % 2);
        decimal = decimal / 2;
    }
    
    while (binary>0)
    {
        printf("%d",binary%10);
        binary = binary / 10;
    }
}