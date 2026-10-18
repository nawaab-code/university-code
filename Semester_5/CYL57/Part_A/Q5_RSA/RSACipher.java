import java.nio.charset.StandardCharsets;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.spec.MGF1ParameterSpec;
import java.util.Base64;
import java.util.Scanner;
import javax.crypto.Cipher;
import javax.crypto.spec.OAEPParameterSpec;
import javax.crypto.spec.PSource;

public class RSACipher {
    public static void main(String[] args) throws Exception {
        System.out.print("Message (at most 190 UTF-8 bytes): ");
        byte[] text = new Scanner(System.in).nextLine().getBytes(StandardCharsets.UTF_8);
        if (text.length > 190) {
            System.out.println("Message too long: use at most 190 UTF-8 bytes.");
            return;
        }
        KeyPairGenerator generator = KeyPairGenerator.getInstance("RSA");
        generator.initialize(2048);
        KeyPair keys = generator.generateKeyPair();
        Cipher cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding");
        OAEPParameterSpec padding = new OAEPParameterSpec("SHA-256", "MGF1",
                MGF1ParameterSpec.SHA256, PSource.PSpecified.DEFAULT);
        cipher.init(Cipher.ENCRYPT_MODE, keys.getPublic(), padding);
        byte[] encrypted = cipher.doFinal(text);
        System.out.println("Public key (X.509): " + Base64.getEncoder().encodeToString(keys.getPublic().getEncoded()));
        System.out.println("Encrypted: " + Base64.getEncoder().encodeToString(encrypted));
        cipher.init(Cipher.DECRYPT_MODE, keys.getPrivate(), padding);
        System.out.println("Decrypted: " + new String(cipher.doFinal(encrypted), StandardCharsets.UTF_8));
    }
}
