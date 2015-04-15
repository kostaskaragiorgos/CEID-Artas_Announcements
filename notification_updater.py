#!/usr/bin/env python3
#-*-coding: utf-8-*-

from bs4 import BeautifulSoup
import urllib.request

page = urllib.request.urlopen('https://www.ce.teiep.gr/news.php')

html = BeautifulSoup(page)

center = html.find_all('center')
# Έτσι πείρα την λίστα "center", που η κάθε θέση της έχει ένα παιδίο <center>...</center>

#for line in center: # Για να διασχίσω όλη την λίστα..
#	for a in line.find_all('a'): # και για να πάρω από κάθε θέση μονάχα το <a> tag
#		print (a)


print ("\nΑναλυτικό print!\n")

# Δημιουργώ λίστες όπου θα κρατάω τα δεδομένα μου
link_anakinosis = []
anakinosi = []

for line in center: # Για να διασχίσω όλη την λίστα..
	for link in line.find_all('a'): # Σε κάθε <center>.. να βρήσω το <a> tag.
		link_anakinosis.append( link.get('href') ) # Να παίρνω από το <a> tag το link μόνο.
		anakinosi.append( link.get_text() ) # Να παίρνω από το <a> tag το κείμενο μόνο. ;)


# Για να προσθέσω μπροστά από κάθε link και το "https://www.ce.teiep.gr/", ώστε να είναι σωστό το link.
for line in range(0,len(link_anakinosis)):
	a = "https://www.ce.teiep.gr/" + link_anakinosis[line]
	link_anakinosis[line]=a



for i in range(0,len(anakinosi)):
	print (anakinosi[i], "-", link_anakinosis[i] )




