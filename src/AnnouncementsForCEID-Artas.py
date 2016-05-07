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
# 			για το κατέβασμα των δεδομένων από το site του CEID. 	---

from ceidPage import *

########################################################################

# --- Κάνω import το module που έκανα εγώ και το οποίο είναι υπεύθυνο 
# 	για το κατέβασμα των δεδομένων από το site του Τ.Ε.Ι. Ηπείρου. 	---

from teiepPage import *

########################################################################





class Applet():

	# Δημιουργώ δομές ( συγκεκριμένα λίστες -αντικειμένου- ) όπου θα κρατάω τα δεδομένα των ανακοινώσεων.
	links_CEID = []
	announcements_CEID = []

	links_TEIep = []
	announcements_TEIep = []

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

		# Δημιουργία αντικειμένων από τις κλάσεις που έχω δημιουργήσει και είναι αρμόδιες για ότι χρειαστεί από την κάθε σελίδα.
		self.CEID = DownloadDataFromSiteCEID()
		self.TEIep = DownloadDataFromSiteTEIEP()


		# For CEID page :
		try : 
			self.CEID.downloadPage_and_FindAll() # Κατεβάζω την σελίδα από το CEID
			self.TEIep.downloadPage_and_FindAll()  # Κατεβάζω την σελίδα από το ΤΕΙ Ηπείρου
			
			self.getData_from_site() # Παίρνω τα δεδομένα που χρειάζομαι από κάθε σελίδα και τα φορτώνω στις κατάληλες δομές που έχω για αυτά.
			
			GLib.timeout_add_seconds(1800, self.check_for_updates) # Κάθε μισή ώρα ( 1800 δευτερόλεπτα ), καλεί την μέθοδο "check_for_updates" ( Η ΟΠΟΊΑ *ΠΡΈΠΕΙ* ΝΑ ΓΥΡΝΆΕΙ ΚΆΤΙ! )


		except urllib.error.URLError : # Αν μας "πασάρουν" κάποιο σφάλμα οι κλήσεις των μεθόδων "downloadPage_and_FindAll()" ( αυτό θα είναι ότι δεν μπορούν να συνδεθούν στην εκάστοτε σελίδα ) :
			self.ind.set_icon("/opt/ceidArtasIndicator/images/student-no-connected.png") # Αλλαγή του εικονιδίου ώστε να δείξουμε πως δεν υπάρχει σύνδεση με τις σελίδες! ;)
			Applet.internetConnection = False
			GLib.timeout_add_seconds(2, self.waitingForInternetConnection , (True) )  # και κάθε 2" θα προσπαθούμε να κάνουμε σύνδεση στο εκάστοτε site.
		
		finally :
			self.set_CEIDAnnouncementsItems() # Προσθήκη πρώτα των ανακοινώσεων.
			self.set_TEIepAnnouncementsItems()
			
			self.set_InfoLabels() # Έπειτα προσθήκη των βασικών στοιχείων στο μενού.

		# For TEIep Page :
		# Μάλλον το καλύτερο θα ήταν να είναι εντελώς ξέχωρα για το κάθε site, αλλά για λόγους ευκολίας τώρα...θα το αφήσω έτσι..
		# Έστω ένα από τα δύο να μην είναι ανοιχτό το applet θα "κρεμάει", όλο! Βαριέμαι τώρα να ασχοληθώ και με αυτό..
		# Ας ελπίσουμε να είναι οκ *και* οι δυο σελίδες πάντα! Δε φταίω εγώ, αυτοί φταίνε! ( χαχαχα ) να κάνουν σοβαρή δουλειά στο κάτω κάτω 
		# και να είναι πάντα online οι σελίδες!! Α.. στο καλό! Δεν ασχολούμαι τώρα με το ακραίο αυτό φαινόμενο :P




	def waitingForInternetConnection(self , first_time = False) :
		'''
		Μέθοδος που σκοπό έχει να προσπαθεί να κάνει σύνδεση με την σελίδα του Τ.Ε.Ι. 

		Αυτή η μέθοδος καλείτε διαδοχικά ανά 2" όσο δεν υπάρχει σύνδεση στην σελίδα. Αλλά λειτουργεί λίγο διαφορετικά
		αν δεν υπάρχει σύνδεση στη σελίδα *κατά την εκκίνηση* της εφαρμογής, διότι σε αυτή την ειδική περίπτωση εμφανίζονται
		δύο πράγματα μόνο : "Δεν υπάρχει σύνδεση" & "Έξοδος". Αυτά τα δύο πρέπει να αφαιρεθούν λοιπόν και να αναπτυχθεί
		πλήρως πλέον το μενού.
		'''

		try : 
			self.CEID.downloadPage_and_FindAll()
			self.TEIep.downloadPage_and_FindAll()
			
		except urllib.error.URLError :
			return True # που σημαίνει συνέχισε την διεργασία..  ( αν γυρνάει True τότε θα ξανακαλείτε αυτή η μέθοδος, αλλιώς με False όχι - έτσι δουλεύει η "GLib.timeout_add_seconds()" )


		# Αν καταφέρει και κάνει σύνδεση : 
		Applet.internetConnection = True

		if ( first_time ) : # Μόνο στην πρώτη φορά ( αν με το που ανοίξει η εφαρμογή, δεν μπορεί να συνδεθεί στο site δηλ. ) πρέπει να κάνει *ΚΑΙ* αυτά : 
			self.removeNoInternetLabels()
			self.getData_from_site()

			self.set_CEIDAnnouncementsItems()
			self.set_TEIepAnnouncementsItems()
			self.set_InfoLabels()
		
		self.ind.set_icon( "/opt/ceidArtasIndicator/images/student.png" ) 
		GLib.timeout_add_seconds(1800, self.check_for_updates) # Πλέον, κάθε μισή ώρα ( 1800 δευτερόλεπτα ), θα καλή την μέθοδο "check_for_updates" ( Η ΟΠΟΊΑ *ΠΡΈΠΕΙ* ΝΑ ΓΥΡΝΆΕΙ ΚΆΤΙ! )

		return False # που σημαίνει, σταμάτησε την διεργασία :)  ( δεν θα ξανά εκτελεστή αυτή η μέθοδος - εφόσον γυρίσει False - )




	def getData_from_site(self):
		'''
		Μέθοδος η οποία ζητάει από το αντικείμενο "self.CEID" & "self.TEIep" και παίρνει τις απαραίτητες πληροφορίες για τις ανακοινώσεις.

		Οι δομές που υπάρχουν για τις ανακοινώσεις κάθε σελίδας είναι δύο λίστες αντικειμένου οι οποίες είναι οι ακόλουθες για την κάθε σελίδα : 
			 > CEID page :
				 - Λίστα για τα ονόματα των ανακοινώσεων ( Applet.announcements_CEID ).
				 - Λίστα για τους συνδέσμους *προς* τις ανακοινώσεις ( Applet.links_CEID ).
			 > TEIep page :
				 - Λίστα για τα ονόματα των ανακοινώσεων ( Applet.announcements_TEIep ).
				 - Λίστα για τους συνδέσμους *προς* τις ανακοινώσεις ( Applet.links_TEIip ).
		'''

		# Καθαρίζω αρχικά τις λίστες μου.
		Applet.links_CEID = []
		Applet.announcements_CEID = []

		Applet.links_TEIep = []
		Applet.announcements_TEIep = []

		# Γέμισμα των δομών :

		# CEID page :
		Applet.announcements_CEID = self.CEID.get_Last10_Announcements()
		Applet.links_CEID = self.CEID.get_Last10_Links_by_Announcements()

		# TEIep page :
		Applet.links_TEIep = self.TEIep.links
		Applet.announcements_TEIep = self.TEIep.announcements




	def updates_are_available(self):
		''' 
		Μέθοδος η οποία ελέγχει αν έχει υπάρξει κάτι καινούριο στις σελίδες.
		
		Συγκεκριμένα, κάνει "ανανέωση" στις σελίδες των ανακοινώσεων και παίρνει έπειτα τους ( νέους *ίσος*) συνδέσμους που βρίσκει.
		Έπειτα συγκρίνει τους *συνδέσμους* των ανακοινώσεων που μόλις είδε πως υπάρχουν στην σελίδα, 
		με τους *συνδέσμους* των ανακοινώσεων που ΥΠΉΡΧΑΝ στην σελίδα.
		
		- ΑΝ υπάρχει κάποια διαφορά μεταξύ τους, σημαίνει πως βγήκε κάποια καινούρια ανακοίνωση,
		οπότε και επιστρέφει :
			True και 2 : Αν και οι δύο σελίδες έχουν νέα ανακοίνωση.
			True και 0 : Αν *μόνο* το CEID έχει νέα ανακοίνωση.
			True και 1 : Αν *μόνο* το ΤΕΗ ΗΠΕΊΡΟΥ έχει νέα ανακοίνωση.
		
		- ΑΝ δεν υπάρχει διαφορά μεταξύ τους επιστρέφει False.
		'''
		
		links_onlyCEID = [] # Εδώ θα κρατήσω τα "νέα" ( ίσος ) links από την σελίδα του CEID, που θα τσεκάρω τώρα.
		links_onlyTEIep = []  # και εδώ από την σελίδα του ΤΕΙ ΗΠΕΙΡΟΥ

		try :
			self.CEID.refreshPage()
			self.TEIep.refreshPage()
		
		except urllib.error.URLError : # Αν δημιουργηθεί κάποιο σφάλμα, τότε :
			raise # άστο δε θα ασχοληθώ εδώ με αυτό, θα τερματίσω αυτή την μέθοδο. Και έπειτα θα πασάρω το σφάλμα που προκλήθηκε σε αυτόν που με κάλεσε.


		links_onlyCEID = self.CEID.get_Last10_Links_by_Announcements()
		links_onlyTEIep = self.TEIep.links


		# Αν ισχύει πάει να πει πως ΚΑΙ στις *ΔΎΟ* λίστες ανακοινώσεων δεν έχει αλλάξει κάτι, είναι ακριβώς ίδιες.
		if ( ( links_onlyCEID == Applet.links_CEID ) and ( links_onlyTEIep == Applet.links_TEIep ) ) :
			return ( False , None ) # Άρα δεν υπάρχει κάτι νέο.

		# Αν και τα δύο έχουν νέες ανακοινώσεις!
		elif ( ( links_onlyCEID != Applet.links_CEID ) and ( links_onlyTEIep != Applet.links_TEIep ) ) : 
			return ( True , 2 )

		# Αν μόνο το CEID έχει κάποια νέα ανακοίνωση :
		elif ( links_onlyCEID != Applet.links_CEID ) : 
			return ( True , 0)

		# Αν το ΤΕΗ Ηπείρου έχει νέα ανακοίνωση : 
		else :
			return ( True , 1 )




	def check_for_updates(self): 
		'''Μέθοδος η οποία ελέγχει για το αν υπάρχει νέα ανακοίνωση.

		Τσεκάρει αν υπάρχουν *νέες* ανακοινώσεις και ΑΝ υπάρχουν, ενημερώνει τις δομές όπου κρατούνται οι πληροφορίες τους.
		Προστίθενται οι νέες ανακοινώσεις στο μενού του applet και ειδοποιείτε ο χρήστης για την *τελευταία* ΝΈΑ ανακοίνωση.
		'''
	
		try :

			there_is , where = self.updates_are_available()

			if ( there_is ) :
								
				# Ενημερώνω τις λίστες από την αρχή και τώρα θα περιέχουν τις νέες ανακοινώσεις : 
				self.getData_from_site() # οκ για λόγους ευκολίας ας ενημερώνονται οι δομές *και για τις δύο σελίδες* ταυτόχρονα.
				# Άλλωστε παρακάτω βλέπω ποια από τις δύο έχει κάτι νέο και εμφανίζω από εκείνη μεμονωμένα τα μηνύματα που θέλω.

				if ( where == 2 ) : # Αν βγήκε και στις δύο σελίδες νέα ανακοίνωση!
					self.refresh_CEID_Items()
					self.refresh_TEIep_Items()

					self.ind.set_status(appindicator.IndicatorStatus.ATTENTION) # Κάνε κόκκινο το εικονίδιο.	
					os.system("notify-send 'C.E.I.D. Άρτας ~ Ενημέρωση.' 'Βγήκε ανακοίνωση με τίτλο : {0}' ".format(Applet.announcements_CEID[0]) )

					self.ind.set_status(appindicator.IndicatorStatus.ATTENTION)
					os.system("notify-send 'Τ.Ε.Ι. Ηπείρου ~ Ενημέρωση.' 'Βγήκε ανακοίνωση με τίτλο : {0}' ".format(Applet.announcements_TEIep[0]) )


				elif ( where == 0 ) : # Αν βγήκε *μόνο* στο CEID νέα ανακοίνωση!
					self.refresh_CEID_Items()

					self.ind.set_status(appindicator.IndicatorStatus.ATTENTION)
					os.system("notify-send 'C.E.I.D. Άρτας ~ Ενημέρωση.' 'Βγήκε ανακοίνωση με τίτλο : {0}' ".format(Applet.announcements_CEID[0]) )


				elif ( where == 1 ) : # Αν βγήκε *μόνο* στο TEIep νέα ανακοίνωση!
					self.refresh_TEIep_Items()

					self.ind.set_status(appindicator.IndicatorStatus.ATTENTION)
					os.system("notify-send 'Τ.Ε.Ι. Ηπείρου ~ Ενημέρωση.' 'Βγήκε ανακοίνωση με τίτλο : {0}' ".format(Applet.announcements_TEIep[0]) )


				os.system("paplay /usr/share/sounds/ubuntu/stereo/message.ogg")


		# το σφάλμα που χειρίζομαι εδώ, είναι για χάρη της μεθόδου "updates_are_available()".
		except urllib.error.URLError : # Αν δημιουργηθεί τώρα σφάλμα ενώ πριν *ήμασταν* οκ, τότε : απλώς ειδοποιώ με το εικονίδιο πως δεν υπάρχει σύνδεση και περιμένω μέχρι να ξανά έχω :

			self.ind.set_icon("/opt/ceidArtasIndicator/images/student-no-connected.png")

			Applet.internetConnection = False
			GLib.timeout_add_seconds(2, self.waitingForInternetConnection)

			return False


		return True # ΠΡΈΠΕΙ -*ΟΠΩΣΔΉΠΟΤΕ*- ΕΔΏ να γυρνάει True ή False , ώστε να παίζει η ΕΠΑΝΆΛΗΨΗ!!.	



	
	def set_CEIDAnnouncementsItems(self) :
		'''
		Μέθοδος η οποία δημιουργεί τα αντικείμενα του μενού που αφορούν τις ανακοινώσεις του τμήματος Μηχανικών Πληροφορικής ( CEID ).

		Καταρχήν η μέθοδος αυτή καλείτε κατά την εκκίνηση της εφαρμογής. Σκοπό έχει να προσθέτει στο μενού του applet 
		10 αντικείμενα που θα έχουν ως τίτλος τις τελευταίες 10 ανακοινώσεις του τμήματος.
		Σε κάθε αντικείμενο που αναγράφει τον τίτλο της εκάστοτε ανακοίνωσης, προστίθεται η λειτουργικότητα πως ΑΝ κάποιος κάνει κλικ πάνω του,
		θα του ανοίξει στον προεπιλεγμένο περιηγητή ιστοσελίδων του συστήματος του, την ανακοίνωση αυτή σε νέα καρτέλα.
		
		Σημείωση : Στην περίπτωση που δεν υπάρχει σύνδεση, θα εμφανίσει μοναχά "Δεν υπάρχει σύνδεση".
		'''

		if Applet.internetConnection : # Αν υπάρχει σύνδεση στο διαδίκτυο.

			self.item0 = Gtk.MenuItem() # Δημιουργία ενός καινούριου αντικειμένου μενού - [ 1ο label ].
			self.item0.set_label(Applet.announcements_CEID[0])
			self.item0.connect("activate", self.open_announcementCEID , (0) )
			self.menu.append(self.item0)


			self.item1 = Gtk.MenuItem() # [ 2ο label ].
			self.item1.set_label(Applet.announcements_CEID[1])
			self.item1.connect("activate", self.open_announcementCEID , (1) ) 
			self.menu.append(self.item1)


			self.item2 = Gtk.MenuItem() # [ 3ο label ].
			self.item2.set_label(Applet.announcements_CEID[2])
			self.item2.connect("activate", self.open_announcementCEID , (2) ) 
			self.menu.append(self.item2)


			self.item3 = Gtk.MenuItem() # [ 4ο label ].
			self.item3.set_label(Applet.announcements_CEID[3])
			self.item3.connect("activate", self.open_announcementCEID , (3) ) 
			self.menu.append(self.item3)


			self.item4 = Gtk.MenuItem() # [ 5ο label ].
			self.item4.set_label(Applet.announcements_CEID[4])
			self.item4.connect("activate", self.open_announcementCEID , (4) ) 
			self.menu.append(self.item4)


			self.item5 = Gtk.MenuItem() # [ 6ο label ].
			self.item5.set_label(Applet.announcements_CEID[5])
			self.item5.connect("activate", self.open_announcementCEID , (5) ) 
			self.menu.append(self.item5)


			self.item6 = Gtk.MenuItem() # [ 7ο label ].
			self.item6.set_label(Applet.announcements_CEID[6])
			self.item6.connect("activate", self.open_announcementCEID , (6) ) 
			self.menu.append(self.item6)


			self.item7 = Gtk.MenuItem() # [ 8ο label ].
			self.item7.set_label(Applet.announcements_CEID[7])
			self.item7.connect("activate", self.open_announcementCEID , (7) ) 
			self.menu.append(self.item7)


			self.item8 = Gtk.MenuItem() # [ 9ο label ].
			self.item8.set_label(Applet.announcements_CEID[8])
			self.item8.connect("activate", self.open_announcementCEID , (8) ) 
			self.menu.append(self.item8)


			self.item9 = Gtk.MenuItem() # [ 10ο label ].
			self.item9.set_label(Applet.announcements_CEID[9])
			self.item9.connect("activate", self.open_announcementCEID , (9) ) 
			self.menu.append(self.item9)
		
		else : # Αν ΔΕΝ υπάρχει σύνδεση με την σελίδα, τότε δημιουργώ ΜΌΝΟ ένα αντικείμενο το οποία απλά θα λέει "Δεν υπάρχει σύνδεση".
			self.item0 = Gtk.MenuItem()
			self.item0.set_label("Δεν υπάρχει σύνδεση")
			self.item0.set_sensitive(False)
			self.menu.append(self.item0)


		self.menu.show_all()




	def set_TEIepAnnouncementsItems(self):
		'''
		Μέθοδος η οποία είναι παρόμοια με την "set_CEIDAnnouncementsItems", μόνο που αυτή είναι για της ανακοινώσεις του Τ.Ε.Ι. Ηπείρου.

		Συγκεκριμένα αυτή η μέθοδος, δημιουργεί ένα υπό-μενού με όνομα "Ανακοινώσεις Τ.Ε.Ι. Ηπείρου", το οποίο αν το ανοίξει κάποιος θα βλέπει
		τις τελευταίες 7 ανακοινώσεις του Τ.Ε.Ι. Ηπείρου. 
		Σε κάθε αντικείμενο που αναγράφει τον τίτλο της εκάστοτε ανακοίνωσης, προστίθεται η λειτουργικότητα πως ΑΝ κάποιος κάνει κλικ πάνω του,
		θα του ανοίξει στον προεπιλεγμένο περιηγητή ιστοσελίδων του συστήματος του, την ανακοίνωση αυτή σε νέα καρτέλα.
		'''

		if Applet.internetConnection :

			self.menu.append( Gtk.SeparatorMenuItem() ) # Προσθήκη διαχωριστικής γραμμής στο μενού.


			self.sub_TeiEpMenu = Gtk.Menu()
			self.menu_TEIep_items = Gtk.MenuItem('Ανακοινώσεις Τ.Ε.Ι. Ηπείρου')
			self.menu.append(self.menu_TEIep_items)
			self.menu_TEIep_items.set_submenu(self.sub_TeiEpMenu)


			
			self.teiEPitem0 = Gtk.MenuItem()
			self.teiEPitem0.set_label( Applet.announcements_TEIep[0] )
			self.teiEPitem0.connect("activate", self.open_announcementTEIep , (0) )
			self.sub_TeiEpMenu.append(self.teiEPitem0)


			self.teiEPitem1 = Gtk.MenuItem()
			self.teiEPitem1.set_label( Applet.announcements_TEIep[1] )
			self.teiEPitem1.connect("activate", self.open_announcementTEIep , (1) )
			self.sub_TeiEpMenu.append(self.teiEPitem1)


			self.teiEPitem2 = Gtk.MenuItem()
			self.teiEPitem2.set_label( Applet.announcements_TEIep[2] )
			self.teiEPitem2.connect("activate", self.open_announcementTEIep , (2) )
			self.sub_TeiEpMenu.append(self.teiEPitem2)


			self.teiEPitem3 = Gtk.MenuItem()
			self.teiEPitem3.set_label(Applet.announcements_TEIep[3])
			self.teiEPitem3.connect("activate", self.open_announcementTEIep , (3) )
			self.sub_TeiEpMenu.append(self.teiEPitem3)


			self.teiEPitem4 = Gtk.MenuItem()
			self.teiEPitem4.set_label( Applet.announcements_TEIep[4] )
			self.teiEPitem4.connect("activate", self.open_announcementTEIep , (4) )
			self.sub_TeiEpMenu.append(self.teiEPitem4)


			self.teiEPitem5 = Gtk.MenuItem()
			self.teiEPitem5.set_label( Applet.announcements_TEIep[5] )
			self.teiEPitem5.connect("activate", self.open_announcementTEIep , (5) )
			self.sub_TeiEpMenu.append(self.teiEPitem5)


			self.teiEPitem6 = Gtk.MenuItem()
			self.teiEPitem6.set_label( Applet.announcements_TEIep[6] )
			self.teiEPitem6.connect("activate", self.open_announcementTEIep , (6) )
			self.sub_TeiEpMenu.append(self.teiEPitem6)

			self.menu.show_all()




	def set_InfoLabels(self):
		'''
		Μέθοδος η οποία προσθέτει κάποια βασικά πράγματα στο μενού του applet για την εύκολη πρόσβαση του χρήστη.

		Αυτά που προστίθενται από αυτή την μέθοδο είναι στάνταρ.
		'''

		if Applet.internetConnection :

			self.menu.append(Gtk.SeparatorMenuItem())

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

			self.item_teiPage = Gtk.MenuItem()
			self.item_teiPage.set_label("Τ.Ε.Ι. Ηπείρου")
			self.item_teiPage.connect("activate", self.teiPage)
			self.pages.append(self.item_teiPage)


			self.menu.append(Gtk.SeparatorMenuItem())

			
			self.item_info = Gtk.MenuItem()
			self.item_info.set_label("Πληροφορίες εφαρμογής")
			self.item_info.connect("activate", self.inform)
			self.menu.append(self.item_info)
		

		self.q_item = Gtk.MenuItem()
		self.q_item.set_label("Έξοδος")
		self.q_item.connect("activate", self.quit)
		self.menu.append(self.q_item)

		
		self.menu.show_all()




	def open_announcementCEID(self, widget , announcement):
		'''
		Μέθοδος η οποία ανοίγει την εκάστοτε ανακοίνωση του CEID στον browser του χρήστη.

		Η παράμετρος "announcement" λέει ποια ανακοίνωση να ανοίξει στον borwser του χρήστη. 
		Όταν καλείτε αυτή η μέθοδος , ανάλογα σε ποια ανακοίνωση έχει κάνει "click" ο χρήστης ( 0,1,2...9 ) δίνεται ο -*- ΆΡΙΘΜΌΣ -*- αυτός,
		στην παράμετρο "announcement". Έτσι ο αριθμός αυτό στην λίστα "Applet.links_CEID", δείνει τον σύνδεσμο της. ;)
		'''

		webbrowser.open_new_tab(Applet.links_CEID[announcement]) # Για να ανοίξει τον σύνδεσμο σε νέα καρτέλα του βασικού browser. 
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE) # Για να αλλάξει την κατάσταση του εικονιδίου στο indicator applet.




	def open_announcementTEIep(self, widget , announcement):
		'''
		Μέθοδος η οποία ανοίγει την εκάστοτε ανακοίνωση του TEIep στον browser του χρήστη.

		Η παράμετρος "announcement" λέει ποια ανακοίνωση να ανοίξει στον borwser του χρήστη. 
		Όταν καλείτε αυτή η μέθοδος , ανάλογα σε ποια ανακοίνωση έχει κάνει "click" ο χρήστης ( 0,1,2...7 ) δίνεται ο -*- ΆΡΙΘΜΌΣ -*- αυτός,
		στην παράμετρο "announcement". Έτσι ο αριθμός αυτό στην λίστα "Applet.links_TEIep", δείνει τον σύνδεσμο της. ;)
		'''

		webbrowser.open_new_tab(Applet.links_TEIep[announcement])
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)




	def refresh_CEID_Items(self) :
		'''
		Μέθοδος η οποία *ανανεώνει* το κείμενο από τα αντικείμενα των ανακοινώσεων του CEID.

		Αυτή η μέθοδος καλείτε όταν υπάρχει καινούρια ανακοίνωση στο CEID & σκοπό έχει να αλλάζει το κείμενο
		που δείχνουν τα αντικείμενα των ανακοινώσεων του μενού. Δηλαδή να αλλάζει τους τίτλους και να δείχνει 
		τους *νέους* τελευταίους 10 τίτλους των ανακοινώσεων.
		'''

		self.item0.set_label( Applet.announcements_CEID[0] )
		self.item1.set_label( Applet.announcements_CEID[1] )
		self.item2.set_label( Applet.announcements_CEID[2] )
		self.item3.set_label( Applet.announcements_CEID[3] )
		self.item4.set_label( Applet.announcements_CEID[4] )
		self.item5.set_label( Applet.announcements_CEID[5] )
		self.item6.set_label( Applet.announcements_CEID[6] )
		self.item7.set_label( Applet.announcements_CEID[7] )
		self.item8.set_label( Applet.announcements_CEID[8] )
		self.item9.set_label( Applet.announcements_CEID[9] )




	def refresh_TEIep_Items(self) :
		'''
		Μέθοδος η οποία *ανανεώνει* το κείμενο από τα αντικείμενα των ανακοινώσεων του μενού που είναι από το Τ.Ε.Ι. Ηπείρου.

		Αυτή η μέθοδος καλείτε όταν υπάρχει καινούρια ανακοίνωση στο TEIep & σκοπό έχει να αλλάζει το κείμενο
		που δείχνουν τα αντικείμενα των ανακοινώσεων του μενού. Δηλαδή να αλλάζει τους τίτλους και να δείχνει 
		τους *νέους* τελευταίους 7 τίτλους των ανακοινώσεων.
		'''

		self.teiEPitem0.set_label( Applet.announcements_Teiep[0] )
		self.teiEPitem1.set_label( Applet.announcements_TEIep[1] )
		self.teiEPitem2.set_label( Applet.announcements_TEIep[2] )
		self.teiEPitem3.set_label( Applet.announcements_TEIep[3] )
		self.teiEPitem4.set_label( Applet.announcements_TEIep[4] )
		self.teiEPitem5.set_label( Applet.announcements_TEIep[5] )
		self.teiEPitem6.set_label( Applet.announcements_TEIep[6] )




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




	def teiPage(self, widget):
		webbrowser.open_new_tab("http://www.teiep.gr/")
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)




	def quit(self, widget):
		'''
		Μέθοδος του κουμπιού εξόδου ( και τερματισμού του προγράμματος ).
		'''
		Gtk.main_quit()




	def removeNoInternetLabels(self) :
		'''
		Η μέθοδος αυτή χρησιμοποιείτε μονάχα ΑΝ *κατά την εκκίνηση* του προγράμματος δεν υπάρχει σύνδεση στις σελίδες του Τ.Ε.Ι..
		Επειδή σε αυτή την περίπτωση το μόνο που δείχνει το applet είναι "Δεν υπάρχει σύνδεση" και το "κουμπί" εξόδου - τερματισμού του applet. 
		ΑΝ υπάρξει σύνδεση όμως αυτά πρέπει να φύγουν και να αναπτυχθεί το μενού όπως πρέπει. Γιαυτό λοιπόν και η κατασκευή αυτής της μεθόδου.
		'''

		self.menu.remove(self.item0) # Διαγραφή του 1ου Label
		self.menu.remove(self.q_item) # Διαγραφή του Quit Label






#################################################### Κυρίως ####################################################

inticator_applet = Applet()

Gtk.main()




