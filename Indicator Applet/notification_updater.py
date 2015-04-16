#!/usr/bin/env python3
#-*-coding: utf-8-*-


# ------------- Για το indicator applet ------------------
import sys
import urllib.request
import hashlib
import lxml.html
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GLib
########################################################################


# --- Για το κατέβασμα των ανακοινώσεων από την σελίδα. ---
from bs4 import BeautifulSoup
import urllib.request
########################################################################

# --- Για άνοιγμα σελίδας σε νέα καρτέλα του browser. ---
import webbrowser

########################################################################

# --- Για να δημιουργώ καθυστερήσεις. ---

import time , threading

########################################################################

# --- Για να μπορώ να τρέχω linux commands. ---

import os

########################################################################



class MyIndicator:
	
	# Δημιουργώ λίστες όπου θα κρατάω τα δεδομένα μου ( τις ανακοινώσεις ).
	link_anakinosis = []
	anakinosi = []
	
	def __init__(self):
	
		self.ind = appindicator.Indicator.new(
		"Test",
		"ubuntuone-client-offline",
		appindicator.IndicatorCategory.APPLICATION_STATUS)
		# Είναι εδώ αυτό : /usr/share/icons/ubuntu-mono-light/status/22/ubuntuone-client-offline.svg
		

		self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
		self.ind.set_attention_icon("ubuntuone-client-error")
		self.menu = Gtk.Menu() # Βρίσκετε εδώ : /usr/share/icons/ubuntu-mono-light/status/22/ubuntuone-client-error.svg
		
		
		self.update_news() # Ότι αφορά τα labels των ενημερώσεων - ( Προσθήκη και ενημέρωση των τελευταίων 7 ανακοινώσεων ).
			
		
		# Δημιουργία του κουμπιού εξόδου.
		item = Gtk.MenuItem()
		item.set_label("Έξοδος") # Όνομα του κουμπιού
		item.connect("activate", self.quit) # Αν είναι ενεργό ή όχι & με πια συνάρτηση συνδέετε.
		self.menu.append(item)
	
		self.menu.show_all()
		self.ind.set_menu(self.menu)
		
		###################################################################################################




	def main(self):
		#self.ind.set_status(appindicator.IndicatorStatus.ACTIVE) οκ τώρα θα βγαίνει κόκκινο το εικονίδιο, με το που ανοίγει η εφαρμογή.
		#GLib.timeout_add_seconds(60, self.update_news) # Ενημέρωση κάθε 60 δευτερόλεπτα.
		Gtk.main()

		
		

		
	

###########################################################################################################################	
	def check_site(self): # Πάμε να κατεβάσουμε τα δεδομένα από την σελίδα τώρα.

		page = urllib.request.urlopen('https://www.ce.teiep.gr/news.php')
		
		html = BeautifulSoup(page)

		center = html.find_all('center')
		# Έτσι πείρα την λίστα "center", που η κάθε θέση της έχει ένα παιδίο <center>...</center>

		# Καθαρισμός των λιστών.
		MyIndicator.link_anakinosis = []
		MyIndicator.anakinosi = []
		
		
		for line in center: # Για να διασχίσω όλη την λίστα..
				link = line.a # Σε κάθε <center>.. να βρίσκω το <a> tag.
				MyIndicator.link_anakinosis.append( link.get('href') ) # Να παίρνω από το <a> tag το link μόνο.
				MyIndicator.anakinosi.append( link.get_text() ) # Να παίρνω από το <a> tag το κείμενο μόνο. ;)
		
		
		
		# Για να προσθέσω μπροστά από κάθε link και το "https://www.ce.teiep.gr/", ώστε να είναι σωστό το link.
		for line in range(0,len(MyIndicator.link_anakinosis)-1):
			a = "https://www.ce.teiep.gr/" + MyIndicator.link_anakinosis[line]
			MyIndicator.link_anakinosis[line]=a
		
		
		#for i in range(0,len(MyIndicator.anakinosi)-1): # Δε θέλω και το τελευταίο το άκυρο που παίρνω καταλάθος.
		#	print (MyIndicator.anakinosi[i], "-", MyIndicator.link_anakinosis[i] )
			

		# οκ μέχρι εδώ.. παίρνω και αποθηκεύω τις λίστες με τις ανακοινώσεις και τα urls τους.
		
###########################################################################################################################


	def update_news(self):
		
		self.check_site() # Καταρχήν ενημερώνω τις λίστες μου.
	
		self.ind.set_status(appindicator.IndicatorStatus.ATTENTION) # Κάνε κόκκινο το εικονίδιο.

		
		number_of_news = len(MyIndicator.anakinosi)-1 # Δε θέλω και το τελευταίο το άκυρο που παίρνω κατά λάθος.
		#print ("Η λίστα έχει ",number_of_news, " ανακοινώσεις.")


		################################# Δημιουργία των αντικειμένων του μενού #################################
		# Ας βάλω αρχικά 7 ενημερώσεις το πολύ να δείχνει.
		
		if number_of_news >= 1 :
			# Κουμπί ενημέρωσης 0 
			item = Gtk.MenuItem() # Δημιουργία ενός καινούριου αντικειμένου.
			item.set_label(MyIndicator.anakinosi[0]) # Με όνομα του label "MyIndicator.anakinosi[0]"
			item.connect("activate", self.open_0 )  # Αν είναι ενεργό ή όχι & με πια συνάρτηση συνδέετε.
			self.menu.append(item) # Το προσθέτουμε στο μενού.
	
	
			if number_of_news >= 2 :
				# Κουμπί ενημέρωσης 1 
				item = Gtk.MenuItem()
				item.set_label(MyIndicator.anakinosi[1])
				item.connect("activate", self.open_1 )
				self.menu.append(item)
	
	
				if number_of_news >= 3 : 	
					# Κουμπί ενημέρωσης 2 
					item = Gtk.MenuItem()
					item.set_label(MyIndicator.anakinosi[2])
					item.connect("activate", self.open_2 )
					self.menu.append(item)
		
		
					if number_of_news >= 4 : 
						# Κουμπί ενημέρωσης 3
						item = Gtk.MenuItem()
						item.set_label(MyIndicator.anakinosi[3])
						item.connect("activate", self.open_3 )
						self.menu.append(item)
					
					
						if number_of_news >= 5 : 
							# Κουμπί ενημέρωσης 4
							item = Gtk.MenuItem()
							item.set_label(MyIndicator.anakinosi[4])
							item.connect("activate", self.open_4 )
							self.menu.append(item)
			
			
							if number_of_news >= 6 : 
								# Κουμπί ενημέρωσης 5
								item = Gtk.MenuItem()
								item.set_label(MyIndicator.anakinosi[5])
								item.connect("activate", self.open_5 )
								self.menu.append(item)
								
								
								
								if number_of_news >= 7 : 
									# Κουμπί ενημέρωσης 6
									item = Gtk.MenuItem()
									item.set_label(MyIndicator.anakinosi[6])
									item.connect("activate", self.open_6 )
									self.menu.append(item)
									



	# Συνάρτηση κουμπιού ενημέρωσης 0	
	def open_0(self, widget):
		#self.hash = self.remote_hash
		webbrowser.open_new_tab(MyIndicator.link_anakinosis[0])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)



	# Συνάρτηση κουμπιού ενημέρωσης 1
	def open_1(self, widget):
		#self.hash = self.remote_hash
		webbrowser.open_new_tab(MyIndicator.link_anakinosis[1])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)	



	# Συνάρτηση κουμπιού ενημέρωσης 2
	def open_2(self, widget):
		#self.hash = self.remote_hash
		webbrowser.open_new_tab(MyIndicator.link_anakinosis[2])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)		



	# Συνάρτηση κουμπιού ενημέρωσης 3
	def open_3(self, widget):
		#self.hash = self.remote_hash
		webbrowser.open_new_tab(MyIndicator.link_anakinosis[3])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	
		
		
	# Συνάρτηση κουμπιού ενημέρωσης 4
	def open_4(self, widget):
		#self.hash = self.remote_hash
		webbrowser.open_new_tab(MyIndicator.link_anakinosis[4])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)


	# Συνάρτηση κουμπιού ενημέρωσης 5
	def open_5(self, widget):
		#self.hash = self.remote_hash
		webbrowser.open_new_tab(MyIndicator.link_anakinosis[5])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	
		
		
	# Συνάρτηση κουμπιού ενημέρωσης 6
	def open_6(self, widget):
		#self.hash = self.remote_hash
		webbrowser.open_new_tab(MyIndicator.link_anakinosis[6])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)	
		
		
		
		
	# Συνάρτηση κουμπιού εξόδου.	
	def quit(self, widget):
		Gtk.main_quit()
    
    
    
    

if __name__ == '__main__':

	indicator = MyIndicator();
	indicator.main();









