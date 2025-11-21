// Binary Search

#include <stdio.h>
#include<math.h>

int main()
{
    int size;

    printf("Please enter the size of the array: ");
    scanf("%d", &size);

    // Entering values for the array elements from the user:
    float array[size];
    printf("Please enter the values in sequence for the array:\n");
    for (int i = 0; i < size; i++)
    {
        scanf("\n%f",&array[i]);
    }

    int find;
    printf("Enter the number to be found: ");
    scanf("%d", &find);
    int low = 0;
    int high = size - 1;
    int check=0;
    while (low <= high)
    {
        int mid = (low + high) / 2;
        if(array[mid]==find)
        {
            printf("Number present at index of: %d", mid);
            check = 1;
            break;
        }
        else if(find>array[mid])
        {
            low = mid + 1;
        }
        else if (find<array[mid])
        {
            high = mid - 1;
        }
    }
    if (check==0)
    {
        printf("Number not found.");
    }
}