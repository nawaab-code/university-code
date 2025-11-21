// Diagonals as 0

#include<stdio.h>
#include<stdlib.h>

int main()
{
    int size=0;
    printf("Enter the number of rows and columns: ");
    scanf("%d", &size);

    printf("\nStart entering the matrix:\n");
    int matrix[size][size];
    for (int i = 0; i < size; i++)
    {
        for (int k = 0; k < size; k++)
        {
            scanf("%d", &matrix[i][k]);
        }
    }

    int i = 0, k = 0;
    while (i < size)
    {
        matrix[i][k] = 0;
        i++;
        k++;
    }
    int a = size-1,b =0;
    while (a>=0)
    {
        printf("\ta=%d\n",a);
        matrix[a][b] = 0;
        a--;
        b++;
    }

    for (int i = 0; i < size; i++)
    {
        for (int k = 0; k < size; k++)
        {
            printf("%d\t", matrix[i][k]);
        }
        printf("\n");
    }
}