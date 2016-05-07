#!/usr/bin/env python3
#-*-coding: utf-8-*-

# Created by G-lts Team
# Copyleft (ↄ)

# --- Για το κατέβασμα των ανακοινώσεων από την σελίδα. ---
import urllib.request # Για το κατέβασμα της σελίδας.
from bs4 import BeautifulSoup # Για το scapping της σελίδας.



class DownloadDataFromSiteTEIEP() : 

	# Οι δομές στις οπόίες θα κρατάω τα δεδομένα μου : 
	links = []
	announcements = []


	def __init__(self):
		'''
		Κατά την δημιουργία του αντικειμένου δεν θα γίνεται τίποτα.
		'''




	def downloadPage(self) :
		'''
		Η μέθοδος αυτή έχει τον πολύ βασικό & απλό σκοπό. Ο οποίος είναι να κατεβάσει απλώς την σελίδα των ανακοινώσεων.

			1. Κατεβάζει την σελίδα των ανακοινώσεων.
			2. Παίρνει τα "blocks" κώδικα που μας ενδιαφέρουν.
			3. Τέλος κρατάει μια λίστα αντικειμένου ( "self.all_a_Tag" ) στην οποία η κάθε θέση της περιέχει *τις* πληροφορίες που θέλουμε για
			την εκάστοτε ανακοίνωση.
		'''

		try :
			allPage = urllib.request.urlopen('http://www.teiep.gr/section.php?titlos=%CE%B1%CE%BD%CE%B1%CE%BA%CE%BF%CE%B9%CE%BD%CF%89%CF%83%CE%B5%CE%B9%CF%83-379')

		except urllib.error.URLError :
			raise

		html = BeautifulSoup(allPage)

		# Έτσι όλα τα a tags που έχουν τις ανακοινώσις μέσα.
		self.all_a_Tag = html.findAll('a' , style="color:#333333;font-size:14px;padding:5px 0 5px 0;" )
		# <a href="view.php?titlos=10η-έκτακτη-συνεδρίαση-συνέλευσης-τει-1019" style="color:#333333;font-size:14px;padding:5px 0 5px 0;">10η έκτακτη συνεδρίαση Συνέλευσης ΤΕΙ</a>




	def findAll(self):
		'''
		Σε αυτή την μέθοδο πλέον αναλύονται & εξάγονται, ξεχωρίζονται και απομονώνονται οι πληροφορίες που θέλω.

		Παίρνω δηλαδή πλέον δύο ξεχωριστές λίστες.
			1. για το τίτλο των εκάστοτε ανακοινώσεων
			2. για τον σύνδεσμο προς την εκάστοτε ενημέρωση.
		'''

		# Αρχικοποιώ τις δομές μου για σιγουριά. :)
		DownloadDataFromSiteTEIEP.links = []
		DownloadDataFromSiteTEIEP.announcements = []

		for aTag in self.all_a_Tag :
			DownloadDataFromSiteTEIEP.announcements.append( aTag.get_text().strip() ) # η .strip() καθαρίζει το string από τα άσκοπα κενά.
			DownloadDataFromSiteTEIEP.links.append( aTag.get('href') )

		self.fixLinks();




	def fixLinks(self) :
		'''
		Διορθώνει τους συνδέσμους που παίρνει από την σελίδα των ανακοινώσεων.

		Όταν παίρνει τους συνδέσμους προς τις ανακοινώσεις τους παίρνει με το "σχετικό" ας πω μονοπάτι τους,
		δηλαδή έτσι : "view.php?titlos=4ο-συμβούλιο-τει-1011" , όμως πρέπει να είναι έτσι : 
		"http://www.teiep.gr/view.php?titlos=4ο-συμβούλιο-τει-1011". Για αυτό λοιπόν τον λόγο υπάρχει η μέθοδος αυτή.
		'''

		for link in range( 0 , len(DownloadDataFromSiteTEIEP.links) ) :
			DownloadDataFromSiteTEIEP.links[link] = "http://www.teiep.gr/" + DownloadDataFromSiteTEIEP.links[link]




	def downloadPage_and_FindAll(self):
		self.downloadPage()
		self.findAll()




	def refreshPage(self) :
		self.downloadPage_and_FindAll();






__version__ = '1.0'




