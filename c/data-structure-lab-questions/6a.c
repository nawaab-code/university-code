#include<stdio.h>
#define MAX 100

int array[MAX];
int size;

int enter()
{
    printf("Enter the size of the array.\n");
    scanf("%d", &size);

    printf("Enter the elements of the array:");
    for (int i = 0; i < size; i++)
    {
        scanf("%d",&array[i]);
    }

    return 0;
}

int sort()
{
    for (int i = 0; i < size; i++)
    {

        for (int k = 0; k < size; k++)
        {
            if(array[k]>array[i])
            {
                int temp = array[i];
                array[i] = array[k];
                array[k] = temp;
            }
        }
    }

    return 0;
}

int binary_search()
{
    
}

int output()
{
    int element;
    printf("Enter the element to be searched: ");
    scanf("%d", &element);

}
int main()
{
    enter();
    sort();
    output();
    
}