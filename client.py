import socket
import time
from threading import Thread
from collections import deque
from select import select

tasks = deque()
stopped = {}

def run_queries():
	while any([tasks, stopped]):
		while not tasks:
			ready_to_read, _, _ = select(stopped,[], [])
			for r in ready_to_read:
				tasks.append(stopped.pop(r))
					
		while tasks:
			task = tasks.popleft()
			try:
				sock = next(task)
				stopped[sock] = task
			except StopIteration:
				print("query done")

def make_request():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("localhost", 8000))
	sock.send(b"GET /\n\n")
	
	yield sock
	
	resp = sock.recv(100)
	sock.close()
	
def run_queries_produser():	
	while True:
		tasks.append(make_request())
		time.sleep(1.0)

t1 = Thread(target = run_queries_produser)

t1.start()
