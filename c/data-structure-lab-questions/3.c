#include <stdio.h>
#define MAX 100

int stack[MAX]; // initialize stack

int push();               // To push element into the stack
int pop();                // To delete element from the stack
int palindrome();         // To check if the stack is palindrome or not
int overflow_underflow(); // To check for stack overflow and underflow
int status();             // To check for the top of the element

int main()
{
    int size;
    printf("Please enter the size of the stack:");
    scanf("%d", &size);

    // Entering elements into the stack from the user
    for (int i = 0; i < size; i++)
    {
        scanf("%d", &stack[i]);
    }
    stack[size] = '\0'; // Null character to mark the end of the stack

    int max = size;
    int top = 0;
    for (int i = 0; i != '\0'; i++)
    {
        top++;
    }


    

    return 0;
}

push(int max, int top)
{
    if (top == --max)
    {
        printf("Overflow,");
        exit();
    }
    else
    {
        printf("Enter the integer to be pushed to the stack.");
        int element;
        scanf("%d", element);

        stack[top] == element;
        stack[++top] == '\0';
        top++;
    }
}

pop(int max, int top)
{
    if(top==0 && stack[0]=='\0')
    {
        printf("Underflow.");
    }
    else
    {
        top = '\0';
        top--;

    }
}

palindrome(int max, int top)
{
    int flag = 0;
    for (int i = 0; i < top / 2; i++)
    {
        if (stack[i] != stack[top - i - 1])
        {
            flag = 1;
            break;
        }
    }
    if (flag == 1)
    {
        printf("The stack is not a palindrome.");
    }
    else
    {
        printf("The stack is a palindrome.");
    }
}
overflow_underflow(int max, int top)
{
    if (top == --max)
    {
        printf("Overflow,");
        exit();
    }
    else if(top==0 && stack[0]=='\0')
    {
        printf("Underflow.");
    }
    else
    {
        printf("No overflow or underflow.");
    }
}
status(int max, int top)
{
    if(top==0 && stack[0]=='\0')
    {
        printf("The stack is empty.");
    }
    else
    {
        printf("The top element is %d", stack[top - 1]);
    }
}
