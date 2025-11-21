#include <stdio.h>

int main(void)
{
    // Size of the array by the user
    int size = 0;
    printf("Enter the size of the array (> 0):\t");
    if (scanf("%d", &size) != 1 || size <= 0)
    {
        printf("Invalid size.\n");
        return 1;
    }

    float a[size]; // Defining the size of the array (VLA)

    printf("Enter the elements of the array:\n");
    for (int i = 0; i < size; i++)
    {
        if (scanf("%f", &a[i]) != 1)
        {
            printf("Invalid input encountered.\n");
            return 1;
        }
    }

    // Calculating the largest number in the array
    float m = a[0];
    for (int i = 1; i < size; i++)
    {
        if (a[i] > m)
            m = a[i];
    }

    printf("The largest number in the array:\t%f\n", m);
    return 0;
}
