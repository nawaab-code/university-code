//input employee details: name, salary and address, print it using structures:
#include<stdio.h>
struct employee
{
    char name[100];
    float salary;
    char address[100];
};
int main()
{
    struct employee details;
    printf("Enter the name of the employee:\t");
    fgets(details.name,100,stdin);

    printf("Enter salary of the employee:\t");
    scanf("%f",&details.salary);

    printf("Enter the address of the employee:\t");
    fgets(details.address,100,stdin);

    printf("Name:%s\tSalary:%f\tAddress:%s",details.name,details.salary,details.address);
}