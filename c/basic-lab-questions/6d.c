// Program to find row sum and column sum and sum of all elements in a matix
#include <stdio.h>

int main()
{
    int size = 0;
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

    int sum_of_all = 0;
    //Calculating Sum of rows
    for (int i = 0; i < row; i++)
    {
        int row_sum = 0;
        for (int k = 0; k < column; k++)
        {
            row_sum = row_sum + matrix[i][k];
            sum_of_all = sum_of_all + matrix[i][k];//calculating sum of elements.
        }
        printf("Sum of row %d is: %d\n",i+1,row_sum);
    }
    // Calculating Sum of columns
    for (int k = 0; k < column; k++)
    {
        int column_sum = 0;
        for (int i = 0; i < row; i++)
        {
            column_sum = column_sum + matrix[i][k];
        }
        printf("Sum of columns %d is: %d\n", k + 1, column_sum);
    }
    printf("\nSum of All elements: %d",sum_of_all);
    return 0;
}