#include <stdio.h>
#include <math.h>

float quiz[4];
float mid1;
float mid2;
float final;

int main()
{
    //Entering the quizes marks

    for (int i = 0; i < 4; i++)
    {
        printf("Please enter the %d quiz marks: ", i + 1);
        scanf("%f", &quiz[i]);
    }

    //Entering the first mid-term marks

    printf("Please enter the first mid-term marks: ");
    scanf("%f", &mid1);

    printf("Please enter the second mid-term marks: ");
    scanf("%f", &mid2);

    //Entering the second mid-term marks

    printf("Please enter the finals marks: ");
    scanf("%f", &final);

    //Calculating the average score

    float average_quiz;

    for (int i = 0; i < 4; i++)
    {
        average_quiz = average_quiz + quiz[i];
    }

    average_quiz = (average_quiz / 400) * 100;
    float average_midterm = (((mid1 + mid2) / 200) * 100);
    float average_total = ((average_quiz + average_midterm + final) / 300) * 100;

    printf("\n");
    printf("Total average score for quiz: %f\n", average_quiz);
    printf("Total average score for midterms: %f\n", average_midterm);
    printf("Total average score for finals: %f\n", final);
    printf("Total average score: %f\n", average_total);

    return 0;
}