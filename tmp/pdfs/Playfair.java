import java.util.*; 
import java.io.*; 
class Playfair { 
    static char[][] m = new char[5][5]; 
    static void makeMatrix(String key) { 
        boolean[] u = new boolean[26]; 
        String s = ""; 
        key = key.toUpperCase().replaceAll("[^A-Z]", "").replace('J', 'I'); 
        for (char c : (key + 
"ABCDEFGHIKLMNOPQRSTUVWXYZ").toCharArray()) 
            if (!u[c - 'A']) { 
                s += c; 
                u[c - 'A'] = true; 
            } 
        for (int i = 0, k = 0; i < 5; i++) 
            for (int j = 0; j < 5; j++) 
                m[i][j] = s.charAt(k++); 
    } 
    static int[] pos(char c) { 
        if (c == 'J') c = 'I'; 
        for (int i = 0; i < 5; i++) 
            for (int j = 0; j < 5; j++) 
                if (m[i][j] == c) return new int[]{i, j}; 
        return null; 
    } 
    static String prepare(String s) { 
        s = s.toUpperCase().replaceAll("[^A-Z]", "").replace('J', 'I'); 
        String r = ""; 
        for (int i = 0; i < s.length();) { 
            char a = s.charAt(i++); 
            char b = i < s.length() ? s.charAt(i) : 'X'; 
            if (a == b) r += a + "X"; 
            else { r += a + "" + b; i++; } 
        } 
        return r; 
    } 
    static String process(String s, boolean enc) { 
        String r = ""; 
        for (int i = 0; i < s.length(); i += 2) { 
            char x = s.charAt(i), y = s.charAt(i + 1); 
            int[] a = pos(x), b = pos(y); 
            int d = enc ? 1 : 4; 
            if (a[0] == b[0]) 
                r += m[a[0]][(a[1] + d) % 5] + "" + 
                     m[b[0]][(b[1] + d) % 5]; 
            else if (a[1] == b[1]) 
                r += m[(a[0] + d) % 5][a[1]] + "" + 
                     m[(b[0] + d) % 5][b[1]]; 
            else 
                r += m[a[0]][b[1]] + "" + m[b[0]][a[1]]; 
        } 
        return r; 
    } 
    static void showMatrix() { 
        System.out.println("\nPlayfair Matrix:"); 
        for (char[] r : m) System.out.println(Arrays.toString(r)); 
    } 
    static String fileRead(String f) throws Exception { 
        return new String(java.nio.file.Files.readAllBytes( 
                java.nio.file.Paths.get(f))); 
    } 
    static void fileWrite(String f, String s) throws Exception { 
        java.nio.file.Files.write(java.nio.file.Paths.get(f), s.getBytes()); 
    } 
    public static void main(String[] args) throws Exception { 
        Scanner sc = new Scanner(System.in); 
        System.out.print("Enter key: "); 
        makeMatrix(sc.nextLine()); 
        showMatrix(); 
        while (true) { 
            System.out.println("\n1. Encrypt"); 
            System.out.println("2. Decrypt"); 
            System.out.println("3. Encrypt from file"); 
            System.out.println("4. Decrypt from file"); 
            System.out.println("5. Exit"); 
            System.out.print("Enter choice: "); 
            int ch = sc.nextInt(); 
            sc.nextLine(); 
            if (ch == 5) break; 
            String s, p, r, in, out; 
            if (ch == 3 || ch == 4) { 
                System.out.print("Input file: "); 
                in = sc.nextLine(); 
                System.out.print("Output file: "); 
                out = sc.nextLine(); 
                s = fileRead(in); 
            } else { 
                System.out.print("Enter text: "); 
                s = sc.nextLine(); 
                out = ""; 
            } 
            if (ch == 1 || ch == 3) { 
                p = prepare(s); 
                System.out.println("Digraph Pairs: " + 
                        p.replaceAll("(?<=\\G..)(?!$)", " ")); 
                r = process(p, true); 
                System.out.println("Ciphertext: " + r); 
            } else if (ch == 2 || ch == 4) { 
                p = s.toUpperCase().replaceAll("[^A-Z]", "").replace('J', 'I'); 
                System.out.println("Digraph Pairs: " + 
                        p.replaceAll("(?<=\\G..)(?!$)", " ")); 
                r = process(p, false); 
                System.out.println("Plaintext: " + r); 
            } else { 
                System.out.println("Invalid choice"); 
                continue; 
            } 
            if (!out.isEmpty()) { 
                fileWrite(out, r); 
                System.out.println("Output saved to " + out); 
            } 
        } 
        sc.close(); 
    } 
} 