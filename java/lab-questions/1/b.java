import java.util.Scanner;

public class b {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		int n;
		System.out.print("Enter the size of arrays: ");
		n = sc.nextInt();
		int[] arr1 = new int[n];
		int[] arr2 = new int[n];
		int[] result = new int[n];

		System.out.println("Enter elements of first array:");
		for(int i = 0; i < n; i++) {
			arr1[i] = sc.nextInt();
		}

		System.out.println("Enter elements of second array:");
		for(int i = 0; i < n; i++) {
			arr2[i] = sc.nextInt();
		}

		for(int i = 0; i < n; i++) {
			result[i] = arr1[i] * arr2[i];
		}

		System.out.println("Resultant array after multiplication:");
		for(int i = 0; i < n; i++) {
			System.out.print(result[i] + " ");
		}
		System.out.println();
		sc.close();
	}
}
