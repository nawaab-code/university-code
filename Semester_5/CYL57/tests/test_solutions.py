"""Run from CYL57: python -m unittest discover -s tests -v.

No external hosts, live packet sending, firewall changes, or browser automation.
Java tools, OpenSSL, and Scapy must be installed; missing dependencies fail clearly.
"""
import base64
import http.server
from pathlib import Path
import ssl
import subprocess
import sys
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[1]


def run(command, **kwargs):
    return subprocess.run(command, text=True, capture_output=True, timeout=30, **kwargs)


class JavaSolutions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.classes = {}
        for source in sorted((ROOT / 'Part_A').glob('*/*.java')):
            output = Path(cls.temp.name) / source.stem
            output.mkdir()
            result = run(['javac', '--release', '11', '-d', str(output), str(source)])
            if result.returncode:
                raise AssertionError(result.stderr)
            cls.classes[source.stem] = output

    def execute(self, name, data):
        result = run(['java', '-cp', str(self.classes[name]), name], input=data)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_caesar_known_vector(self):
        output = self.execute('CaesarCipher', 'Attack at dawn!\n3\n')
        self.assertIn('Encrypted: Dwwdfn dw gdzq!', output)
        self.assertIn('Decrypted: Attack at dawn!', output)

    def test_caesar_negative_large_zero_and_extreme_shifts(self):
        for key, expected in [(-1, 'Zab Wxy! 123'), (29, 'Def Abc! 123'),
                              (0, 'Abc Xyz! 123'), (-2147483648, 'Cde Zab! 123')]:
            with self.subTest(key=key):
                output = self.execute('CaesarCipher', f'Abc Xyz! 123\n{key}\n')
                self.assertIn('Encrypted: ' + expected, output)
                self.assertIn('Decrypted: Abc Xyz! 123', output)

    def test_caesar_preserves_non_english(self):
        output = self.execute('CaesarCipher', 'Café नमस्ते\n1\n')
        self.assertIn('Encrypted: Dbgé नमस्ते', output)
        self.assertIn('Decrypted: Café नमस्ते', output)

    def test_playfair_monarchy_vector(self):
        output = self.execute('PlayfairCipher', 'MONARCHY\nINSTRUMENTS\n')
        self.assertIn('Prepared: INSTRUMENTSX', output)
        self.assertIn('Encrypted: GATLMZCLRQXA', output)

    def test_playfair_classic_vector(self):
        output = self.execute('PlayfairCipher', 'PLAYFAIR EXAMPLE\nHIDE THE GOLD IN THE TREE STUMP\n')
        self.assertIn('Encrypted: BMODZBXDNABEKUDMUIXMMOUVIF', output)

    def test_playfair_repeated_letters(self):
        for text, pairs in [('BALLOON', 'BALXLOON'), ('XX', 'XQXQ'), ('X', 'XQ'),
                            ('Jig!', 'IXIG'), ('123!', '')]:
            with self.subTest(text=text):
                output = self.execute('PlayfairCipher', f'MONARCHY\n{text}\n')
                self.assertIn('Prepared: ' + pairs + '\n', output)

    def test_playfair_default_alphabet(self):
        output = self.execute('PlayfairCipher', '\nAB\n')
        self.assertIn('ABCDE\nFGHIK\nLMNOP\nQRSTU\nVWXYZ', output)
        self.assertIn('Encrypted: BC', output)

    def test_des_and_aes_roundtrips(self):
        for name in ['DESCipher', 'AESCipher']:
            for message in ['', 'Hello crypto', 'नमस्ते café 🔐', 'a' * 257]:
                with self.subTest(name=name, message=message):
                    output = self.execute(name, message + '\n')
                    self.assertIn('Decrypted: ' + message + '\n', output)
                    encrypted = output.split('Encrypted: ', 1)[1].splitlines()[0]
                    data = base64.b64decode(encrypted, validate=True)
                    iv = base64.b64decode(output.split('IV: ', 1)[1].splitlines()[0], validate=True)
                    if name == 'DESCipher':
                        self.assertEqual(len(iv), 8)
                        self.assertEqual(len(data) % 8, 0)
                    else:
                        self.assertEqual(len(iv), 12)
                        self.assertEqual(len(data), len(message.encode()) + 16)

    def test_crypto_randomness(self):
        for name in ['DESCipher', 'AESCipher', 'RSACipher']:
            with self.subTest(name=name):
                a = self.execute(name, 'same message\n').split('Encrypted: ')[1].splitlines()[0]
                b = self.execute(name, 'same message\n').split('Encrypted: ')[1].splitlines()[0]
                self.assertNotEqual(a, b)

    def test_rsa_roundtrip_and_boundary(self):
        for message in ['', 'Hello RSA', 'é' * 95]:
            with self.subTest(message=message):
                output = self.execute('RSACipher', message + '\n')
                self.assertIn('Decrypted: ' + message + '\n', output)
                encrypted = output.split('Encrypted: ', 1)[1].splitlines()[0]
                self.assertEqual(len(base64.b64decode(encrypted, validate=True)), 256)

    def test_rsa_rejects_oversized_utf8(self):
        for message in ['a' * 191, 'é' * 96]:
            self.assertIn('Message too long', self.execute('RSACipher', message + '\n'))


class PacketSolutions(unittest.TestCase):
    def test_three_constructed_probes(self):
        from scapy.all import ICMP, IP, TCP, UDP, Raw, rdpcap
        with tempfile.TemporaryDirectory() as directory:
            result = run([sys.executable, str(ROOT / 'Part_B/Q4_Packet_Crafting/packets.py')], cwd=directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            packets = rdpcap(str(Path(directory) / 'probes.pcap'))
            self.assertEqual(len(packets), 3)
            self.assertTrue(all(p[IP].dst == '10.57.1.2' for p in packets))
            self.assertEqual(packets[0][TCP].dport, 8080)
            self.assertEqual(str(packets[0][TCP].flags), 'S')
            self.assertEqual(packets[1][UDP].dport, 9999)
            self.assertEqual(bytes(packets[1][Raw]), b'CYL57')
            self.assertEqual(packets[2][ICMP].type, 8)

    def test_public_probe_target_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run([sys.executable, str(ROOT / 'Part_B/Q4_Packet_Crafting/packets.py'), '8.8.8.8'], cwd=directory)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('private IPv4', result.stderr)
            self.assertFalse((Path(directory) / 'probes.pcap').exists())

    def test_arp_conflicting_claim_and_restoration(self):
        from scapy.all import ARP, Ether, rdpcap
        with tempfile.TemporaryDirectory() as directory:
            result = run([sys.executable, str(ROOT / 'Part_B/Q5_ARP_Spoofing/arp_demo.py')], cwd=directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            packets = rdpcap(str(Path(directory) / 'arp-demo.pcap'))
            self.assertEqual(len(packets), 5)
            self.assertTrue(all(p[ARP].op == 2 for p in packets))
            self.assertEqual(packets[0][ARP].psrc, packets[1][ARP].psrc)
            self.assertEqual(packets[0][ARP].hwsrc, '02:00:00:57:00:01')
            self.assertEqual(packets[1][ARP].hwsrc, '02:00:00:57:00:03')
            self.assertEqual(packets[1][Ether].dst, '02:00:00:57:00:02')
            self.assertEqual(packets[2][ARP].psrc, '10.57.0.2')
            self.assertEqual(packets[3][ARP].hwsrc, packets[0][ARP].hwsrc)
            self.assertEqual(packets[4][ARP].hwsrc, '02:00:00:57:00:02')


class TLSClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.folder = Path(cls.temp.name)
        cls.cert, cls.key = cls.folder / 'server.crt', cls.folder / 'server.key'
        result = run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes',
                      '-keyout', str(cls.key), '-out', str(cls.cert), '-days', '1',
                      '-subj', '/CN=localhost', '-addext', 'subjectAltName=DNS:localhost'])
        if result.returncode:
            raise AssertionError(result.stderr)
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'CYL57 local HTTPS test')
            def log_message(self, *args):
                pass
        cls.server = http.server.HTTPServer(('127.0.0.1', 0), Handler)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cls.cert, cls.key)
        cls.server.socket = context.wrap_socket(cls.server.socket, server_side=True)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.addClassCleanup(cls.server.server_close)
        cls.addClassCleanup(cls.thread.join, 5)
        cls.addClassCleanup(cls.server.shutdown)

    def client(self, *extra):
        return run([sys.executable, str(ROOT / 'Part_B/Q1_TLS_Handshake/tls_client.py'),
                    'localhost', '--port', str(self.server.server_port), *extra], cwd=self.folder)

    def test_trusted_local_tls_request_and_key_logging(self):
        result = self.client('--cafile', str(self.cert))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Version: TLS', result.stdout)
        self.assertIn('Status: HTTP/1.0 200 OK', result.stdout)
        keys = (self.folder / 'session.keys').read_text()
        self.assertTrue('TRAFFIC_SECRET' in keys or 'CLIENT_RANDOM' in keys)

    def test_untrusted_certificate_rejected(self):
        result = self.client()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('CERTIFICATE_VERIFY_FAILED', result.stderr)


class FilesAndScripts(unittest.TestCase):
    def test_every_question_has_readme_and_source(self):
        folders = sorted((ROOT / 'Part_A').glob('Q*')) + sorted((ROOT / 'Part_B').glob('Q*'))
        self.assertEqual(len(folders), 10)
        for folder in folders:
            with self.subTest(folder=folder.name):
                text = (folder / 'README.md').read_text()
                for heading in ['## 1. Question', '## 2. Brief explanation',
                                '## 3. Extensive explanation', '## 4. How to operate/run the files']:
                    self.assertIn(heading, text)
                self.assertTrue(any(p.suffix in ['.java', '.py', '.sh', '.js'] for p in folder.iterdir()))

    def test_shell_script_syntax(self):
        for script in (ROOT / 'Part_B').glob('*/*.sh'):
            with self.subTest(script=script.name):
                result = run(['bash', '-n', str(script)])
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_python_syntax(self):
        for script in (ROOT / 'Part_B').glob('*/*.py'):
            compile(script.read_text(), str(script), 'exec')


if __name__ == '__main__':
    unittest.main()
