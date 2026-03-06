import socket
import cli, connection_manager, utils, message_manager



class Client():
        
	def __init__(self):
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connect_infos = ('', 0)
			self.connection_state = True
			self.bufsize = 1024
	def connect(self,address, port):
		self.connect_infos = (address, port)
		try:
			self.sock.connect(self.connect_infos)
		except socket.error as e:
			self.connection_state = False
			print("Erreur de connexion")
	def send(self, message):
		to_send = b''
		if not message:
			return None
		if message[0] == '-s' or message == '/health':
			to_send = utils.create_text_message(''.join(message[1::]),utils.BPC,True)
			self.sock.sendall(to_send)
		else:
			to_send = utils.create_text_message(''.join(message[0::]),utils.BPC)
			self.sock.sendall(to_send)
	def receive(self, timeout = 0.001):
			if self.connection_state == False:
				return None
			self.sock.settimeout(timeout)
			try:
				data = self.sock.recv(1024)
				if not data:
					print("[-] Connexion lost")
					self.close()
					return None
				else:
					return data
			except TimeoutError:
					return None
			except:
					print("[-] Connexion Closed")
					self.close()
					return None
	def close(self):
			self.sock.close()
			self.connection_state = False