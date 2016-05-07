#!/usr/bin/env python3
#-*-coding: utf-8-*-

# Created by G-lts Team
# Copyleft (ↄ)

# --- Για το κατέβασμα των ανακοινώσεων από την σελίδα. ---
import urllib.request # Για το κατέβασμα της σελίδας.
from bs4 import BeautifulSoup # Για το scapping της σελίδας.



class DownloadDataFromSiteCEID() : 

	# Οι δομές στις οπόίες θα κρατάω τα δεδομένα μου : 
	links_Of_Announcements = []
	announcements = []


	def __init__(self):
		'''
		Κατά την δημιουργία του αντικειμένου δεν θα γίνεται τίποτα.
		'''




	def downloadPage(self) :
		'''
		Η μέθοδος αυτή έχει τον πολύ βασικό σκοπό που αφορά το κατέβασμα των ανακοινώσεων.
			1. "Κοιτάει"& "κατεβάζει" την σελίδα των ανακοινώσεων.
			2. Παίρνει τα "blocks" κώδικα που μας ενδιαφέρουν.
			3. Τέλος κρατάει μια λίστα αντικειμένου ( "self.all_aTags" ) στην οποία η κάθε θέση της περιέχει ακριβώς *τις* πληροφορίες που θέλουμε.
		'''

		try :
			allPage = urllib.request.urlopen('https://www.ce.teiep.gr/news.php?sa=show_all')

		except urllib.error.URLError :
			raise

		html = BeautifulSoup(allPage)

		# Mε την παρακάτω μοναδική εντολή παίρνω ότι είναι μέσα στο "<table class="table table-striped">" - εκεί βρίσκονται οι ανακοινώσεις  
		table = html.find('table',  {'class' : 'table table-striped'}  )

		# Με την παρακάτω εντολή παίρνω ότι a tag υπάρχει εκεί μέσα. :)
		self.all_aTags = table.findAll('a') # Έτσι παίρνω κατευθείαν όλα τα a tags που αφορούν τις ανακοινώσεις και μόνο.




	def findAll(self):
		'''
		Σε αυτή την μέθοδο, σε κάθε ένα από τα blocks κώδικα που έχω παίρνω :
			1. & τον σύνδεσμο προς την ανακοίνωση
			2. & την ανακοίνωση.
		Γεμίζοντας τις λίστες του αντικειμένου.
		'''

		# Αρχικοποίηση ή επαναορισμός των λιστών ως άδειες ( για να μην έχω προβλήματα και στο refresh )
		DownloadDataFromSiteCEID.links_Of_Announcements = []
		DownloadDataFromSiteCEID.announcements = []


		for aTag in self.all_aTags: # Για κάθε ένα a tag
			DownloadDataFromSiteCEID.links_Of_Announcements.append( aTag.get('href') ) # Παίρνω λοιπόν τον σύνδεσμο της εκάστοτε ανακοίνωσης 
			DownloadDataFromSiteCEID.announcements.append( aTag.get_text().strip() ) # και το "κείμενο" (τίτλο) της ανακοίνωσης αφάιρόντας τα περιττά κενά που μπορεί να υπάρξουν.

		self.fixLinks();




	def findLinksOnly(self):
		'''
		Σε αυτή την μέθοδο, σε κάθε ένα από τα blocks κώδικα που έχω παίρνω :
			1. Μονάχα τον *σύνδεσμο* προς την ανακοίνωση
		Γεμίζοντας την κατάλληλη λίστα του αντικειμένου.
		'''

		DownloadDataFromSiteCEID.links_Of_Announcements = []

		for aTag in self.all_aTags:
			DownloadDataFromSiteCEID.links_Of_Announcements.append( aTag.get('href') )

		self.fixLinks();




	def findAnnouncementsOnly(self):
		'''
		Σε αυτή την μέθοδο, σε κάθε ένα από τα blocks κώδικα που έχω παίρνω :
			1. Μονάχα την *ανακοίνωση*.
		Γεμίζοντας την κατάλληλη λίστα του αντικειμένου.
		'''

		DownloadDataFromSiteCEID.announcements = []

		for aTag in self.all_aTags:
			DownloadDataFromSiteCEID.announcements.append( aTag.get_text().strip() )




	def refreshPage(self) :
		self.downloadPage_and_FindAll();




	def downloadPage_and_FindAll(self):
		self.downloadPage()
		self.findAll()




	def fixLinks(self):
		'''
		Διορθώνει τους συνδέσμους προς τις ανακοινώσεις.
		
		Για να προσθέσω μπροστά από κάθε link και το "https://www.ce.teiep.gr/", ώστε να είναι σωστό το link.
		'''
		# Για να προσθέσω μπροστά από κάθε link και το "https://www.ce.teiep.gr/", ώστε να είναι σωστό το link.
		for link in range( 0 ,len( DownloadDataFromSiteCEID.links_Of_Announcements ) ) : 
			DownloadDataFromSiteCEID.links_Of_Announcements[link] = "https://www.ce.teiep.gr/" + DownloadDataFromSiteCEID.links_Of_Announcements[link]




	def get_Last10_Announcements(self):
		return DownloadDataFromSiteCEID.announcements[:10];




	def get_Last10_Links_by_Announcements(self):
		return DownloadDataFromSiteCEID.links_Of_Announcements[:10];






__version__ = '2.0'


