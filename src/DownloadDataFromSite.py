#!/usr/bin/env python3
#-*-coding: utf-8-*-

# Created by G-lts Team
# Copyleft (ↄ)

# --- Για το κατέβασμα των ανακοινώσεων από την σελίδα. ---
import urllib.request # Για το κατέβασμα της σελίδας.
from bs4 import BeautifulSoup # Για το scapping της σελίδας.



class DownloadDataFromSite() : 

	# Οι δομές στις οπόίες θα κρατάω τα δεδομένα μου : 
	links_Of_Announcements = []
	announcements = []


	def __init__(self):
		'''
		Κατά την δημιουργεία του αντικειμένου δεν θα γίνεται τίποτα.
		'''



	def downloadPage(self) :
		'''
		Η μέθοδος αυτή έχει τον πολύ βασικό σκοπό που αφορά το κατέβασμα των ανακοινώσεων.
			1. "Κοιτάει"& "κατεβάζει" την σελίδα των ανακοινώσεων.
			2. Παίρνει τα "blocks" κώδικα που μας ενδιαφέρουν.
			3. Τέλος κρατάει μια λίστα αντικειμένου ( "self.tr" ) στην οποία η κάθε θέση της περιέχει ακριβώς *τις* πληροφορίες που θέλουμε.
		'''

		try :
			allPage = urllib.request.urlopen('https://www.ce.teiep.gr/news.php?sa=show_all')

		except urllib.error.URLError :
			raise

		html = BeautifulSoup(allPage)

		table = html.findAll('table',  {'border' : '0'} , {'width' : '100%'} )
		table = table[2]

		self.tr = []
		self.tr = table.findAll("tr")
		self.tr.pop(0)



	def findAll(self):
		'''
		Σε αυτή την μέθοδο, σε κάθε ένα από τα blocks κώδικα που έχω παίρνω :
			1. & τον σύνδεσμο προς την ανακοίνωση
			2. & την ανακοίνωση.
		Γεμίζοντας τις λίστες του αντικοιμένου.
		'''

		# Αρχικοποίηση ή επαναορισμός των λιστών ως άδειες ( για να μην έχω προβλήματα και στο refresh )
		DownloadDataFromSite.links_Of_Announcements = []
		DownloadDataFromSite.announcements = []

		for td in self.tr: # Για κάθε ένα td ( που έχει μέσα και την ανακοίνωση )..
			link = td.a # Παίρνω το <a> tag.
			DownloadDataFromSite.links_Of_Announcements.append( link.get('href') ) # Παίρνω λοιπόν τον σύνδεσμο της εκάστοτε ανακοίνωσης 
			DownloadDataFromSite.announcements.append( link.get_text().strip() ) # και το "κείμενο" της ανακοίνωσης αφάιρόντας τα περιτά κενά που μπορεί να υπάρξουν.


		self.fixLinks();



	def findLinksOnly(self):
		'''
		Σε αυτή την μέθοδο, σε κάθε ένα από τα blocks κώδικα που έχω παίρνω :
			1. Μονάχα τον *σύνδεσμο* προς την ανακοίνωση
		Γεμίζοντας την κατάλληλη λίστα του αντικοιμένου.
		'''

		DownloadDataFromSite.links_Of_Announcements = [] # Αρχικοποίηση ή επαναορισμός της λίστας ως άδεια ( για να μην έχω προβλήματα και στο refresh )

		for td in self.tr: # Για κάθε ένα td ( που έχει μέσα και την ανακοίνωση )..
			link = td.a # Παίρνω το <a> tag.
			DownloadDataFromSite.links_Of_Announcements.append( link.get('href') ) # Παίρνω λοιπόν τον σύνδεσμο της εκάστοτε ανακοίνωσης 
			# εδώ στην από πάνω γραμμή έχω ένα error, αλλά δε ξέρω το λόγο.. :/ ( συμβαίνει μερικές φορές μόνο... )

		self.fixLinks();



	def findAnnouncementsOnly(self):
		'''
		Σε αυτή την μέθοδο, σε κάθε ένα από τα blocks κώδικα που έχω παίρνω :
			1. Μονάχα την *ανακοίνωση*.
		Γεμίζοντας την κατάλληλη λίστα του αντικοιμένου.
		'''

		DownloadDataFromSite.announcements = [] # Αρχικοποίηση ή επαναορισμός της λίστας ως άδεια ( για να μην έχω προβλήματα και στο refresh )

		for td in self.tr: # Για κάθε ένα td ( που έχει μέσα και την ανακοίνωση )..
			link = td.a # Παίρνω το <a> tag.
			DownloadDataFromSite.announcements.append( link.get_text().strip() ) # και το "κείμενο" της ανακοίνωσης αφάιρόντας τα περιτά κενά που μπορεί να υπάρξουν.



	def refreshPage(self) :
		self.downloadPage_and_FindAll();



	def downloadPage_and_FindAll(self):
		self.downloadPage()
		self.findAll()



	def fixLinks(self):
		# Για να προσθέσω μπροστά από κάθε link και το "https://www.ce.teiep.gr/", ώστε να είναι σωστό το link.
		for link in range( 0 ,len( DownloadDataFromSite.links_Of_Announcements ) ) : 
			DownloadDataFromSite.links_Of_Announcements[link] = "https://www.ce.teiep.gr/" + DownloadDataFromSite.links_Of_Announcements[link]



	def get_Last10_Announcements(self):
		return DownloadDataFromSite.announcements[:10];



	def get_Last10_Links_by_Announcements(self):
		return DownloadDataFromSite.links_Of_Announcements[:10];




__version__ = '1.0'