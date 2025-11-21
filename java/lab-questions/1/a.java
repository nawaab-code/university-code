import java.util.Scanner;

public class a {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		double a, b, c;
		System.out.print("Enter coefficient a: ");
		a = sc.nextDouble();
		System.out.print("Enter coefficient b: ");
		b = sc.nextDouble();
		System.out.print("Enter coefficient c: ");
		c = sc.nextDouble();

		double discriminant = b * b - 4 * a * c;
		if (discriminant > 0) {
			double root1 = (-b + Math.sqrt(discriminant)) / (2 * a);
			double root2 = (-b - Math.sqrt(discriminant)) / (2 * a);
			System.out.println("Roots are real and different.");
			System.out.println("Root 1: " + root1);
			System.out.println("Root 2: " + root2);
		} else if (discriminant == 0) {
			double root = -b / (2 * a);
			System.out.println("Roots are real and same.");
			System.out.println("Root: " + root);
		} else {
			double realPart = -b / (2 * a);
			double imagPart = Math.sqrt(-discriminant) / (2 * a);
			System.out.println("Roots are complex and different.");
			System.out.println("Root 1: " + realPart + " + " + imagPart + "i");
			System.out.println("Root 2: " + realPart + " - " + imagPart + "i");
		}
		sc.close();
	}
}
