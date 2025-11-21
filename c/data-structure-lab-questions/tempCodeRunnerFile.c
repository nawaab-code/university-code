#include <stdio.h>
#define MAX 100
int array[MAX]; // Array of max capacity of 100
int size = 0;   // The upper limit defined by user in main

void display();
void insert();
void delete();
void exit();

int main()
{

    // Gettting the size of the array from the user.
    printf("Enter the size of the array,(maximum size of 100):\t");
    scanf("%d", &size);
    printf("Please enter the elements of the array:\n");

    for (int i = 0; i < size; i++)
    {
        scanf("\t%d", &array[i]);
    }

    // Creating a switch-case for selecting the function to be performed
    printf("Please enter the number corresponding to the function which is to be performed:\n");
    printf("1. Display the elements of the array\n");
    printf("2. Insert an element in the array\n");
    printf("3. Delete an element from the array\n");
    printf("4. Exit the program\n");
    int select;
    scanf("%d", &select);
    switch (select)
    {
    case 1:
        display();
        break;
    case 2:
        insert();
        break;
    case 3:
        delete();
        break;
    case 4:
        exit(0);
        break;

    default:
        break;
    }
}

void display()
{
    if (size <= 0)
    {
        printf("The array is empty.");
        exit(0);
    }

    printf("\nThe elements of the array as follows:");
    for (int i = 0; i < size; i++)
    {
        printf("\t%d", array[i]);
        printf("\n");
    }
}

void insert()
{
    if (size >= MAX)
    {
        printf("The array is full, cannot insert any more elements.");
        exit(0);
    }
    int position, element;
    printf("Enter the position at which the elements needs to inserted:\t");
    scanf("%d", &position);
    printf("Enter the element that is to be inserted into that position:\t");
    scanf("%d", &element);

    if (position < 1 || position > size + 1)
    {
        printf("Invalid position\n");
        return;
    }

    for (int i = size; i >= position; i--)
    {
        array[i] = array[i - 1];
    }
    array[position - 1] = element;
    size++;

    printf("\nThe updated elements of the array are as follows:");
    for (int i = 0; i < size; i++)
    {
        printf("\t%d", array[i]);
        printf("\n");
    }
}

void delete()
{
    int pos;
    if (size == 0)
    {
        printf("Array is empty\n");
        return;
    }
    printf("Enter position to delete (1 to %d): ", size);
    scanf("%d", &pos);

    if (pos < 1 || pos > size)
    {
        printf("Invalid position\n");
        return;
    }

    for (int i = pos - 1; i < size - 1; i++)
    {
        array[i] = array[i + 1];
    }
    size--;
}