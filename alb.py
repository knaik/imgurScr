import sys
import os
import random
import requests
import threading 

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15'
    }
otherErr = []
notFound = []
oth = []
def scraper(urlChars, stop_event, urlSize):
    dir = "dlimages"
    if not os.path.exists(dir):
        os.mkdir(dir)
    while not stop_event.is_set():
        try:  
            img = ''.join(random.choices(urlChars,k=urlSize)) 
            url = 'https://' + 'imgur.com' + '/a' + '/'+ img  
            response = requests.head(url)            
            if response.status_code == 200: #assuming 404 not possible, avoiding redirects
                count = count + 1
                
                r = requests.get(url, headers=headers, stream=True, allow_redirects=False, timeout=20)
                if not (r.status_code == 302): #print('Valid[+]:'+img)
                    print(url)
            elif (response.status_code == 302):                              
                otherErr.append(img)
            elif (response.status_code == 404):                              
                notFound.append(img)
            else:
                oth.append(img)
            pass
        except requests.exceptions.HTTPError as err:
            stop_event.set()
            pass
            
#thr = int(input("how many threads? "))
urlChars = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
stop_event = threading.Event()
threads = []

count=0
for i in [5,5,5,5,6,6,7,7]: #range(thr):
    # lgth = i%3 + 5 # urlSize
    t = threading.Thread(target=scraper, args=(urlChars, stop_event,i))
    t.start()
    threads.append(t)
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Program terminated by user.")
    stop_event.set()
    if (len(otherErr)):
        print("302: ", len(otherErr))
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