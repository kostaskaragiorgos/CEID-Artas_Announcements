#!/usr/bin/env python3
#-*-coding: utf-8-*-

# Created by G-lts Team
# Copyleft (ↄ)


# ------------- Για το indicator applet ------------------
import lxml.html
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GLib
########################################################################

# --- Για άνοιγμα σελίδας σε νέα καρτέλα του browser. ---

import webbrowser

########################################################################

# --- Για να μπορώ να τρέχω linux commands. ---

import os

########################################################################

# --- Κάνω import το module που έκανα εγώ και το οποίο είναι υπεύθυνο 
#	για το κατέβασμα & την ανάλυση των δεδομένων από το site του τμήματος. 	---

from DownloadDataFromSite import *

########################################################################







class Applet():

	# Δημιουργώ λίστες ( αντικειμένου ) όπου θα κρατάω τα δεδομένα μου ( τις ανακοινώσεις ).
	link_anakinosis = []
	anakinosi = []


	internetConnection = True

	
	def __init__(self):
		'''
		Εδώ δημιουργούνται τα βασικά του Applet.
		'''
	
		self.ind = appindicator.Indicator.new(
		"G-lts CEID-Artas Not-Up",
		"/opt/ceidArtasIndicator/images/student.png",
		appindicator.IndicatorCategory.APPLICATION_STATUS)
		

		self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
		self.ind.set_attention_icon( "/opt/ceidArtasIndicator/images/student-alert.png" ) 
		
		
		self.menu = Gtk.Menu()		
		self.ind.set_menu(self.menu)
		
		self.downloadDataFromSite = DownloadDataFromSite()

		try : 
			self.downloadDataFromSite.downloadPage_and_FindAll()
			self.getData_from_site() # Βλέπω για πρώτη φορά το site και ενημερώνω για πρώτη φορά τις δομές μου!
			GLib.timeout_add_seconds(1800, self.check_for_updates) # Κάθε μισή ώρα ( 1800 δευτερόλεπτα ), καλή την μέθοδο "check_for_updates".

		except urllib.error.URLError :
			self.ind.set_icon("/opt/ceidArtasIndicator/images/student-no-connected.png")
			Applet.internetConnection = False
			GLib.timeout_add_seconds(2, self.waitingForInternetConnection , (True) )

		finally :
			self.set_NewsItems()
			self.set_InfoLabels()





	def waitingForInternetConnection(self , first_time = False) :
		'''
		Μέθοδος που σκοπό έχει να προσπαθεί να κάνει σύνδεση με την σελίδα του Τ.Ε.Ι. 

		Αυτή η μέθοδος καλείτε διαδοχικά ανά 2" όσο δεν υπάρχει σύνδεση στην σελίδα. Αλλά λειτουργεί λίγο διαφορετικά
		αν δεν υπάρχει σύνδεση στη σελίδα *κατά την εκκίνηση* της εφαρμογής, διότι σε αυτή την ειδική περίπτωση εμφανίζονται
		δύο πράγματα μόνο : "Δεν υπάρχει σύνδεση" & "Έξοδος". Αυτά τα δύο πρέπει να αφαιρεθούν λοιπόν και να αναπτυχθεί
		πλήρως πλέον το μενού.
		'''

		try : 
			self.downloadDataFromSite.downloadPage_and_FindAll()
			
		except urllib.error.URLError :
			return True


		# Αν καταφέρει όμως να κάνει σύνδεση : 
		Applet.internetConnection = True

		if ( first_time ) :
			self.removeNoInternetLabels()
			self.getData_from_site()
			self.set_NewsItems()
			self.set_InfoLabels()
		
		self.ind.set_icon( "/opt/ceidArtasIndicator/images/student.png" ) 
		GLib.timeout_add_seconds(1800, self.check_for_updates)

		return False





	def getData_from_site(self):
		'''
		Μέθοδος η οποία ζητάει από το αντικείμενο "self.downloadDataFromSite" και παίρνει τις ανακοινώσεις.

		Οι δομές που υπάρχουν για τις ανακοινώσεις είναι δύο λίστες αντικειμένου οι οποίες είναι οι ακόλουθες :
			 - Λίστα για τα ονόματα των ανακοινώσεων ( Applet.anakinosi ).
			 - Λίστα για τους συνδέσμους *προς* τις ανακοινώσεις ( Applet.link_anakinosis ).
		'''
		# Καθαρίζω αρχικά τις λίστες - δομές μου.
		Applet.link_anakinosis = []
		Applet.anakinosi = []

		# Γέμισμα των δομών :
		Applet.anakinosi = self.downloadDataFromSite.get_Last10_Announcements()
		Applet.link_anakinosis = self.downloadDataFromSite.get_Last10_Links_by_Announcements()





	def updates_are_available(self):
		''' 
		Μέθοδος η οποία ελέγχει αν έχει υπάρξει κάτι καινούριο στο site.
		
		Συγκεκριμένα, κάνει "ανανέωση" στη σελίδα των ανακοινώσεων και παίρνει έπειτα τους ( νέους ίσος) συνδέσμους που βρίσκει.
		Έπειτα συγκρίνει τους *συνδέσμους* των ενημερώσεων που μόλις είδε πως υπάρχουν στην σελίδα, 
		με τους *συνδέσμους* των ενημερώσεων που ΥΠΉΡΧΑΝ στην σελίδα.
		
		- ΑΝ υπάρχει κάποια διαφορά μεταξύ τους, σημαίνει πως βγήκε κάποια καινούρια ενημέρωση,
		οπότε και επιστρέφει True.
		
		- ΑΝ δεν υπάρχει διαφορά μεταξύ τους επιστρέφει False.
		'''
		
		links_only = [] # Εδώ θα κρατήσω προσωρινά τα "νέα" ( ίσος ) links από το site, που θα τσεκάρω τώρα.
	
		try :
			self.downloadDataFromSite.refreshPage() # κατεβάζει και φορτώνει, και τους συνδέσμους των ανακοινώσεων ΚΑΙ τους τίτλους αυτών.

		except urllib.error.URLError :
			raise

		links_only = self.downloadDataFromSite.get_Last10_Links_by_Announcements()

		if ( links_only == Applet.link_anakinosis ) :
			return False
		else :
			return True





	def check_for_updates(self): 
		'''Μέθοδος η οποία ελέγχει για το αν υπάρχει ενημέρωση.

		Τσεκάρει αν υπάρχουν *νέες* ανακοινώσεις και ΑΝ υπάρχουν, ενημερώνει τις δομές όπου κρατούνται οι πληροφορίες τους.
		Προστίθενται οι νέες ανακοινώσεις στο μενού του applet και ειδοποιείτε ο χρήστης για την *τελευταία* ΝΈΑ ανακοίνωση.
		'''
	
		try :
			if ( self.updates_are_available() ): 
				self.getData_from_site()
				self.refresh_News_Items()
				
				self.ind.set_status(appindicator.IndicatorStatus.ATTENTION)
				os.system("notify-send 'C.E.I.D. Άρτας ~ Ενημέρωση.' 'Βγήκε ανακοίνωση με τίτλο : {0}' ".format(Applet.anakinosi[0]) )
				os.system("paplay /usr/share/sounds/ubuntu/stereo/message.ogg")

		except urllib.error.URLError :
			self.ind.set_icon("/opt/ceidArtasIndicator/images/student-no-connected.png")
			Applet.internetConnection = False
			GLib.timeout_add_seconds(2, self.waitingForInternetConnection)

			return False

		
		return True





	def set_NewsItems(self) :
		'''
		Μέθοδος η οποία δημιουργεί τα αντικείμενα του μενού που αφορούν τις ανακοινώσεις.

		Καταρχήν η μέθοδος αυτή καλείτε κατά την εκκίνηση της εφαρμογής. Σκοπό έχει να προσθέτει στο μενού του applet 
		10 αντικείμενα που θα έχουν ως τίτλος τις τελευταίες 10 ανακοινώσεις και σε κάθε ένα από αυτά να του 
		προσθέτει την λειτουργικότητα - να ανοίγει δηλαδή στον default browser την σελίδα της εκάστοτε ανακοίνωσης.
		
		Σημείωση : Στην περίπτωση που δεν υπάρχει σύνδεση, θα εμφανίσει μοναχά "Δεν υπάρχει σύνδεση".
		'''
	
		if Applet.internetConnection :

			self.item0 = Gtk.MenuItem() # Δημιουργία ενός καινούριου αντικειμένου μενού - [ 1ο label ].
			self.item0.set_label(Applet.anakinosi[0])
			self.item0.connect("activate", self.open_announcement , (0) )
			self.menu.append(self.item0)


			self.item1 = Gtk.MenuItem() # [ 2ο label ].
			self.item1.set_label(Applet.anakinosi[1])
			self.item1.connect("activate", self.open_announcement , (1) ) 
			self.menu.append(self.item1)


			self.item2 = Gtk.MenuItem() # [ 3ο label ].
			self.item2.set_label(Applet.anakinosi[2])
			self.item2.connect("activate", self.open_announcement , (2) ) 
			self.menu.append(self.item2)


			self.item3 = Gtk.MenuItem() # [ 4ο label ].
			self.item3.set_label(Applet.anakinosi[3])
			self.item3.connect("activate", self.open_announcement , (3) ) 
			self.menu.append(self.item3)


			self.item4 = Gtk.MenuItem() # [ 5ο label ].
			self.item4.set_label(Applet.anakinosi[4])
			self.item4.connect("activate", self.open_announcement , (4) ) 
			self.menu.append(self.item4)


			self.item5 = Gtk.MenuItem() # [ 6ο label ].
			self.item5.set_label(Applet.anakinosi[5])
			self.item5.connect("activate", self.open_announcement , (5) ) 
			self.menu.append(self.item5)


			self.item6 = Gtk.MenuItem() # [ 7ο label ].
			self.item6.set_label(Applet.anakinosi[6])
			self.item6.connect("activate", self.open_announcement , (6) ) 
			self.menu.append(self.item6)


			self.item7 = Gtk.MenuItem() # [ 8ο label ].
			self.item7.set_label(Applet.anakinosi[7])
			self.item7.connect("activate", self.open_announcement , (7) ) 
			self.menu.append(self.item7)


			self.item8 = Gtk.MenuItem() # [ 9ο label ].
			self.item8.set_label(Applet.anakinosi[8])
			self.item8.connect("activate", self.open_announcement , (8) ) 
			self.menu.append(self.item8)


			self.item9 = Gtk.MenuItem() # [ 10ο label ].
			self.item9.set_label(Applet.anakinosi[9])
			self.item9.connect("activate", self.open_announcement , (9) ) 
			self.menu.append(self.item9)
		
		else : # Αν ΔΕΝ υπάρχει σύνδεση στο διαδίκτυο, τότε ΜΌΝΟ στο ΠΡΏΤΟ αντικείμενο θα γράψω αυτό το μήνυμα : 
			self.item0 = Gtk.MenuItem()
			self.item0.set_label("Δεν υπάρχει σύνδεση")
			self.item0.set_sensitive(False)
			self.menu.append(self.item0)


		self.menu.show_all()





	def refresh_News_Items(self) :
		'''
		Μέθοδος η οποία *ανανεώνει* το κείμενο από τα αντικείμενα των ανακοινώσεων του μενού.

		Αυτή η μέθοδος καλείτε όταν υπάρχει καινούρια ανακοίνωση στο Τ.Ε.Ι. & σκοπό έχει να αλλάζει το κείμενο
		που δείχνουν τα αντικείμενα των ανακοινώσεων του μενού. Δηλαδή να αλλάζει τους τίτλους και να δείχνει 
		τους *νέους* τελευταίους 10 τίτλους των ανακοινώσεων.
		'''

		self.item0.set_label( Applet.anakinosi[0] )
		self.item1.set_label( Applet.anakinosi[1] )
		self.item2.set_label( Applet.anakinosi[2] )
		self.item3.set_label( Applet.anakinosi[3] )
		self.item4.set_label( Applet.anakinosi[4] )
		self.item5.set_label( Applet.anakinosi[5] )
		self.item6.set_label( Applet.anakinosi[6] )
		self.item7.set_label( Applet.anakinosi[7] )
		self.item8.set_label( Applet.anakinosi[8] )
		self.item9.set_label( Applet.anakinosi[9] )





	def set_InfoLabels(self):
		'''
		Μέθοδος η οποία προσθέτει κάποια βασικά πράγματα στο μενού του applet για την εύκολη πρόσβαση του χρήστη.

		Αυτά που προστίθενται από αυτή την μέθοδο είναι στάνταρ.
		'''

		if Applet.internetConnection :

			# Πάμε τώρα να προσθέσουμε και άλλα πράγματα για την εύκολη πρόσβαση του χρήστη στο μενού.

			self.seperator_line1 = Gtk.SeparatorMenuItem()
			self.menu.append( self.seperator_line1 )

			self.pages = Gtk.Menu()
			self.sub_menu_items = Gtk.MenuItem('Άνοιγμα σελίδας')
			self.menu.append(self.sub_menu_items)
			self.sub_menu_items.set_submenu(self.pages)

			self.item_news = Gtk.MenuItem()
			self.item_news.set_label("Ανακοινώσεων")
			self.item_news.connect("activate", self.tei_news)
			self.pages.append(self.item_news)
			
			self.item_eclass = Gtk.MenuItem()
			self.item_eclass.set_label("Ασύγχρονης Τηλεκπαίδευσης")
			self.item_eclass.connect("activate", self.eclass)
			self.pages.append(self.item_eclass)		

			self.item_stu = Gtk.MenuItem()
			self.item_stu.set_label("Βαθμολογιών")
			self.item_stu.connect("activate", self.tei_stu)
			self.pages.append(self.item_stu)

			self.seperator_line = Gtk.SeparatorMenuItem()
			self.menu.append(self.seperator_line)

			self.item_info = Gtk.MenuItem()
			self.item_info.set_label("Πληροφορίες εφαρμογής")
			self.item_info.connect("activate", self.inform)
			self.menu.append(self.item_info)


		self.q_item = Gtk.MenuItem()
		self.q_item.set_label("Έξοδος")
		self.q_item.connect("activate", self.quit)
		self.menu.append(self.q_item)
		
		self.menu.show_all()





	def open_announcement(self, widget , announcement):
		'''
		Μέθοδος η οποία ανοίγει την εκάστοτε ανακοίνωση στον browser του χρήστη.

		Η παράμετρος "announcement" λέει ποια ανακοίνωση να ανοίξει στον borwser του χρήστη. 
		Όταν καλείτε αυτή η μέθοδος , ανάλογα σε ποια ανακοίνωση έχει κάνει "click" ο χρήστης ( 0,1,2...9 ) δίνεται ο -*- ΆΡΙΘΜΌΣ -*- αυτός,
		στην παράμετρο "announcement".
		'''
		webbrowser.open_new_tab(Applet.link_anakinosis[announcement]) # Για να ανοίξει τον σύνδεσμο σε νέα καρτέλα του βασικού browser. 
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE) # Για να αλλάξει την κατάσταση του εικονιδίου στο indicator applet.





	def inform(self, widget):
		webbrowser.open_new_tab("https://github.com/Tas-sos/CEID-Artas_Announcements")
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
	




	def quit(self, widget):
		Gtk.main_quit()





	def removeNoInternetLabels(self) :
		'''
		Η μέθοδος αυτή χρησιμοποιείτε μονάχα ΑΝ *κατά την εκκίνηση* του προγράμματος δεν υπάρχει σύνδεση στην σελίδα του Τ.Ε.Ι..
		Επειδή σε αυτή την περίπτωση το μόνο που δείχνει το applet είναι "Δεν υπάρχει σύνδεση" και το "κουμπί" εξόδου - τερματισμού του applet. 
		ΑΝ υπάρξει σύνδεση όμως αυτά πρέπει να φύγουν και να αναπτυχθεί το μενού όπως πρέπει.
		'''
		self.menu.remove(self.item0) # Διαγραφή του 1ου Label
		self.menu.remove(self.q_item) # Διαγραφή του Quit Label







#################################################### Κυρίως ####################################################

inticator_applet = Applet()

Gtk.main()


