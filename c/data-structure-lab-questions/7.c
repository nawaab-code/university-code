/* A Call center phone 	system has to hold the phone calls from customers and provide service based on the arrival time of the calls.
Write a C program to simulate this system using appropriate data structure.
Program should have options to add and remove the phone calls in appropriate order for their service. */

//The calls will be identified by assigning each of them a id.

#include<stdio.h>
#include<stdlib.h>

typedef struct node
{
	int id;
	struct node *link;
}NODE;

NODE *head;

void enqueue(int id)// To add a call to the queue.
{
	NODE *newnode=malloc(sizeof(NODE));

	if(newnode==NULL)
	{
		printf("Queue is full, please dequeue first, to accept new calls.\n");
		return;
	}

	newnode->id=id;
	newnode->link=NULL;

	if(head==NULL)
	{
		head=newnode;
		return;
	}

	NODE *ptr=head;
	while(ptr->link!=NULL)
	{
		ptr=ptr->link;
	}

	ptr->link=newnode;

	return;
}

void dequeue()
{
	if(head==NULL || head->link==NULL)
	{
		printf("No calls in waiting\n");
		return;
	}

	NODE *ptr=head;

	while(ptr->link->link!=NULL)
	{
		ptr=ptr->link;
	}
	ptr->link=NULL;
	printf("Call served:\t%d\n",ptr->id);
	free(ptr->link);

	return;
}

void display()
{
	NODE *ptr=head;
	printf("Calls in waiting:\n");
	while(ptr!=NULL)
	{
		printf("%d\n",ptr->id);
		ptr=ptr->link;
	}
	return;
}

int main()
{
	while(1)
	{
		printf("Select from the following:\n1. To add a call.\n2. To serve\n3. Display\n4. Exit\n");
		int select;
		scanf("%d",&select);

		switch(select)
		{
			case 1:
				printf("Enter call id:\n");
				int id;
				scanf("%d",&id);
				enqueue(id);
				break;
			case 2:
				dequeue();
				break;
			case 3:
				display();
				break;
			case 4:
				exit(1);
				break;
		}
	}
	return 0;
}
