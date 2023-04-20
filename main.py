import sys
import os
import random
import requests
import threading 


def scraper(urlChars, stop_event, urlSize):
    dir = "dlimages"
    if not os.path.exists(dir):
        os.mkdir(dir)
    while not stop_event.is_set():
        try:  
            img = ''.join(random.choices(urlChars,k=urlSize)) 
            url = 'https://' + 'i.imgur.com' + '/' + img + '.jpg'  
            response = requests.head(url)            
            if response.status_code == 200: #assuming 404 not possible, avoiding redirects
                r = requests.get(url, stream=True, allow_redirects=False)
                if not (r.status_code == 302): #print('Valid[+]:'+img)
                    with open(os.path.join(dir, img)+".jpg", 'wb') as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
                        print("written ",img,f.tell())
                # else: #print('notvalid[-]:'+img)
            else:                              
                print(response, url)                
            pass
        except requests.exceptions.HTTPError as err:
            print('NOT valid[-]:'+url)
            pass
            
thr = int(input("how many threads? "))
urlChars = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
stop_event = threading.Event()
threads = []

for i in range(thr):
    lgth = i%3 + 5 # urlSize
    t = threading.Thread(target=scraper, args=(urlChars, stop_event,lgth))
    t.start()
    threads.append(t)
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Program terminated by user.")
    stop_event.set()

for t in threads:
    t.join()
    
# todo
# separate by real 5,6,7 url size instead of modulo
# clean up response handling
# extensions will be incorrect
# assuming redirection will be to "404"
# 26^5 = 11e6 , 26^6 = 308e6, 26^7 = 8e9 or 8000e6
# 62^5 = 916e6 ,62^6 = 56e9,  62^7 = 3e12
# filesize