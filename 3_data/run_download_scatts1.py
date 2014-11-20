import urllib,urllib2
from bs4 import BeautifulSoup
import os, time

url = 'http://ematch.scatt.com/download/'
file_name_source = 'ematch_web.txt'
out_folder = 'ematch/'

time_delay_sec = 1

file(file_name_source, "w").write(urllib2.urlopen(url).read())


conn = urllib2.urlopen(url)
html = conn.read()

soup = BeautifulSoup(html)
links = soup.find_all('a')

#for tag in links:
#	link = tag.get('href',None)
#	if link != None:
#		print link

if not os.path.exists(out_folder):
	os.mkdir(out_folder)

#for sk in range(5,len(links)+1):
for sk in range(5,len(links)):
	link = links[sk].get('href',None)
	if link != None:
		print sk,link
		urllib.urlretrieve(url+link, out_folder+link)
		time.sleep(time_delay_sec)