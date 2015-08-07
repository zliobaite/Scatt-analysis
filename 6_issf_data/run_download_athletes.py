import urllib,urllib2
from bs4 import BeautifulSoup
import os, time
import dateutil.parser as dparser
import csv
import sys


url_master = 'http://www.issf-sports.org/athletes/athlete.ashx?personissfid='
out_file = 'athlete_bios.csv'
input_file = 'athleteID_master.txt'

#example link
#http://www.issf-sports.org/athletes/athlete.ashx?personissfid=SHCROW1307198201
#athlete_IDs = ('SHCROW1307198201','SHNORM0105198901')

wfile = open(input_file)
athlete_IDs = wfile.readlines()
wfile.close()

print(athlete_IDs)

time_delay_sec = 1

header = ['ID','name','country','gender','club','yob','start_competing','birth_place','start_practicing','hometown','personal_coach','residence','national_coach','height','hand','weight','eye','marital_status','events','children','education','profession','languages']

#write results to a file
wfile = open(out_file, "wb")
writer = csv.writer(wfile, delimiter=';', quoting=csv.QUOTE_NONE)
writer.writerow(header)

reload(sys)
sys.setdefaultencoding('utf8') # to solve the problem of umlaut writing

#process individual results
data_all = []
for sk in range(0,len(athlete_IDs)):
	at_now = []
	at_now.append(athlete_IDs[sk][:-2])
	url_now = url_master+athlete_IDs[sk]
	print(url_now)
	conn = urllib2.urlopen(url_now)
	html = conn.read()
	soup = BeautifulSoup(html)
	#athlete = soup.find_all(class_="issflist")
	athlete = soup.find_all('td')
	aa = athlete[0].text[:-3]
	aa = aa.split(' - ')
	at_now.append(aa[0]) #name
	at_now.append(aa[1]) #country
	at_now.append(athlete[5].text) #gender
	at_now.append(athlete[7].text) #club
	at_now.append(athlete[9].text) #birth
	at_now.append(athlete[11].text) #start competing
	at_now.append(athlete[13].text) #place of birth
	at_now.append(athlete[15].text) #practicing
	at_now.append(athlete[17].text) #hometown
	at_now.append(athlete[19].text) #personal coach
	at_now.append(athlete[21].text) #residence
	at_now.append(athlete[23].text) #national coach
	at_now.append(athlete[25].text) #height
	at_now.append(athlete[27].text) #hand
	at_now.append(athlete[29].text) #weight
	at_now.append(athlete[31].text) #eye
	at_now.append(athlete[33].text) #status
	at_now.append(athlete[35].text) #events
	at_now.append(athlete[37].text) #children
	at_now.append(athlete[41].text) #education
	at_now.append(athlete[45].text) #profession
	at_now.append(athlete[51].text) #languages
	for sk2 in range(len(at_now)):
		if at_now[sk2]==u'\xa0':
			at_now[sk2] = 'NA'
		at_now[sk2] = at_now[sk2].replace('\"', '')
		at_now[sk2] = at_now[sk2].replace(';', ',')
	#at_now[sk2].decode("utf-8").replace(u'\xfc', 'u')
	#['NA' if x==u'\xa0' else x for x in at_now]
	data_all.append(at_now)
	print(sk,at_now)
	writer.writerow(at_now)
	time.sleep(time_delay_sec)

# file writing
wfile.close()