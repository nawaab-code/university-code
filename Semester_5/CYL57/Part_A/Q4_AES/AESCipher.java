import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.Scanner;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;

public class AESCipher {
    public static void main(String[] args) throws Exception {
        System.out.print("Message: ");
        String text = new Scanner(System.in).nextLine();
        KeyGenerator generator = KeyGenerator.getInstance("AES");
        generator.init(128);
        SecretKey key = generator.generateKey();
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        byte[] iv = cipher.getIV();
        byte[] encrypted = cipher.doFinal(text.getBytes(StandardCharsets.UTF_8));
        System.out.println("IV: " + Base64.getEncoder().encodeToString(iv));
        System.out.println("Encrypted: " + Base64.getEncoder().encodeToString(encrypted));
        cipher.init(Cipher.DECRYPT_MODE, key, new GCMParameterSpec(128, iv));
        System.out.println("Decrypted: " + new String(cipher.doFinal(encrypted), StandardCharsets.UTF_8));
    }
}
