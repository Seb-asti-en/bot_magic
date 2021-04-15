import socket
import pickle


class Network:
	def __init__(self, host = 'localhost', port = 5000):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.host = host
		#self.port = port
		self.__addr = (host, port)
		#self.__size = size
		
	def connect(self):
		try:
			self.client.connect(self.__addr)
		except:
			pass

	def send(self, data):
		try:
			self.client.send(pickle.dumps(data))
			#return pickle.loads(self.client.recv(4096))
		except socket.error as e:
			print(e)

	def recv(self, size = 4096):
		return self.client.recv(size)
