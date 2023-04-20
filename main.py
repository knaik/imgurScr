import sys
import os
import random
import requests
import threading 
import time
from math import floor

total_operations = 0
total_download = 0
total_seconds = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15'
    }
otherErr = []
notFound = []
oth = []
count = 1

def scraper(urlChars, stop_event, urlSize):
    dir = "dlimages"
    count = 1
    global total_operations
    global total_download
    global total_seconds
    instStat = threading.local()
    instStat.num = nam.pop()
    instStat.count = 0
    #print(threading.current_thread().ident)
    #print(threading.current_thread(),str(urlSize))
    if not os.path.exists(dir):
        os.mkdir(dir)
    while not stop_event.is_set():
        try:  
            img = ''.join(random.choices(urlChars,k=urlSize)) 
            url = 'https://' + 'i.imgur.com' + '/' + img + '.jpg'  
            start_time = time.perf_counter()
            response = requests.head(url)            
            if response.status_code == 200: #assuming 404 not possible, avoiding redirects
                r = requests.get(url, headers=headers, stream=True, allow_redirects=False, timeout=200)
                instStat.count = instStat.count + 1
                if not (r.status_code == 302): #print('Valid[+]:'+img)                    
                    total_operations += 1
                    instName = threading.current_thread().ident
                    with open(os.path.join(dir, img)+".jpg", 'wb') as f:
                        for chunk in r.iter_content(2048):
                            f.write(chunk)
                        size = f.tell()//1000 #this conversion was wrong
                        if (size//1024>=1):
                            total_download = total_download + f.tell()
                            dlfloat = total_download/1000000
                            end_time = time.perf_counter()
                            elapsed_time = (end_time - start_time) * 1000 # convert to milliseconds
                            total_seconds =  elapsed_time + total_seconds
                            rate = float(8*(size/elapsed_time))
                            #totalrate = (dlfloat/elapsed_time)/1000
                            print((instStat.num+":").ljust(6),str(instStat.count).ljust(4)+str(total_operations).rjust(4),img.rjust(7),(str(size//1024)+"mb").rjust(7),str(int(floor(elapsed_time)))+"ms",str('%.3f'%rate)+"mbps",(total_download/1000000))
                        elif (f.tell() <= 1024):
                            total_download = total_download + f.tell()
                            dlfloat = total_download/1000000
                            end_time = time.perf_counter()
                            elapsed_time =  float((end_time - start_time) * 1000) # convert to milliseconds
                            total_seconds =  elapsed_time + total_seconds
                            rate = float(8*(size/elapsed_time))
                            #totalrate = (dlfloat/elapsed_time)/1000
                            print((instStat.num+":").ljust(6),str(instStat.count).ljust(4)+str(total_operations).rjust(4),img.rjust(7),(str(f.tell())+"bb").rjust(7),str(int(floor(elapsed_time)))+"ms",str('%.3f'%rate)+"mbps",(total_download/1000000))
                        else:
                            total_download = total_download + f.tell()
                            dlfloat = total_download/1000000
                            end_time = time.perf_counter()
                            elapsed_time = (end_time - start_time) * 1000 # convert to milliseconds
                            rate = float(8*(size/elapsed_time))
                            total_seconds =  elapsed_time + total_seconds
                            #totalrate = (dlfloat/elapsed_time)/1000
                            print((instStat.num+":").ljust(6),str(instStat.count).ljust(4)+str(total_operations).rjust(4),img.rjust(7),(str(size)+"kb").rjust(7),str(int(floor(elapsed_time)))+"ms",str('%.3f'%rate)+"mbps",(total_download/1000000)) # f.tell())
            elif (response.status_code == 302):                              
                otherErr.append(img)
            elif (response.status_code == 404):                              
                notFound.append(img)
            else:
                oth.append(img)
            end_time = time.perf_counter()
            elapsed_time = (end_time - start_time) * 1000 # convert to milliseconds
            #print("Elapsed time:", elapsed_time, "milliseconds")
            pass
        except requests.exceptions.HTTPError as err:
            stop_event.set()
            pass
            
#thr = int(input("how many threads? "))
urlChars = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
stop_event = threading.Event()
threads = []

nam = ["seven", "six", "five", "four", "three", "two", "one"]

st_time = time.process_time()

for i in [5,5,5,5,6,6,7]: #range(thr):
    # lgth = i%3 + 5 # urlSize
    t = threading.Thread(target=scraper, args=(urlChars, stop_event,i))
    t.start()
    threads.append(t)
try:
    while True:
        #print(st_time)
        pass
except KeyboardInterrupt:
    print("Program terminated by user.")
    stop_event.set()
    ed_time = time.process_time()
    print(ed_time)
    el_time = (ed_time - st_time) * 1000
    print(str(str(el_time)+"ms"))
    print(str(total_seconds//1000)+"s")
    print(total_download/1000000)
    #if (len(otherErr)):
        # print("302: ", len(otherErr))
    if (len(notFound)):
        print("404 ", len(notFound))
    if (len(oth)):
        print("other ", len(oth))


for t in threads:
    t.join()
    
    
    
 #def
 # img,size
 #function calcualte size print
 
# todo
# separate by real 5,6,7 url size instead of modulo
# clean up response handling
# extensions will be incorrect
# assuming redirection will be to "404"
# 26^5 = 11e6 , 26^6 = 308e6, 26^7 = 8e9 or 8000e6
# 62^5 = 916e6 ,62^6 = 56e9,  62^7 = 3e12
# filesize
# count termporarily inaccurate but overall accurate
#                             print("written ",img.rjust(7),(str(size//1024)+"mb").rjust(7),str(count).rjust(7),str(instName)+" inst",instNum,str(len(img)))
