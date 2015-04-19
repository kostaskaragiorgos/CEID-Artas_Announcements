#!/usr/bin/env python3
#-*-coding: utf-8-*-
# G-lts Team.


# ------------- Για το indicator applet ------------------
import sys
import urllib.request
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







class Applet():

	# Δημιουργώ λίστες όπου θα κρατάω τα δεδομένα μου ( τις ανακοινώσεις ).
	link_anakinosis = []
	anakinosi = []



	######################################## Τα βασικά του applet ########################################
	
	def __init__(self):
	
		self.ind = appindicator.Indicator.new(
		"G-lts CEID-Artas Not-Up",
		"ubuntuone-client-offline",
		appindicator.IndicatorCategory.APPLICATION_STATUS)
		# Είναι εδώ αυτό : /usr/share/icons/ubuntu-mono-light/status/22/ubuntuone-client-offline.svg
		

		self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
		self.ind.set_attention_icon("ubuntuone-client-error") # Βρίσκετε εδώ : /usr/share/icons/ubuntu-mono-light/status/22/ubuntuone-client-error.svg
		
		
		self.menu = Gtk.Menu() # Εδώ δημιουργείτε ένα νέο στοιχείο μενού
		
		self.ind.set_menu(self.menu) # Προσθέτουμε το μενού στο indicator applet.
		
		# Δημιουργεί το indicator applet πάνω, χωρίς τίποτα στο μενού του.


	################################################################################
	################################################################################		
		
	


	def getData_from_site(self): # Συνάρτηση η οποία βλέπει το site ΤΩΡΑ και επιστρέφει το top10.
	
	
		# Δημιουργώ λίστες όπου θα κρατάω τα δεδομένα μου - ΤΟΠΙΚΑ.
		self.temp_link_anakinosis = []
		self.temp_anakinosi = []
		
			
		page = urllib.request.urlopen('https://www.ce.teiep.gr/news.php')
		
		html = BeautifulSoup(page)

		center = html.find_all('center')
		# Έτσι πείρα την λίστα "center", που η κάθε θέση της έχει ένα πεδίο <center>...</center>
	
		
		for line in center: # Για να διασχίσω όλη την λίστα..
			link = line.a # Παίρνω το <a> tag.
			self.temp_link_anakinosis.append( link.get('href') ) # Να παίρνω από το <a> tag το link μόνο.
			self.temp_anakinosi.append( link.get_text() ) # Να παίρνω από το <a> tag το κείμενο μόνο. ;)
		

		
				
		# Για να προσθέσω μπροστά από κάθε link και το "https://www.ce.teiep.gr/", ώστε να είναι σωστό το link.
		for line in range(0,len(self.temp_link_anakinosis)-1 ): # ΠΡΟΣΟΧΉ και εδώ ΜΈΧΡΙ ΠΟΥ ΠΆΩ!! 
			a = "https://www.ce.teiep.gr/" + self.temp_link_anakinosis[line]
			self.temp_link_anakinosis[line]=a



	
		return self.temp_link_anakinosis , self.temp_anakinosi
	
	
	
	
	
	
	
	def updates_are_available(self): # Συνάρτηση η οποία ελέγχει αν έχει υπάρξει κάτι καινούριο στο site.
		
		self.links_only = [] # Εδώ θα κρατήσω τα "νέα" ( ίσος ) links από το site, που θα τσεκάρω τώρα.
	
		# Τώρα θα δω, ΤΏΡΑ τι υπάρχει στο site ( μονάχα τους συνδέσμους βασικά ;) ).
	
		page = urllib.request.urlopen('https://www.ce.teiep.gr/news.php')		
		html = BeautifulSoup(page)
		center = html.find_all('center')
		
		
		for line in center: # Και τώρα εδώ θα πάρω ΜΌΝΟ τους συνδέσμους.
			link = line.a # Παίρνω το <a> tag.
			self.links_only.append( link.get('href') ) # Παίρνω τον σύνδεσμο.
	
				
		# Για να προσθέσω μπροστά από κάθε link και το "https://www.ce.teiep.gr/", ώστε να είναι σωστό το link.
		for line in range(0,len(self.links_only)-1 ): # ΠΡΟΣΟΧΉ εδώ μέχρι που πάω..
			a = "https://www.ce.teiep.gr/" + self.links_only[line]
			self.links_only[line]=a
		
		
		# Και τώρα θα συγκρίνω αυτά που είδα πως έχει ΤΏΡΑ το site, με αυτά που είχε πριν.
		
		
		if ( self.links_only == Applet.link_anakinosis ) : # Αν ισχύει πάει να πει πως στις λίστες δεν αλλάζει κάτι.. είναι ακριβώς ίδιες.
			return True
	
		else : # Δεν είναι ακριβώς ίδιες οι λίστες.. Άρα ΥΠΆΡΧΕΙ ενημέρωση! 
			return False
			
			
			
			
	
	
	def check_for_updates(self): # Ελέγχει για το αν υπάρχουν ενημερώσεις και ΑΝ υπάρχουν, ενημερώνει τις δομές.

	
		if ( self.updates_are_available() == False ): # Αν υπάρχει αλλαγή στις λίστες! 
			#print ("Υπάρχει ενημέρωση! :D")
			# Καθαρίζω τις λίστες μου.
			Applet.link_anakinosis = []
			Applet.anakinosi = []
			# Ενημερώνω τις λίστες από την αρχή και τώρα θα περιέχουν και τα νέα πράγματα.
			Applet.link_anakinosis , Applet.anakinosi = self.getData_from_site()
	
			self.removeLabels() # Διαγράφω όλα τα κουμπιά πρώτα.
			self.setLabels() # Προσθήκη των νέων τώρα κουμπιών.
			

			self.ind.set_status(appindicator.IndicatorStatus.ATTENTION) # Κάνε κόκκινο το εικονίδιο.	
			os.system("notify-send 'C.E.I.D. Άρτας ~ Ενημέρωση.' 'Βγήκε ανακοίνωση με τίτλο : {0}' ".format(Applet.anakinosi[0]) )
			os.system("paplay /usr/share/sounds/ubuntu/stereo/message.ogg")

	
			
		#else:
		#	print ("Όχι δεν υπάρχει ενημέρωση.")
		
		return True # ΠΡΈΠΕΙ -*ΟΠΩΣΔΉΠΟΤΕ*- ΕΔΏ να γυρνάει True ή False , ώστε να παίζει η ΕΠΑΝΆΛΗΨΗ!!.	







	def first(self): # Βλέπω για πρώτη φορά τι έχει το site.
		Applet.link_anakinosis , Applet.anakinosi = self.getData_from_site()





###################################################################################################################
######################################## Ότι αφορά το Indicator Applet. ###########################################
###################################################################################################################


	


	def setLabels(self): # Συνάρτηση η οποία δημιουργεί τα Labels.
	
		number_of_news = len(Applet.anakinosi)-1 # Δε θέλω και το τελευταίο το άκυρο που παίρνω κατά λάθος.
		
		
		if number_of_news >= 1 :
			self.item0 = Gtk.MenuItem() # Δημιουργία ενός καινούριου αντικειμένου μενού - [ Πρώτου label ].
			self.item0.set_label(Applet.anakinosi[0]) # Με όνομα του κουμπιού "MyIndicator.anakinosi[0]"
			self.item0.connect("activate", self.open_0 )  # Αν είναι ενεργό ή όχι & με πια συνάρτηση συνδέετε.
			self.menu.append(self.item0) # Το προσθέτουμε στο μενού.
		
		
			if number_of_news >= 2 :
				self.item1 = Gtk.MenuItem() # [ Δεύτερο label ].
				self.item1.set_label(Applet.anakinosi[1])
				self.item1.connect("activate", self.open_1 ) 
				self.menu.append(self.item1)
		
		
				if number_of_news >= 3 :
					self.item2 = Gtk.MenuItem() # [ Τρίτο label ].
					self.item2.set_label(Applet.anakinosi[2])
					self.item2.connect("activate", self.open_2 ) 
					self.menu.append(self.item2)
		
		
					if number_of_news >= 4 :
						self.item3 = Gtk.MenuItem() # [ Τέταρτο label ].
						self.item3.set_label(Applet.anakinosi[3])
						self.item3.connect("activate", self.open_3 ) 
						self.menu.append(self.item3)
		

						if number_of_news >= 5 :
							self.item4 = Gtk.MenuItem() # [ Πέμπτο label ].
							self.item4.set_label(Applet.anakinosi[4])
							self.item4.connect("activate", self.open_4 ) 
							self.menu.append(self.item4)
		
		
							if number_of_news >= 6 :
								self.item5 = Gtk.MenuItem() # [ Έκτο label ].
								self.item5.set_label(Applet.anakinosi[5])
								self.item5.connect("activate", self.open_5 ) 
								self.menu.append(self.item5)
		
		
								if number_of_news >= 7 :
									self.item6 = Gtk.MenuItem() # [ Έβδομο label ].
									self.item6.set_label(Applet.anakinosi[6])
									self.item6.connect("activate", self.open_6 ) 
									self.menu.append(self.item6)


									if number_of_news >= 8 :
										self.item7 = Gtk.MenuItem() # [ Όγδοο label ].
										self.item7.set_label(Applet.anakinosi[7])
										self.item7.connect("activate", self.open_7 ) 
										self.menu.append(self.item7)
		
		
										if number_of_news >= 9 :
											self.item8 = Gtk.MenuItem() # [ Ένατο label ].
											self.item8.set_label(Applet.anakinosi[8])
											self.item8.connect("activate", self.open_8 ) 
											self.menu.append(self.item8)
		
		
											if number_of_news == 10 : # Ε.. μέχρι 10 το πολύ ανακοινώσεις να δείχνω..
												self.item9 = Gtk.MenuItem() # [ Δέκατο label ].
												self.item9.set_label(Applet.anakinosi[9])
												self.item9.connect("activate", self.open_9 ) 
												self.menu.append(self.item9)
		
		
		
			
		
		
		self.seperator_line = Gtk.SeparatorMenuItem()
		self.menu.append(self.seperator_line) 
		
		
		# Δημιουργία του κουμπιού "Πληροφορίες".
		self.item_info = Gtk.MenuItem()
		self.item_info.set_label("Πληροφορίες εφαρμογής")
		self.item_info.connect("activate", self.inform)
		self.menu.append(self.item_info)
		

		# Δημιουργία του κουμπιού εξόδου.
		self.q_item = Gtk.MenuItem()
		self.q_item.set_label("Έξοδος") # Όνομα του κουμπιού
		self.q_item.connect("activate", self.quit) # Αν είναι ενεργό ή όχι & με πια συνάρτηση συνδέετε.
		self.menu.append(self.q_item)

		
		self.menu.show_all()
		
		
		###################################################################################################)


	
	# Συνάρτηση κουμπιού ενημέρωσης 0	
	def open_0(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[0]) # Για να ανοίξει τον σύνδεσμο σε νέα καρτέλα του βασικού browser. 
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE) # Για να αλλάξει την κατάσταση του εικονιδίου στο indicator applet.
			
	
	# Συνάρτηση κουμπιού ενημέρωσης 1	
	def open_1(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[1])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)


	# Συνάρτηση κουμπιού ενημέρωσης 2	
	def open_2(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[2])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	
	
	# Συνάρτηση κουμπιού ενημέρωσης 3	
	def open_3(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[3])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

	
	# Συνάρτηση κουμπιού ενημέρωσης 4	
	def open_4(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[4])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	
	
	# Συνάρτηση κουμπιού ενημέρωσης 5	
	def open_5(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[5])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	
	
	# Συνάρτηση κουμπιού ενημέρωσης 6		
	def open_6(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[6])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	
	
	# Συνάρτηση κουμπιού ενημέρωσης 7	
	def open_7(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[7])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	
	
	# Συνάρτηση κουμπιού ενημέρωσης 8
	def open_8(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[8])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	
	
	# Συνάρτηση κουμπιού ενημέρωσης 9
	def open_9(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[9])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

	
	
	
	
	# Συνάρτηση του κουμπιού Πληροφορίες.
	def inform(self, widget):
		webbrowser.open_new_tab("https://github.com/Tas-sos/CEID-Artas_Not-Up")
		
	
		
	# Συνάρτηση του κουμπιού εξόδου.	
	def quit(self, widget):
		Gtk.main_quit()
	

		
		
		
		
			
	
	
	def removeLabels(self): # Συνάρτηση η οποία διαγράφει τα ΌΛΑ τα Labels.
	
		number_of_news = len(Applet.anakinosi)-1 # Δε θέλω και το τελευταίο το άκυρο που παίρνω κατά λάθος.
	
	
		if number_of_news >= 1 :
			self.menu.remove(self.item0) # Διαγραφή του 1ου Label
		
			if number_of_news >= 2 :
				self.menu.remove(self.item1)
				
				
				if number_of_news >= 3 :
					self.menu.remove(self.item2)
					
					
					if number_of_news >= 4 :
						self.menu.remove(self.item3)
						
						
						if number_of_news >= 5 :
							self.menu.remove(self.item4)
							
							
							if number_of_news >= 6 :
								self.menu.remove(self.item5)
								
								
								if number_of_news >= 7 :
									self.menu.remove(self.item6)
									
									
									if number_of_news >= 8 :
										self.menu.remove(self.item7)
										
										
										if number_of_news >= 9 :
											self.menu.remove(self.item8)
											
											
											if number_of_news == 10 :
												self.menu.remove(self.item9)
		
		

		self.menu.remove(self.seperator_line) # Διαγραφή της διαχωριστικής γραμμής.
		self.menu.remove(self.item_info) # Διαγραφή του κουμπιού Πληροφορίες.
		self.menu.remove(self.q_item) # Διαγραφή του Quit Label

	
	
	

	
	


################################################################################################################
#################################################### Κυρίως ####################################################
################################################################################################################


inticator_applet = Applet() # Οκ, τώρα εμφάνισε το Indicator Applet :D
inticator_applet.first() # Βλέπω για πρώτη φορά το site και ενημερώνω για πρώτη φορά τις δομές μου!
inticator_applet.setLabels() # Προσθήκη των πρώτων Label.

GLib.timeout_add_seconds(60, inticator_applet.check_for_updates) # Κάθε 60 δευτερόλεπτα καλή την μέθοδο "check_for_updates" ( ΠΡΈΠΕΙ ΝΑ ΓΥΡΝΆΕΙ ΚΆΤΙ! )

Gtk.main()







