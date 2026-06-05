// Write a c program to find the limits of number of clock cycles.
#include<stdio.h>
#include<unistd.h>
#include<limits.h>

int main()
{
	long tick,max_child,max_path,max_file_name,max_process;
	
	tick = sysconf(_SC_CLK_TCK);
	max_child = sysconf(_SC_CHILD_MAX);
	max_path = pathconf("/",_PC_PATH_MAX);
	max_file_name = pathconf("/",_PC_NAME_MAX);
	max_process = sysconf(_SC_OPEN_MAX);
	
	
	printf("Total ticks per sec: %ld\n",tick);
	printf("Max child: %ld\n",max_child);
	printf("Max path size: %ld\n",max_path);
	printf("Max file name : %ld\n",max_file_name);
	printf("Max proccess: %ld\n",max_process);
	return 0;
}
