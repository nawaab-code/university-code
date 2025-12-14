//Traversing through a linked list.
#include<stdio.h>
#include<stdlib.h>

struct node
{
	int data;
	struct node *link;
};

int CountNodes(struct node *head)
{
	if(head==NULL)//Checking if the linked is empty.
	{
		printf("The linked list is empty");
		return 0;
	}

	struct node *temp=head;
	int count=0;
	while(temp!=NULL)
	{
		count++;
		temp=temp->link;
	}
	printf("Number of nodes: %d",count);

	return 0;
}

int main()
{
	struct node *head=malloc(sizeof(struct node));
	head->data=1;
	head->link=NULL;

	struct node *current=malloc(sizeof(struct node));
	current->data=2;
	current->link=NULL;

	head->link=current;//Creating a link betweeen node 1 and node 2.

	current=malloc(sizeof(struct node));
	current->data=3;
	current->link=NULL;
	head->link->link=current;//Creating a chain by connecting node 2 and node 3.

	CountNodes(head);

	return 0;
}
