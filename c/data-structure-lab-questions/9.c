/* Write a program to create a singly linked list that maintains a list of names in alphabetical order. Implement the following operations on the list.
a. Insert a new name
b. Delete a specified name */

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

typedef struct node
{
	char name[100];
	struct node *link;
} NODE; // Creates a alias to struct node

NODE *head=NULL;

void arrange(char *name)//Always accept it as pointer to the character array, as it will be regarded as the first element of the array, which is required to perform the operations.
{
	NODE *newnode=malloc(sizeof(NODE));
	strcpy(newnode->name,name);
	newnode->link=NULL;

	//if the name is greater than the first name at the list, or is the first name in the list, therefore head will point to first created pointer.
	if(head==NULL || strcmp(newnode->name,head->name)>0)
	{
		newnode->link=head;
		head=newnode;

		return;
	}

	NODE *ptr=head;
	//if the name is alphabetically smaller than first node.
	while(ptr!=NULL && strcmp(newnode->name,ptr->link->name)<0)
	{

		ptr=ptr->link;
	}

	newnode->link=ptr->link;
	ptr->link=newnode;

	return;
}

void delete(char *name)
{
	if(head==NULL)
	{
		printf("The linked list is empty.");
		return;
	}
	NODE *ptr=head;

	if(strcmp(head->name,name)==0)
	{
		ptr=head;
		head=head->link;
		free(ptr);

		return;
	}

	//if the node is other than the first node.

	while(ptr!=NULL && strcmp(ptr->link->name,name)!=0)
	{
		ptr=ptr->link;
	}
	if(strcmp(ptr->link->name,name)==0)
	{
		ptr->link=ptr->link->link;
		free(ptr->link);
	}
}

int main()
{
	//Infinite loop for switch case based inputting
	while(1)
	{
		printf("Please select from the following options:\n1. To insert a name\n2. To delete a name\n3. To display the list\n4. Exit\n");
		char name[100];
		int select;
		scanf("%d",&select);
		switch(select)
		{
			case 1:
				printf("Enter the number to be placed into the list:\t");
				scanf("%s",name);
				arrange(name);
				break;
			case 2:
				printf("Enter the name to be deleted from the list:\t");
				scanf("%s",name);
				delete(name);
				break;
			case 3:
				NODE *ptr=head;
				while(ptr!=NULL)
				{
					printf("%s\n",ptr->name);
					ptr=ptr->link;
				}
				break;
			case 4:
				exit(1);
				break;
			default:
				printf("Invalid input, try again.");
		}
	}
	return 0;
}
