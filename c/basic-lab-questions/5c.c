// Bubble sorting acesending
#include<stdio.h>
#include<stdlib.h>

int main()
{
    int size;
    printf("Please enter the size of the array.");

    scanf("%d", &size);

    int sort[size];
    printf("Please enter the array:\n");
    for (int i = 0; i < size; i++)
    {
        scanf("%d", &sort[i]);
    }

    printf("\nThe sorted Array:");

    for (int i = 0; i < size; i++)
    {
        for (int k = i; i < size; k++)
        {
            if(sort[i]<sort[k])
            {
                int temp = sort[i];
                sort[i] = sort[k];
                sort[k] = temp;
            }
        }
    }

        for (int i = 0; i < size; i++)
    {
        printf("%d", sort[i]);
    }
    return 0;
}