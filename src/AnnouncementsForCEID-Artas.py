#!/usr/bin/env python3
#-*-coding: utf-8-*-

# Created by G-lts Team
# Copyleft (ↄ)


# ------------- Για το indicator applet ------------------

import sys
import lxml.html
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GLib
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

# --- Κάνω import το module που έκανα εγώ και το οποίο 
# είναι υπεύθυνο για το κατέβασμα των δεδομένων από το site. ---

from DownloadDataFromSite import *

########################################################################






class Applet():

	# Δημιουργώ λίστες ( αντικειμένου ) όπου θα κρατάω τα δεδομένα μου ( τις ανακοινώσεις ).
	link_anakinosis = []
	anakinosi = []



	######################################## Τα βασικά του applet ########################################
	
	def __init__(self):
	
		self.ind = appindicator.Indicator.new(
		"G-lts CEID-Artas Not-Up",
		"/opt/ceidArtasIndicator/images/student.png",
		appindicator.IndicatorCategory.APPLICATION_STATUS)
		

		self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
		self.ind.set_attention_icon( "/opt/ceidArtasIndicator/images/student-alert.png" ) 
		
		
		self.menu = Gtk.Menu()		
		self.ind.set_menu(self.menu)
		
		# Δημιουργεί το indicator applet πάνω, χωρίς τίποτα στο μενού του.

		# Καλώ επίσης και δημιουργώ ένα αντικείμενο της κλάσης που έχω κάνει εγώ και είναι υπεύθυνο ώστε να κατεβάζει και να αναλύει τα δεδομένα από το site :
		self.downloadDataFromSite = DownloadDataFromSite()
		self.downloadDataFromSite.findAll(); # Βρες αρχικά και τις ανακοινώσεις και τους συνδέσμους αυτών.


	################################################################################
	################################################################################		
		
	


	def getData_from_site(self):
		'''
		Μέθοδος η οποία ζητάει από το αντικείμενο "self.downloadDataFromSite" και παίρνει τις ανακοινώσεις.

		Η δομές που κρατάει τις ενημερώσεις είναι δύο λίστες αντικειμένου οι οποίες είναι οι ακόλουθες :
			 - Λίστα για τα ονόματα των ενημερώσεων ( Applet.anakinosi ).
			 - Λίστα για τους συνδέσμους προς τις ενημερώσεις ( Applet.link_anakinosis ).
		'''

		# Γέμισμα των δομών :
		Applet.anakinosi = self.downloadDataFromSite.get_Last10_Announcements()
		Applet.link_anakinosis = self.downloadDataFromSite.get_Last10_Links_by_Announcements()
	
		
		
	
	def updates_are_available(self):
		''' 
		Μέθοδος η οποία ελέγχει αν έχει υπάρξει κάτι καινούριο στο site.
		
		Συγκεκριμένα, κάνει "ανανέωση" στη σελίδα ενημερώσεων και παίρνει έπειτα τους ( νέους ίσος) συνδέσμους που βρίσκει.
		Έπειτα συγκρίνει τους *συνδέσμους* των ενημερώσεων που μόλις είδε πως υπάρχουν στην σελίδα, 
		με τους *συνδέσμους* των ενημερώσεων που ΥΠΉΡΧΑΝ στην σελίδα.
		
		ΑΝ υπάρχει κάποια διαφορά μεταξύ τους, σημαίνει πως βγήκε κάποια καινούρια ενημέρωση,
		οπότε και επιστρέφει True.
		
		ΑΝ δεν υπάρχει διαφορά μεταξύ τους επιστρέφει False.
		'''
		
		links_only = [] # Εδώ θα κρατήσω τα "νέα" ( ίσος ) links από το site, που θα τσεκάρω τώρα.
	
		# Τώρα θα ζητήσω να δω ΤΏΡΑ τι υπάρχει στο site ( μονάχα τους συνδέσμους βασικά ;) ).

		self.downloadDataFromSite.refreshPage()
		links_only = self.downloadDataFromSite.get_Last10_Links_by_Announcements()

		

		# Και τώρα θα συγκρίνω αυτά που είδα πως έχει ΤΏΡΑ το site, με αυτά που είχε πριν.

		if ( links_only == Applet.link_anakinosis ) : # Αν ισχύει πάει να πει πως στις λίστες - ενημερώσεις - δεν έχει αλλάξει κάτι, είναι ακριβώς ίδιες.
			return False
	
		else : # Δεν είναι ακριβώς ίδιες οι λίστες.. Άρα ΥΠΆΡΧΕΙ ενημέρωση! 
			return True
			
			
			
			
	
	
	def check_for_updates(self): 
		'''Μέθοδος η οποία ελέγχει για το αν υπάρχει ενημέρωση.

		Τσεκάρει αν υπάρχουν ενημερώσεις και ΑΝ υπάρχουν, ενημερώνει τις δομές όπου κρατούνται οι ενημερώσεις.
		'''
	
		if ( self.updates_are_available() ): # Αν υπάρχει αλλαγή στις λίστες! 
			# Καθαρίζω τις λίστες μου.
			Applet.link_anakinosis = []
			Applet.anakinosi = []
			# Ενημερώνω τις λίστες από την αρχή και τώρα θα περιέχουν και τα νέα πράγματα.
			self.getData_from_site()
	
			self.removeLabels() # Καθαρίζει όλα τα εικονίδια πρώτα.
			self.set_NewsItems() # Προσθήκη των νέων τώρα label που δείχνουν τις ενημερώσεις.
			self.set_InfoLabels() # Προσθήκη και των κλασικών label για τις διάφορες πληροφορίες.
			

			self.ind.set_status(appindicator.IndicatorStatus.ATTENTION) # Κάνε κόκκινο το εικονίδιο.	
			os.system("notify-send 'C.E.I.D. Άρτας ~ Ενημέρωση.' 'Βγήκε ανακοίνωση με τίτλο : {0}' ".format(Applet.anakinosi[0]) )
			os.system("paplay /usr/share/sounds/ubuntu/stereo/message.ogg")

	
			
		#else:
		#	print ("Όχι δεν υπάρχει ενημέρωση.")
		
		return True # ΠΡΈΠΕΙ -*ΟΠΩΣΔΉΠΟΤΕ*- ΕΔΏ να γυρνάει True ή False , ώστε να παίζει η ΕΠΑΝΆΛΗΨΗ!!.	







	def first(self):
		self.getData_from_site() # Βλέπω για πρώτη φορά τι έχει το site.





###################################################################################################################
######################################## Ότι αφορά το Indicator Applet. ###########################################
###################################################################################################################


	


	def set_NewsItems(self) :
		'''
		Μέθοδος η οποία δημιουργεί τα αντικείμενα της λίστας τους μενού που αφορούν τις ανακοινώσεις.

		Δημιουργεί κάθε μενού με τον τίτλο του ( label ), του προσθέτει την λειτουργικότητα του και τέλος το προσθέτει στο μενού.
		'''
	
		self.item0 = Gtk.MenuItem() # Δημιουργία ενός καινούριου αντικειμένου μενού - [ Πρώτου label ].
		self.item0.set_label(Applet.anakinosi[0]) # Με όνομα του label "MyIndicator.anakinosi[0]"
		self.item0.connect("activate", self.open_0 )  # Αν είναι ενεργό ή όχι & με πια μέθοδο συνδέετε.
		self.menu.append(self.item0) # Το προσθέτουμε στο μενού.


		self.item1 = Gtk.MenuItem() # [ Δεύτερο label ].
		self.item1.set_label(Applet.anakinosi[1])
		self.item1.connect("activate", self.open_1 ) 
		self.menu.append(self.item1)


		self.item2 = Gtk.MenuItem() # [ Τρίτο label ].
		self.item2.set_label(Applet.anakinosi[2])
		self.item2.connect("activate", self.open_2 ) 
		self.menu.append(self.item2)


		self.item3 = Gtk.MenuItem() # [ Τέταρτο label ].
		self.item3.set_label(Applet.anakinosi[3])
		self.item3.connect("activate", self.open_3 ) 
		self.menu.append(self.item3)


		self.item4 = Gtk.MenuItem() # [ Πέμπτο label ].
		self.item4.set_label(Applet.anakinosi[4])
		self.item4.connect("activate", self.open_4 ) 
		self.menu.append(self.item4)


		self.item5 = Gtk.MenuItem() # [ Έκτο label ].
		self.item5.set_label(Applet.anakinosi[5])
		self.item5.connect("activate", self.open_5 ) 
		self.menu.append(self.item5)


		self.item6 = Gtk.MenuItem() # [ Έβδομο label ].
		self.item6.set_label(Applet.anakinosi[6])
		self.item6.connect("activate", self.open_6 ) 
		self.menu.append(self.item6)


		self.item7 = Gtk.MenuItem() # [ Όγδοο label ].
		self.item7.set_label(Applet.anakinosi[7])
		self.item7.connect("activate", self.open_7 ) 
		self.menu.append(self.item7)


		self.item8 = Gtk.MenuItem() # [ Ένατο label ].
		self.item8.set_label(Applet.anakinosi[8])
		self.item8.connect("activate", self.open_8 ) 
		self.menu.append(self.item8)


		self.item9 = Gtk.MenuItem() # [ Δέκατο label ].
		self.item9.set_label(Applet.anakinosi[9])
		self.item9.connect("activate", self.open_9 ) 
		self.menu.append(self.item9)
		

		self.menu.show_all()
	




	def set_InfoLabels(self):
		
		self.seperator_line1 = Gtk.SeparatorMenuItem()
		self.menu.append(self.seperator_line1)

		# Θα δημιουργήσω ένα υπομενού το οποίο θα περιέχει βασικές σελίδες του Τ.Ε.Ι, ώστε αν θέλει ο χρήστης να πατάει πάνω σε αυτές και να μεταφέρετε. :)

		self.pages = Gtk.Menu()
		
		self.sub_menu_items = Gtk.MenuItem('Άνοιγμα σελίδας')

		self.menu.append(self.sub_menu_items)
		
		self.sub_menu_items.set_submenu(self.pages)

		
		
		
		# Δημιουργία του κουμπιού "Ανακοινώσεων".
		self.item_news = Gtk.MenuItem()
		self.item_news.set_label("Ανακοινώσεων")
		self.item_news.connect("activate", self.tei_news)
		self.pages.append(self.item_news) # Αυτό το αντικείμενο το προσθέτω στο νέο υπόμενού που έκανα
		
		
		
		# Δημιουργία του κουμπιού "Ασύγχρονης Τηλεκπαίδευσης".
		self.item_eclass = Gtk.MenuItem()
		self.item_eclass.set_label("Ασύγχρονης Τηλεκπαίδευσης")
		self.item_eclass.connect("activate", self.eclass)
		self.pages.append(self.item_eclass)
		

		# Δημιουργία του κουμπιού "Βαθμολογιών".
		self.item_stu = Gtk.MenuItem()
		self.item_stu.set_label("Βαθμολογιών")
		self.item_stu.connect("activate", self.tei_stu)
		self.pages.append(self.item_stu)
		
		
		#==================================================================================================================================
		

		self.seperator_line = Gtk.SeparatorMenuItem()
		self.menu.append(self.seperator_line)
		
		# Δημιουργία του κουμπιού "Πληροφορίες".
		self.item_info = Gtk.MenuItem()
		self.item_info.set_label("Πληροφορίες εφαρμογής")
		self.item_info.connect("activate", self.inform)
		self.menu.append(self.item_info)
		

		# Δημιουργία του κουμπιού εξόδου.
		self.q_item = Gtk.MenuItem()
		self.q_item.set_label("Έξοδος")
		self.q_item.connect("activate", self.quit)
		self.menu.append(self.q_item)

		
		self.menu.show_all()
		
		
		###################################################################################################)







	
	# Μέθοδος κουμπιού ενημέρωσης 0	
	def open_0(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[0]) # Για να ανοίξει τον σύνδεσμο σε νέα καρτέλα του βασικού browser. 
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE) # Για να αλλάξει την κατάσταση του εικονιδίου στο indicator applet.
			
	
	# Μέθοδος κουμπιού ενημέρωσης 1	
	def open_1(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[1])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)


	# Μέθοδος κουμπιού ενημέρωσης 2	
	def open_2(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[2])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	
	
	# Μέθοδος κουμπιού ενημέρωσης 3	
	def open_3(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[3])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

	
	# Μέθοδος κουμπιού ενημέρωσης 4	
	def open_4(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[4])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	
	
	# Μέθοδος κουμπιού ενημέρωσης 5	
	def open_5(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[5])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	
	
	# Μέθοδος κουμπιού ενημέρωσης 6		
	def open_6(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[6])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	
	
	# Μέθοδος κουμπιού ενημέρωσης 7	
	def open_7(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[7])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	
	
	# Μέθοδος κουμπιού ενημέρωσης 8
	def open_8(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[8])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	
	
	# Μέθοδος κουμπιού ενημέρωσης 9
	def open_9(self, widget):
		webbrowser.open_new_tab(Applet.link_anakinosis[9])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

	
	
	
	# Μέθοδος του κουμπιού Πληροφορίες.
	def inform(self, widget):
		webbrowser.open_new_tab("https://github.com/Tas-sos/CEID-Artas_Not-Up")
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
		
	
	
	

	def tei_news(self, widget):
		webbrowser.open_new_tab("https://www.ce.teiep.gr/news.php")
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)


	def eclass(self, widget):
		webbrowser.open_new_tab("https://www.ce.teiep.gr/e-class/")
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
	

	def tei_stu(self, widget):
		webbrowser.open_new_tab("https://gmweb.teiep.gr/unistudent/")
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)


	
	# Μέθοδος του κουμπιού εξόδου ( και τερματισμού το προγράμματος ).	
	def quit(self, widget):
		Gtk.main_quit()
	

		
		
		
		
			
	
	
	def removeLabels(self) :
		'''
		Μέθοδος η οποία διαγράφει τα ΌΛΑ τα αντικείμενα του μενού.

		Διαγράφει όλα τα αντικείμενα του applet.
		'''
	
	
		self.menu.remove(self.item0) # Διαγραφή του 1ου Label

		self.menu.remove(self.item1)

		self.menu.remove(self.item2)

		self.menu.remove(self.item3)

		self.menu.remove(self.item4)

		self.menu.remove(self.item5)

		self.menu.remove(self.item6)

		self.menu.remove(self.item7)

		self.menu.remove(self.item8)

		self.menu.remove(self.item9)
		
		
		self.menu.remove(self.seperator_line1)

		
		self.menu.remove(self.sub_menu_items);
		self.menu.remove(self.pages)

		self.menu.remove(self.seperator_line) 

		self.menu.remove(self.item_info)
		self.menu.remove(self.q_item)


	
	

	
	


################################################################################################################
#################################################### Κυρίως ####################################################
################################################################################################################


inticator_applet = Applet() # Οκ, τώρα εμφάνισε το Indicator Applet :D
inticator_applet.first() # Βλέπω για πρώτη φορά το site και ενημερώνω για πρώτη φορά τις δομές μου!

# Προσθήκη των στοιχείων του μενού : 
inticator_applet.set_NewsItems() # Προσθήκη των ενημερώσεων.
inticator_applet.set_InfoLabels() # Προσθήκη των βασικών στοιχείων στο μενού.


GLib.timeout_add_seconds(1800, inticator_applet.check_for_updates) # Κάθε μισή ώρα ( 1800 δευτερόλεπτα ), καλή την μέθοδο "check_for_updates" ( Η ΟΠΟΊΑ *ΠΡΈΠΕΙ* ΝΑ ΓΥΡΝΆΕΙ ΚΆΤΙ! )

Gtk.main()
	
	
	
	
	

