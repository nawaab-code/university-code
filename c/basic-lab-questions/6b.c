// Program to perform multiplication of two matrices.
#include <stdio.h>

int main()
{
    int size = 0;

    int row, column;
    printf("Enter the number of rows and columns: ");
    scanf("%d %d", &row, &column);

    printf("\nStart entering the first matrix:\n");
    int first[row][column];
    for (int i = 0; i < row; i++)
    {
        for (int k = 0; k < column; k++)
        {
            scanf("%d", &first[i][k]);
        }
    }

    printf("\nStart entering the second matrix:\n");
    int second[row][column];
    for (int i = 0; i < row; i++)
    {
        for (int k = 0; k < column; k++)
        {
            scanf("%d", &second[i][k]);
        }
    }

    int third[row][column];
    for (int i = 0; i < row; i++)
    {
        for (int k = 0; k < column; k++)
        {
            third[i][k] = first[i][k] * second[i][k];
            printf("%d  ", third[i][k]);
        }
        printf("\n");
    }

    return 0;
}