#include <stdio.h>

#define MAX 100

void insertionSort(long long arr[], int n) {
    int i, j;
    long long key;

    for (i = 1; i < n; i++) {
        key = arr[i];
        j = i - 1;

        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}

int main() {
    int n, i;
    long long phone[MAX];

    printf("Enter number of telephone numbers: ");
    scanf("%d", &n);

    printf("Enter telephone numbers:\n");
    for (i = 0; i < n; i++) {
        scanf("%lld", &phone[i]);
    }

    insertionSort(phone, n);

    printf("\nTelephone numbers in ascending order:\n");
    for (i = 0; i < n; i++) {
        printf("%lld\n", phone[i]);
    }

    return 0;
}
