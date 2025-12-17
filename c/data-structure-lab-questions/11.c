#include<stdio.h>
#include<stdlib.h>

typedef struct node
{
	struct node *previous;
	int data;
	struct node *next;
}NODE;

NODE *head;

void insert()
{
	int value;
	int search;
	printf("Please enter the element to be inserted into the linked list:\t");
	scanf("%d",&value);
	printf("Please element to be before which element is added:\t");
	scanf("%d",&search);

	NODE *ptr=head;
	while(ptr!=NULL && ptr->data!=value)
	{
		ptr=ptr->next;
	}

	if(ptr==NULL)
	{
		printf("Element not found in the list.\n");
		return;
	}

	NODE *newnode=malloc(sizeof(NODE));
	newnode->data=value;
	newnode->previous=ptr->previous;
	ptr->previous=newnode;

	if(ptr->previous!=NULL)
	{
		ptr->previous->next=newnode;
	}
	else
	{
		head=newnode;
	}
	ptr->previous=newnode;
	return;
}

void delete()
{
	int search;
	printf("Please enter the element to be deleted from the list:\t");
	scanf("%d",&search);
	NODE *ptr=head;

	if(head==NULL)
	{
		printf("The list is empty\n");
		return;
	}

	while(ptr==NULL && ptr->data!=search)
	{
		ptr=ptr->next;
	}

	if(ptr==NULL)
	{
		printf("Element not found");
		return;
	}

	if(ptr->previous!=NULL)
	{
		ptr->previous->next=ptr->next;
	}
	else
	{
		head=ptr->next;
	}

	if(ptr->next!=NULL)
	{
		ptr->next->previous=ptr->previous;
	}
	printf("Element deleted:\t%d\n",ptr->data);
	free(ptr);
	return;
}

void display()
{
	NODE *ptr=head;
	printf("The list as follows:\n");
	while(ptr!=NULL)
	{
		printf("%d\n",ptr->data);
		ptr=ptr->next;
	}
	return;
}

int main()
{
	while(1)
	{
		printf("Please choose from the given options:\n1. Insert\n2. Delete\n3. Display\n4. Exit\n");
		int select;
		scanf("%d",&select);
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
