import pyPdf
import urllib,urllib2
import os, time
from bs4 import BeautifulSoup

param_do_pdf_download = 0 #if 0 then not read, assume already saved
param_do_parsing = 1 # if 0 then do not extract links

file_name = "AR60M_Scatt_eng.pdf"
interesting_files = [51,57,76,80,94,98]

url_home = 'http://www.shooting-ua.com/'
url_site = 'control_On-Line.htm'
file_name_source = 'ua_online_web.txt'
out_folder = 'ua_online/'

time_delay_sec = 1

ct = 0

if param_do_pdf_download:

	file(file_name_source, "w").write(urllib2.urlopen(url_home+url_site).read())

	conn = urllib2.urlopen(url_home+url_site)
	html = conn.read()

	soup = BeautifulSoup(html)
	links = soup.find_all('a')
	
	if not os.path.exists(out_folder):
		os.mkdir(out_folder)

	for sk in range(len(links)):
		link = links[sk].get('href',None)
		if link != None:
			ln = link.strip().split('/')
			if (sk in interesting_files):
				print sk, ln[2]
				urllib.urlretrieve(url_home+link, out_folder+ln[2][0:5]+'_'+str(ct)+'.pdf')
				ct += 1
				time.sleep(time_delay_sec)

if param_do_parsing:

	all_files = os.listdir(out_folder)
	print (all_files)

	key = '/Annots'
	uri = '/URI'
	ank = '/A'

	for file_name in all_files:
		if file_name[-3:]=='pdf':
			print file_name
			file_name = out_folder+file_name
			f = open(file_name,'rb')

			pdf = pyPdf.PdfFileReader(f)
			pgs = pdf.getNumPages()
	

			for pg in range(pgs):
				p = pdf.getPage(pg)
				o = p.getObject()
	
				if o.has_key(key):
					ann = o[key]
					for a in ann:
						u = a.getObject()
						if u[ank].has_key(uri):
							link = u[ank][uri]
							print link
							ln = link.strip().split('/')
							urllib.urlretrieve(link, out_folder+ln[6])
							time.sleep(time_delay_sec)