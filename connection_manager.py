import socket

ADDRESS = 'vlbelintrocrypto.hevs.ch'
PORT = 6000

class client():
        
        def __init__(self):
             self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        def connect(self,address, port):
            try:
                self.sock.connect((address, port))
            except:
                print("Erreur de connexion")
        def send(self, message):
             pass
        def receive(self):
             pass
        def close(self):
             self.sock.close
             return False
        