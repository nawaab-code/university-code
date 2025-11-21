//Print the square of index and print it.

#include<stdio.h>
#include<math.h>

int main()
{
    int size;
    printf("Enter the size of the array.");
    scanf("%d", &size);

    int array[size];

    for (int i = 0; i < size; i++)
    {
        array[i] = pow((i + 1), 2);
    }
    for (int i = 0; i < size; i++)
    {
        printf("%d  %d\n", i + 1, array[i]);
    }
}