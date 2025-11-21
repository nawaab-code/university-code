// Transposing A Matrix

#include<stdio.h>
#include<stdlib.h>

int main()
{
    int size=0;

    int row, column;
    printf("Enter the number of rows and columns: ");
    scanf("%d %d", &row, &column);

    printf("\nStart entering the matrix:\n");
    int matrix[row][column];
    for (int i = 0; i < row; i++)
    {
        for (int k = 0; k < column; k++)
        {
            scanf("%d", &matrix[i][k]);
        }
    }

    int transpose[row][column];
    // Finding the transpose of the matrix

    int a = row - 1;
    for (int i = 0; i < row; i++)
    {
        int b = column - 1;
        for (int k = 0; k < column; k++)
        {
            transpose[a][b] = matrix[i][k];
            b -= 1;
        }
        a -= 1;
    }

    for (int i = 0; i < row; i++)
    {
        for (int k = 0; k < column; k++)
        {
            printf("%d\t", transpose[i][k]);
        }
        printf("\n");
    }
}