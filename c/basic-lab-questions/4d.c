//Fibonacci number by recursion

#include<stdio.h>
#include<stdlib.h>
#include<math.h>

int fib(int a, int b, int limit);

int main()
{
    int limit;
    printf("Please enter a limit:\t");
    scanf("%d",&limit);
    printf("\n");

    fib(0, 1, limit);

    return 0;
}

int fib(int a,int b,int limit)
{
    if(limit>=0)
    {
        printf("%d\n", a);
        return fib(b,a+b,--limit);
    }
    else
    {
        return 0;
    }
}