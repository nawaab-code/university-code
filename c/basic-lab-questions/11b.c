// Program to calculate the subject - wise and student - wise total marks and store them as a part of structure.

#include<stdio.h>
struct marks
{
    int subject[3];
    int total;
};
int main()
{
    // Creating an array of 3 as in for 3 students. And initializing
    struct marks student[3] =
        {
            {{20, 30, 40}, 0}, // Initializing marks of each student.
            {{10, 50, 70}, 0}, // Leaving the total as 0, be calculated later.
            {{60, 10, 90}, 0}};
    // Totaling marks of each student and storing it in total
    for (int i = 0; i < 3; i++)
    {
        for (int k = 0; k < 3; k++)
        {
            student[i].total = student[i].total + student[i].subject[k];
        }
    }
    
    // Creating an object to store total marks of each suject.
    struct marks suject_total = {0, 0, 0, 0}; // Initializing as 0.
    
    // Total for each suject individually
    for (int i = 0; i < 3; i++) // Loop for 3 sujects
    {
        for (int j = 0; j < 3; j++) // Loop of 3 students score
        {
            suject_total.subject[i] = suject_total.subject[i] + student[j].subject[i];
        }
        suject_total.total = suject_total.total + suject_total.subject[i];
    }

    // Printing total each student
    printf("Sudent\tTotal\n");
    for (int i = 0; i < 3; i++)// Printing total each student
    {
        printf("Sudent %d: %d\n",i+1,student[i].total);
    }
    printf("\n");//Creating a space.

    // Printing total of each subject
    printf("Subject\tTotal\n");
    for (int i = 0; i < 3; i++) // Printing total each student
    {
        printf("Sudent %d: %d\n",i+1,suject_total.subject[i]);
    }
    printf("\n");
    printf("Grand Total:%d", suject_total.total);

    return 0;
}