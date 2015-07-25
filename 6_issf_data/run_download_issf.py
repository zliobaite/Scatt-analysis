import urllib,urllib2
from bs4 import BeautifulSoup
import os, time
import dateutil.parser as dparser

url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1692&resultkey=Q00000_I_1104150900.1.AR40.0'
url_master = 'http://www.issf-sports.org'
file_name_source = 'issf_web.txt'
out_folder = 'issf/'

time_delay_sec = 1

string_result = '/pages/resulttargets.ashx?reskey='
string_series = '/pages/resulttargetdetails.ashx?srid='

file(file_name_source, "w").write(urllib2.urlopen(url).read())

conn = urllib2.urlopen(url)
html = conn.read()

soup = BeautifulSoup(html)
links = soup.find_all('a')

print '-----'
for ln in soup.find_all(class_="row5"):
	d = ln.text
print d
dd = dparser.parse(d,fuzzy=True)
print dd
print dd.date()
if (soup.title.text.find('Women')>-1):
	file_name = str(dd.date())+'W.csv'
else:
	file_name = str(dd.date())+'M.csv'
print file_name
print '-----'

#for tag in links:
#	link = tag.get('href',None)
#	if link != None:
#		print link

if not os.path.exists(out_folder):
	os.mkdir(out_folder)

#http://www.issf-sports.org/athletes/athlete.ashx?personissfid=SHCROW1307198201
result_links = []

#for sk in range(5,len(links)+1):
for sk in range(38,44):#0,len(links)):
	link = links[sk].get('href',None)
	if link != None:
		print sk,link
		if (link.find(string_result)>-1):
			result_links.append(link)
		#urllib.urlretrieve(url+link, out_folder+link)
		time.sleep(time_delay_sec)

result_links = list(set(result_links))
print(result_links)

for sk in range(1,2):
	print('---')
	result_url_now = url_master+result_links[sk]
	conn = urllib2.urlopen(result_url_now)
	html = conn.read()
	soup = BeautifulSoup(html)
	athlete = soup.find_all(class_="shooterInfo")[0]
	ath_all = athlete.text.split('Nation: ')
	ath_name = ath_all[0]
	ath_country = ath_all[1].split(' ')[0][0:3]
	ath_ID = str(athlete).split('issfid=')[1]
	ath_ID = ath_ID.split('&amp;')[0]
	print(ath_name,ath_country,ath_ID)
	links = soup.find_all('a')
	scores = []
	ind = [6,9,12,15,18]
	for sk2 in range(0,len(links)):
		link = links[sk2].get('href',None)
		if link != None:
			if (link.find(string_series)>-1):
				print sk2,link
				conn = urllib2.urlopen(url_master+link)
				html = conn.read()
				soup = BeautifulSoup(html)
				sc = soup.find_all('td')
				children = sc[0].findChildren()
				for ii in ind:
					scores.append(children[ii].text)
				for sk3 in range(1,6):
					scores.append(sc[sk3].text)
	print(scores)
	print(len(scores))
