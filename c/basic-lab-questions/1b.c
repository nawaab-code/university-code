// C Program to calculate the area and the circumference of a circle using PI as a defined constant.

#include<stdio.h>

#define PI 3.142 //Defining the constant pi as 3.142

int main()
{
    float pi = PI;// Storing the value of pi in a variable.

    float radius;
    printf("Enter the radius of the circle:\t");
    scanf("%f", &radius);

    // Calculating the area of a circle
    printf("Area of the circle: %f\n", pi*radius*radius);

    //Calculating the circumference of a circle
    printf("Circumference of the circle: %f", 2 * pi * radius);

    return 0;
}