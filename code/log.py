#!/usr/bin/env python3

import time
import datetime

class Log:
	
	def __init__(self):
		self.__log_file = None

	def start(self):
		try:
			f = open(self.filename(), "x")
			f.close()
			self.__log_file = open(self.filename(), "a")
		except:
			print("error")

	def filename(self):
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
		return (f"logs/logfile_{st}.log")
	
	def add_log(self, text):
		self.__log_file.write(text)
		

def main():
	log = Log()
	log.start()
	log.add_log("test_add_log")


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print ('Interrupted')
		sys.exit(0)
