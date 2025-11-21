//  Converting Binary to decimal number.
#include<stdio.h>
#include<stdlib.h>
#include<math.h>

int main()
{
    int binary;
    printf("Please enter a binary number:\t");
    scanf("%d",&binary);

    float decimal = 0;
    for (int i = 0; binary>0; i++)
    {
        decimal = decimal + ((binary % 10) * (pow(2, i)));
        binary = binary / 10;
    }

    printf("\nDecimal Equivalent= %f", decimal);

    return 0;
}