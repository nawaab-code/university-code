#include<stdio.h>
#include<stdlib.h>

typedef struct node
{
	struct node *previous;
	int data;
	struct node *next;
}NODE

void insert()
{
	printf("Please enter the element to be inserted into the linked list
}

void delete()
{

}

void display()
{

}

int main()
{
	while(1)
	{
		printf("Please choose from the given options:\n1. Insert\n2. Delete\n3.Display\n 4. Exit\n");
		int select;
		scanf("%d",&select)
		switch(select)
		{
			case 1:
				insert();
				break;
			case 2:
				delete();
				break;
			case 3:
				display();
				break;
			case 4:
				exit(1);
				break;
			default:
				printf("Invalid input, please try again.\n");
		}
	}
}
