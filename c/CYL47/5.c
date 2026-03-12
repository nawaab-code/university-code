#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

int partition(int arr[], int low, int high)
{
    int pivot = arr[high];
    int i = low - 1;

    for(int j = low; j < high; j++)
    {
        if(arr[j] <= pivot)
        {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }

    swap(&arr[i + 1], &arr[high]);
    return i + 1;
}

void quickSort(int arr[], int low, int high)
{
    if(low < high)
    {
        int pi = partition(arr, low, high);

        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

int main()
{
    int n, i;
    int *arr;
    clock_t start, end;
    double time_taken;

    printf("Enter number of transactions: ");
    scanf("%d", &n);

    arr = (int*)malloc(n * sizeof(int));

    srand(time(0));

    printf("\nGenerated Transaction Amounts:\n");
    for(i = 0; i < n; i++)
    {
        arr[i] = rand() % 100000;   // transaction amounts
        printf("%d ", arr[i]);
    }

    start = clock();

    quickSort(arr, 0, n - 1);

    end = clock();

    time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("\n\nSorted Transaction Amounts:\n");
    for(i = 0; i < n; i++)
    {
        printf("%d ", arr[i]);
    }

    int largest = arr[n-1];

    printf("\n\nLargest Transaction Amount = %d\n", largest);

    printf("Time taken to sort = %f seconds\n", time_taken);

    free(arr);

    return 0;
}
