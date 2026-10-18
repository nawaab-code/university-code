import java.util.Scanner;

public class PlayfairCipher {
    static String letters(String text) {
        return text.toUpperCase(java.util.Locale.ROOT).replaceAll("[^A-Z]", "").replace('J', 'I');
    }

    static String square(String key) {
        String result = "";
        for (char c : (letters(key) + "ABCDEFGHIKLMNOPQRSTUVWXYZ").toCharArray())
            if (result.indexOf(c) < 0) result += c;
        return result;
    }

    static String prepare(String text) {
        text = letters(text);
        String result = "";
        for (int i = 0; i < text.length();) {
            char a = text.charAt(i++);
            char filler = a == 'X' ? 'Q' : 'X';
            char b = i == text.length() || text.charAt(i) == a ? filler : text.charAt(i++);
            result += "" + a + b;
        }
        return result;
    }

    static String encrypt(String pairs, String grid) {
        String result = "";
        for (int i = 0; i < pairs.length(); i += 2) {
            int a = grid.indexOf(pairs.charAt(i)), b = grid.indexOf(pairs.charAt(i + 1));
            int r1 = a / 5, c1 = a % 5, r2 = b / 5, c2 = b % 5;
            if (r1 == r2) { c1 = (c1 + 1) % 5; c2 = (c2 + 1) % 5; }
            else if (c1 == c2) { r1 = (r1 + 1) % 5; r2 = (r2 + 1) % 5; }
            else { int temp = c1; c1 = c2; c2 = temp; }
            result += "" + grid.charAt(5 * r1 + c1) + grid.charAt(5 * r2 + c2);
        }
        return result;
    }

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Key: ");
        String grid = square(input.nextLine());
        System.out.print("Message: ");
        String pairs = prepare(input.nextLine());
        System.out.println("Matrix:");
        for (int i = 0; i < 25; i += 5) System.out.println(grid.substring(i, i + 5));
        System.out.println("Prepared: " + pairs);
        System.out.println("Encrypted: " + encrypt(pairs, grid));
    }
}
