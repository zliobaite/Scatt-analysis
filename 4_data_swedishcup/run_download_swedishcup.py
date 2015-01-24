import urllib,urllib2
from bs4 import BeautifulSoup
import os, time
import pyPdf

from collections import deque #for processing shots

url_home = 'http://iof3.idrottonline.se/'
folder_participants = 'ImageVaultFiles/id_110659/cf_104/'
file_name_participants = 'Rifle_2015.PDF'

out_folder = 'swedishcup2015/'

do_download = 0

time_delay_sec = 1

url_results = 'http://www.swedishcup.nu/'
folder_results = '2015/Result/3/PDF/Rifle/'
file_results = '1-46-50.pdf'

def download_file(url,folder,file_name,destination_folder):
	download_url = url + folder + file_name
	response = urllib2.urlopen(download_url)
	if not os.path.exists(destination_folder):
		os.mkdir(destination_folder)
	file = open(destination_folder+file_name, 'w')
	file.write(response.read())
	file.close()
	print("Downloaded "+ file_name)


# download list of participants
if do_download:
	#download_file(url_home,folder_participants,file_name_participants,out_folder)
	download_file(url_results,folder_results,file_results,out_folder)

import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

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
	text_file = open('out.txt', "w")
	text_file.write(data)
	text_file.close()
	return data

def sort_shots_and_write(queue_ids,queue_scores,one_shooter):
	if len(queue_scores)<40:
		print 'problem, shots are missing'
	else:
		for tt in range(40):
			one_shooter[queue_ids.popleft()] = queue_scores.popleft()
		write_one_shooter(one_shooter)
	return queue_ids,queue_scores

def process_data(data):
	data = data.split("\n")
	data = filter(None, data)
	print data
	flag_name = 0
	series_set = ('ARW')
	one_shooter = dict()
	flag_total = 0
	queue_ids = deque()
	queue_scores = deque()
	for dt in data:
		#check flags
		if flag_name:
			one_shooter['name'] = dt
			flag_name = 0
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
		if dt =='Series 1': flag_name = 1
		if dt in series_set: one_shooter['series'] = dt
		if dt == 'Total': flag_total = 1
		#scores
		if (':' in dt) and (len(dt)<4): queue_ids.append(dt)
		if '.' in dt: # a number in the right format
			if 'x' in dt: dt = dt[:-1] #central 10
			if (len(dt)<4) or ((len(dt)==4) and (dt[0]=='1')): # it must be a single score
				queue_scores.append(dt)
	queue_ids,queue_scores = sort_shots_and_write(queue_ids,queue_scores,one_shooter)


def write_one_shooter(one_shooter):
	file_name = one_shooter['series']+'_'+one_shooter['name']+'.txt'
	text_file = open(file_name, "w")
	#text_file.write(one_shooter['name']+'\n')
	#text_file.write(one_shooter['series'] + '\n')
	total_score = 0
	for sk in range(40):
		shot_id = str(sk+1)+':'
		shot_now = one_shooter[shot_id]
		text_file.write(shot_now + '\n')
		total_score += float(shot_now)
	text_file.write('score pdf '+one_shooter['total_pdf'] + '\n')
	text_file.write('score count '+str(total_score))
	text_file.close()



data1 = pdfparser(out_folder+file_results)
process_data(data1)


