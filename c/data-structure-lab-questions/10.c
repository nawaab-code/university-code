//Write a C program to maintain a stack of integers using linked implementation method.
#include<stdio.h>
#include<stdlib.h>

typedef struct node
{
	int data;
	struct node *link;
}NODE;

NODE *head=NULL;

void push(int number)
{
	NODE *newnode=malloc(sizeof(NODE));

	if(newnode==NULL)//if the memory ran out, it will assign a NULL value to the newly created pointer, therefore will be regarded as an 'overflow' since no memory left to work with.
	{
		printf("Overflow");
		return;
	}
	newnode->data=number;
	newnode->link=NULL;

	if(head==NULL)//if the node is the first node.
	{
		head=newnode;
		return;
	}

	NODE *ptr=head;
	while(ptr->link!=NULL)//reaching to the last node.
	{
		ptr=ptr->link;
	}
	ptr->link=newnode;

	return;
}

void pop()
{
	if(head==NULL)
	{
		printf("Underflow");
		return;
	}

	NODE *ptr=head;
	while(ptr->link->link!=NULL)
	{
		ptr=ptr->link;
	}

	printf("%d\n",ptr->link->data);

	free(ptr->link);
	ptr->link=NULL;

	return;
}

void display()
{
	NODE *ptr=head;

	while(ptr!=NULL)
	{
		printf("%d\n",ptr->data);
		ptr=ptr->link;
	}
	return;
}

int main()
{
	while(1)
	{
		printf("Please enter the number in accordance to the selected operation:\n1.Push an element.\n2.Pop an element out of the stack.\n3.Display all the elements of the stack.\n4. Exit.\n");
		int select;
		scanf("%d",&select);

		switch(select)
		{
			case 1:
				printf("Please enter the element to be pushed into the stack:\t");
				int x;
				scanf("%d",&x);
				push(x);
				break;
			case 2:
				pop();
				break;
			case 3:
				display();
				break;
			case 4:
				exit(1);
				break;
			default:
				printf("The input is invalid, please try again:\n");
		}
	}
	return 0;
}

