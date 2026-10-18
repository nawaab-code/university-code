import java.util.Scanner;

public class CaesarCipher {
    static String shift(String text, int key) {
        StringBuilder result = new StringBuilder();
        key = Math.floorMod(key, 26);
        for (char c : text.toCharArray()) {
            char base = c >= 'A' && c <= 'Z' ? 'A' : 'a';
            if (c >= 'A' && c <= 'Z' || c >= 'a' && c <= 'z')
                c = (char) (base + (c - base + key) % 26);
            result.append(c);
        }
        return result.toString();
    }

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Message: ");
        String text = input.nextLine();
        System.out.print("Shift: ");
        int key = Math.floorMod(Integer.parseInt(input.nextLine()), 26);
        String encrypted = shift(text, key);
        System.out.println("Encrypted: " + encrypted);
        System.out.println("Decrypted: " + shift(encrypted, -key));
    }
}
