/* A Call center phone system has to hold the phone calls from customers and provide service based on the arrival time of the calls.
Write a C program to simulate this system using appropriate data structure.
Program should have options to add and remove the phone calls in appropriate order for their service. */

//The calls will be identified by assigning each of them a id.

#include<stdio.h>
#include<stdlib.h>

typedef struct node
{
	int id;
	struct node *link;
}

NODE *head;

void accept(int id)// To add a call to the queue.
{
	NODE *newnode=malloc(sizeof(NODE));

	if(newnode==NULL)
	{
		printf("Queue is full, please dequeue first, to accept new calls.");
	}

	if(head->link=
