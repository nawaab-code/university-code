#include <stdio.h>
#include<math.h>

int main()
{
    char decide;
    printf("Enter the following the deseired area output:\nsquare: s\nrectangle: r\ntriangle: t\ncircle: c\n");
    scanf("%c",&decide);

    switch (decide)
    {

    case 's':{
        float side=0;
        printf("Please enter the side of the square: ");
        scanf("%f", &side);

        printf("area of the sqaure: %f\n", pow(side, 2));
        break;
    }

    case 'r':{
        float length;
        float breadth;

        printf("Please enter the length of the rectangle: ");
        scanf("%f",&length);
        printf("Please enter the breadth of the rectangle: ");
        scanf("%f", &breadth);

        printf("The area of the rectangle is: %f\n",length*breadth);
        break;}
    
    case 'c':{
        float radius;
        printf("Please enter the radius of the circle: ");
        scanf("%f",&radius);

        printf("The area of the circle: %f",M_PI*pow(radius,2));
        break;}

    case 't':{
        float base;
        float height;
        printf("Please enter the base of the triangle: ");
        scanf("%f", &base);
        printf("Please enter the heght of the triangle: ");
        scanf("%f", &height);

        printf("Area of the trianle: %f", 0.5 * base * height);
        break;}

    default :{
        printf("Invalid output, try again.");
        main();
        break;}
    }
}