import urllib,urllib2
from bs4 import BeautifulSoup
import os, time
import dateutil.parser as dparser
import csv

#example link
#http://www.issf-sports.org/athletes/athlete.ashx?personissfid=SHCROW1307198201

#2015-04-11 ChangW
#url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1692&resultkey=Q00000_I_1104150900.1.AR40.0'
url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1692&resultkey=Q10000_I_1004150900.1.AR60.0'

#2015-05-14 Fort Ben
#url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1694&resultkey=Q10000_I_1305150915.1.AR60.0'
#url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1694&resultkey=Q00000_I_1405151100.1.AR40.0'

#2015-05 Munich
#url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1695&resultkey=Q10000_I_2805150845.1.AR60.0'
#url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1695&resultkey=Q00000_I_2805151315.1.AR40.0'

#2014 Fort Ben
#url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1510&resultkey=Q10000_I_2803140815.1.AR60.0'
#url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1510&resultkey=Q00000_I_2903141115.1.AR40.0'

#2014 Munich
#url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1514&resultkey=Q10000_I_0806140845.1.AR60.0'
url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1514&resultkey=Q00000_I_0806141045.1.AR40.0'

#2014 Maribor
#url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1515&resultkey=Q10000_I_1506140900.1.AR60.0'
#url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1515&resultkey=Q00000_I_1506141330.1.AR40.0'

#2014 Beijing
#url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1516&resultkey=Q10000_I_0307140915.1.AR60.0'
#url = 'http://www.issf-sports.org/competitions/results/detail.ashx?cshipid=1516&resultkey=Q00000_I_0307141130.1.AR40.0'

url_master = 'http://www.issf-sports.org'
out_folder = 'scores/'
out_folder_athletes = 'athletes/'
out_folder_summary = 'summary/'

string_result = '/pages/resulttargets.ashx?reskey='
string_series = '/pages/resulttargetdetails.ashx?srid='

time_delay_sec = 1


#read the summary page with results
conn = urllib2.urlopen(url)
html = conn.read()
soup = BeautifulSoup(html)
links = soup.find_all('a')

# date of the event
for ln in soup.find_all(class_="row5"):
	d = ln.text
dd = dparser.parse(d,fuzzy=True)
if (soup.title.text.find('Women')>-1):
	file_name = str(dd.date())+'W.csv'
	file_name2 = str(dd.date())+'W.txt'
	file_name3 = str(dd.date())+'W_athletes.txt'
else:
	file_name = str(dd.date())+'M.csv'
	file_name2 = str(dd.date())+'M.txt'
	file_name3 = str(dd.date())+'M_athletes.txt'

# write all summary results page
if not os.path.exists(out_folder_summary):
	os.mkdir(out_folder_summary)
file(out_folder_summary+file_name2, "w").write(urllib2.urlopen(url).read())

result_links = []

#extract individual athletes (links)
for sk in range(0,len(links)):
	link = links[sk].get('href',None)
	if link != None:
		#print sk,link
		if (link.find(string_result)>-1):
			result_links.append(link)
		#urllib.urlretrieve(url+link, out_folder+link)
		#time.sleep(time_delay_sec)

result_links = list(set(result_links))


#process individual results
data_all = []
athletes_all = []
for sk in range(0,len(result_links)):
	scores = []
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
	athletes_all.append(ath_ID)
	print(sk,ath_name,ath_country,ath_ID)
	scores.append(ath_name)
	scores.append(ath_ID)
	scores.append(ath_country)
	links = soup.find_all('a')
	ind = [6,9,12,15,18]
	for sk2 in range(0,len(links)):
		link = links[sk2].get('href',None)
		if link != None:
			if (link.find(string_series)>-1):
				conn = urllib2.urlopen(url_master+link)
				html = conn.read()
				soup = BeautifulSoup(html)
				sc = soup.find_all('td')
				children = sc[0].findChildren()
				for ii in ind:
					scores.append(children[ii].text)
				for sk3 in range(1,6):
					scores.append(sc[sk3].text)
	data_all.append(scores)
	time.sleep(time_delay_sec)

#write results to a file
if not os.path.exists(out_folder):
	os.mkdir(out_folder)
wfile = open(out_folder+file_name, "wb")
writer = csv.writer(wfile, delimiter=',', quoting=csv.QUOTE_NONE)
for row in data_all:
	writer.writerow(row)
wfile.close()

#write athletes
if not os.path.exists(out_folder_athletes):
	os.mkdir(out_folder_athletes)
print(athletes_all)
wfile = open(out_folder_athletes+file_name3, "wb")
wfile.write('\n'.join(athletes_all))
wfile.close()
