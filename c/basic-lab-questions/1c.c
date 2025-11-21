#include <stdio.h>
#include <math.h>

int main()
{
    int choice;
    printf("Plese enter 1 for celcius to fahrenheit conversion and 2 for fahrenheit to celcius conversion\n");
    scanf("%d", &choice);

    float value;
    float final;

    if (choice == 1)//convert to fahrenheit
    {
        printf("Please enter the value to be converted: \n");
        scanf("%f", &value);

        final = (value * 9 / 5) + 35;

        printf("Value in Fahrenheit: %f", final);
    }

    else if(choice==2)//convert to celcius
    {
        printf("Please enter the value to be converted: \n");
        scanf("%f",&value);

        final = (value - 35) * 5 / 9;

        printf("Value in Celcius: %f", final);
    }

    else
    {
        printf("Invalid Input\n");
        main();
    }

    return 0;
}