#include <stdio.h>
#include <string.h>

#define MAX_NAMES 100
#define MAX_LEN 100

void bubbleSort(char names[][MAX_LEN], int n) {
    int i, j;
    char temp[MAX_LEN];
    int swapped;

    for (i = 0; i < n - 1; i++) {
        swapped = 0;
        for (j = 0; j < n - i - 1; j++) {
            if (strcmp(names[j], names[j + 1]) > 0) {
                strcpy(temp, names[j]);
                strcpy(names[j], names[j + 1]);
                strcpy(names[j + 1], temp);
                swapped = 1;
            }
        }
        if (!swapped)   // Optimization for best case
            break;
    }
}

int main() {
    int n, i;
    char names[MAX_NAMES][MAX_LEN];

    printf("Enter number of names: ");
    scanf("%d", &n);

    printf("Enter names:\n");
    for (i = 0; i < n; i++) {
        scanf("%s", names[i]);
    }

    bubbleSort(names, n);

    printf("\nNames in alphabetical order:\n");
    for (i = 0; i < n; i++) {
        printf("%s\n", names[i]);
    }

    return 0;
}
