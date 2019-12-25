import re, requests
from md5 import md5

USER = 'admin'
PASS = '' #default is blank for new routers
IP = '192.168.1.1'

browser = requests.Session()
browser.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
#browser.proxies = {"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"} #uncomment to use proxy

#get md5 salt
res = browser.get('http://' + IP + '/login')
regex = re.search('hexMD5\(\'(.+?)\' \+ document.login.password.value \+ \'(.+?)\'\);', res.text)

#if found salt, do login
if regex :
  payload = {'username':USER, 'password':hex_hash_password, 'dst':'', 'popup':'true'}
  res = browser.post('http://' + IP + '/login', data=payload) #send data to /login
  hex_hash_password = md5( regex.group(1).decode('string_escape') + PASS + regex.group(2).decode('string_escape') ).hexdigest()
  print ('hexMD5' + regex.group(1) + PASS + regex.group(2) + ') => ' + hex_hash_password
  # do something
  #print res.text
