from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import threading



class _Client(WebSocket):
	def handleMessage(self):
		thr=threading.Thread(target=self.process_message,args=(),kwargs={})
		thr.deamon=True
		thr.start()
	def handleConnected(self):
		self.WS.on_client_connect(self)
	def handleClose(self):
		self.WS.on_client_close(self)
	def process_message(self,*args):
		msg=self.data
		self.sendMessage("null")
		r=self.WS._p(msg)
		if (r!="null"):
			self.sendMessage(r)
	def send_message(self,m):
		self.sendMessage(m)



class _BaseWS(SimpleWebSocketServer):
	def _constructWebSocket(self,s,a):
		c=self.websocketclass(self,s,a)
		c.WS=self.WS
		c.ID=self.WS._n_id()
		return c
class WS:
	def __init__(self,a):
		self._s=_BaseWS(a[0],a[1],_Client)
		self._s.WS=self
		self._a=a
		self.packets={}
		self._s_thr=None
		self._c_id=0
	def start(self):
		print("WS (addr: "+self._a[0]+" port: "+self._a[1]+")")
		def f():
			self._s.serveforever()
		self._s_thr=threading.Thread(target=f,args=(),kwargs={})
		self._s_thr.start()
	def _p(self,m):
		k=m.split(":")[0]
		v=m[len(k)+1:]
		if (k not in self.packets.keys()):
			self.on_error("Invalid packet!")
			return "null"
		return self.packets[k](v)
	def _n_id(self):
		self._c_id+=1
		return self._c_id-1



	def on_client_connect(self,c):
		pass
	def on_client_close(self,c):
		pass
	def on_error(self,e):
		print(e)
		self._s.close()



	def packets(self):
		return self.packets
	def add_packet(self,k,f):
		self.packets[k]=f



	def clients(self):
		c=[]
		for cl in self._s.connections.items():
			c.apend(cl[1])
		return c
	def get_client(self,id_):
		for c in self.clients():
			if (c.ID==id_):return c
		return None
