#include <stdio.h>
#include <math.h>

int main()
{
    int size;

    printf("Please enter the size of the array: ");
    scanf("%d", &size);

    // Entering values for the array elements from the user:
    float array[size];
    printf("Please enter the values for the array:\n");
    for (int i = 0; i < size; i++)
    {
        scanf("\n%f",&array[i]);
    }

    float average=0;
    for (int i = 0; i < size; i++)
    {
        average = average + array[i];
    }
    printf("The average of the values of the array: %f", average / size);
}