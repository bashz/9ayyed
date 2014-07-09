#!/usr/bin/env python
#coding: utf8 

#scrape the polling center list from the isie official site (http://www.isie.tn/index.php/fr/)
# sudo apt-get install python-setuptools
# easy_install beautifulsoup4

import urllib2
from bs4 import BeautifulSoup
import csv
import time
import json
import os #for the se of wget command to download the files
source_url = "http://www.isie.tn/index.php/fr/"
# using urllib2 to read the remote html page
#html = urllib2.urlopen(source_url).read()
#but the site is usually down so I am putting the select values as a html sting here 
html='<select name="circonscription_isie" id="circonscription_isie" class="inputbox"><option>Circonscription</option><option value="1">Tunis 1</option><option value="2">Tunis 2</option><option value="3">Ben Arous</option><option value="4">Ariana</option><option value="5">Manouba</option><option value="6">Jendouba</option><option value="7">Le Kef</option><option value="8">Siliana</option><option value="9">Bizerte</option><option value="10">Béja</option><option value="11">Nabeul 1</option><option value="12">Nabeul 2</option><option value="13">Zaghouan</option><option value="14">Kairouan</option><option value="15">Kasserine</option><option value="16">Sidi Bouzid</option><option value="17">Gafsa</option><option value="18">Tozeur</option><option value="19">Kébili</option><option value="20">Sousse</option><option value="21">Mahdia</option><option value="22">Monastir</option><option value="23">Sfax 1</option><option value="24">Sfax 2</option><option value="25">Gabès</option><option value="26">Médenine</option><option value="27">Tataouine</option></select>'
#using BeautifulSoup library for pulling data out of HTML
soup = BeautifulSoup(html)
#gettting all the disticts
districts_html =soup.find('select', id="circonscription_isie")
#print districts_html
districts = districts_html.find_all('option')
f = open('districts.csv', 'wb')
writer = csv.writer(f,delimiter=',')
writer.writerow(["distric_code","district_name","region_code","region_name","center_code","center_name"])
for option in districts :
	if option.get('value'):
		#regions for districts  is given here http://www.isie.tn/get_params.php?val=1&file=regions where 1 is the disrtict code 
		region_url= "http://www.isie.tn/get_params.php?val=" + option.get('value') + "&file=regions"
                response=urllib2.urlopen(region_url)
		html = response.read()
		j = json.loads(html)
                for r in j :
			# centers for regions http://www.isie.tn/get_params.php?file=centres&val=1000 where 1000 is the region code ( given by 
			#the variable r
			center_url= "http://www.isie.tn/get_params.php?val=" + r + "&file=centres"
			center_response=urllib2.urlopen(center_url)
			center_html=center_response.read()
			center_json=json.loads(center_html)
			for c in center_json :
				writer.writerow([option.get('value'),option.text.encode('utf-8').strip(),r,j[r].encode('utf-8').strip(),c,center_json[c].encode('utf-8').strip()])

