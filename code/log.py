#!/usr/bin/env python3

import time
import datetime

class Log:
	
	def __init__(self):
		self.__log_file = None

	def start(self, port):
		try:
			self.__log_file = open(self.filename(port), "w+")
		except:
			print("error")

	def filename(self, port):
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%d%m%y_%Hh%M')
		return (f"logs/game{port}_{st}.txt")
	
	def write(self, text):
		self.__log_file.write(f"{text}\n")
		print(text)
		

def main():
	log = Log()
	log.start()
	log.write("test_add_log")


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print ('Interrupted')
		sys.exit(0)
