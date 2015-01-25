import urllib,urllib2
from bs4 import BeautifulSoup
import os, time
import pyPdf

#for parsing pdf
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

#for processing shots
from collections import deque

##########

do_download = 0
do_pdf_parsing = 1

time_delay_sec = 1

url_results = 'http://www.swedishcup.nu/'
folder_results = '2015/Result/3/PDF/Rifle/'
file_results = '1-46-50.pdf'

url_start = 'http://www.swedishcup.nu/2015/Result/' #http://www.swedishcup.nu/2015/Result/3/3.php

##########

def download_file(url,folder,file_name,destination_folder):
	download_url = url + folder + file_name
	response = urllib2.urlopen(download_url)
	if not os.path.exists(destination_folder):
		os.mkdir(destination_folder)
	file = open(destination_folder+file_name, 'w')
	file.write(response.read())
	file.close()
	print("Downloaded "+ file_name)

def crawl_day_results(url_start,day):
	url = url_start + str(day)+'/'+str(day)+'.php'
	print url
	conn = urllib2.urlopen(url)
	html = conn.read()
	soup = BeautifulSoup(html)
	links = soup.find_all('a')
	out_folder = 'PDF_DAY'+str(day-2)+'/'
	if not os.path.exists(out_folder):
		os.mkdir(out_folder)
	for tag in links:
		link = tag.get('href',None)
		if link != None:
			#check if main competition rifle
			if link.split('/')[1] == 'Rifle':
				if link.split('/')[2][0] in {'1','2','3','4','5','6','7'}:
					print link + ' downloading'
					download_url = url_start + str(day)+'/' + link
					response = urllib2.urlopen(download_url)
					file = open(out_folder+link.split('/')[2], 'w')
					file.write(response.read())
					file.close()
					time.sleep(time_delay_sec)

def pdfparser(file_name):
	fp = file(file_name, 'rb')
	rsrcmgr = PDFResourceManager()
	retstr = StringIO()
	codec = 'utf-8'
	laparams = LAParams()
	device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
	# Create a PDF interpreter object.
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	# Process each page contained in the document.
	for page in PDFPage.get_pages(fp):
		interpreter.process_page(page)
		data = retstr.getvalue()
	#text_file = open('out.txt', "w")
	#text_file.write(data)
	#text_file.close()
	return data

def sort_shots_and_write(queue_ids,queue_scores,one_shooter):
	for tt in range(len(queue_ids)):
		one_shooter[queue_ids.popleft()] = queue_scores.popleft()
	write_one_shooter(one_shooter)
	return queue_ids,queue_scores

def process_data(data):
	data = data.split("\n")
	data = filter(None, data)
	#print data
	series_set = ('ARW','ARJW','ARM','ARJM','ARV','R SH2')
	standard_set = ('FIN,','SWE,','DEN,','NOR,','SUI,','GER,','NED,','Day ','Swed','http','MLRe')
	one_shooter = dict()
	flag_total = 0
	queue_ids = deque()
	queue_scores = deque()
	for dt in data:
		#check flags
		if flag_total:
			if ('total_pdf' in one_shooter):
				if (float(dt)>float(one_shooter['total_pdf'])):
					one_shooter['total_pdf'] = dt
			else:
				one_shooter['total_pdf'] = dt
			flag_total = 0
		# check if new shooter
		if dt == '\x0cRelay':
			queue_ids,queue_scores = sort_shots_and_write(queue_ids,queue_scores,one_shooter)
			one_shooter = dict()
		# check content
		if dt in series_set: one_shooter['series'] = dt
		if dt == 'Total': flag_total = 1
		if dt[0:4] == 'Day ': one_shooter['day'] = dt.split(',')[0].split(' ')[1]
		if (len(dt)>8): #assume name and surname has at least 4 letters
			if not dt[0].isdigit(): # is not a digit
				if dt[0:4] not in standard_set:
					one_shooter['name'] = dt
					print dt
		#scores
		if (':' in dt) and (len(dt)<4): queue_ids.append(dt)
		if '.' in dt: # a number in the right format
			if 'x' in dt: dt = dt[:-1] #central 10
			if (len(dt)<4) or ((len(dt)==4) and (dt[0]=='1')): # it must be a single score
				queue_scores.append(dt)
	queue_ids,queue_scores = sort_shots_and_write(queue_ids,queue_scores,one_shooter)

def write_one_shooter(one_shooter):
	destination_folder = one_shooter['series'] + one_shooter['day']+'/'
	if not os.path.exists(destination_folder):
		os.mkdir(destination_folder)
	file_name = destination_folder + one_shooter['name']+'.txt'
	text_file = open(file_name, "w")
	#text_file.write(one_shooter['name']+'\n')
	#text_file.write(one_shooter['series'] + '\n')
	total_score = 0
	if one_shooter['series'] in {'ARM','ARJM','R SH2'}:
		no_shots = 60
	else:
		no_shots = 40
	for sk in range(no_shots):
		shot_id = str(sk+1)+':'
		shot_now = one_shooter[shot_id]
		text_file.write(shot_now + '\n')
		total_score += float(shot_now)
	if 	((total_score - float(one_shooter['total_pdf'])) > 0.01) :
		print one_shooter['name']+' score sum is incorrect'
		text_file.write('score pdf '+one_shooter['total_pdf'] + '\n')
		text_file.write('score count '+str(total_score))
	text_file.close()

##########

# download list of participants
if do_download:
	#download_file(url_results,folder_results,file_results,out_folder)
	for day in range(3,6): #day of January
		crawl_day_results(url_start,day)

#data = pdfparser('swedishcup2015/Rifle_2015.PDF')
#print data


# extract txt from pdf
if do_pdf_parsing:
	#data1 = pdfparser(out_folder+file_results)
	for day in range(3):
		folder_now = 'PDF_DAY'+str(day+1)+'/'
		file_names = next(os.walk(folder_now))[2]
		for file_now in file_names:
			print file_now
			data_raw = pdfparser(folder_now+file_now)
			# write files for individual shooters
			process_data(data_raw)


