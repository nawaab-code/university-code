#include <stdio.h>

void demoFunction()
{
    auto int autoVar = 0;     // Automatic variable (default for local variables)
    static int staticVar = 0; // Static variable retains value

    autoVar++;   // Increments with every function call
    staticVar++; // Retains its value across function calls

    printf("autoVar: %d, staticVar: %d\n", autoVar, staticVar);
}

int main()
{
    printf("First call:\n");
    demoFunction();

    printf("Second call:\n");
    demoFunction();

    printf("Third call:\n");
    demoFunction();

    return 0;
}