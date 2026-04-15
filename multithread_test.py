import threading
import time

def count(x):
    for i in range(10):
        print(x*i)
        time.sleep(1)

def count2(x):
    for i in range(100,110):
        print(x*i)
        time.sleep(1)

things = [1,2]

threads = []

for num in things:
    t = threading.Thread(target=count,args=(num,))
    threads.append(t)

t = threading.Thread(target=count2,args=(100,))
threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()