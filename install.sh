#!/bin/bash

# Αυτό το script δημιουργήθηκε με σκοπό να βοηθήσει τον χρήστη
# με την εγκατάσταση του Indicator Applet στον υπολογιστή του.
# Ελπίζουμε να βοηθήσει.  :)

# Created by G-lts Team
# Copyleft (ↄ)


sudo mkdir /opt/ceidArtasIndicator
sudo mv src images unistall.sh /opt/ceidArtasIndicator/

sudo chmod u+x /opt/ceidArtasIndicator/unistall.sh

# Για να προστεθεί το πρόγραμμα στα προγράμματα εκκίνησης, ούτως ώστε να ξεκινάει αυτόματα : 

mv ciedArtas.desktop ~/.config/autostart

# Εγκατάσταση απαραίτητων βιβλιοθηκών :
sudo apt-get install python3-bs4
sudo apt-get install python-lxml
sudo apt-get install python3-lxml
sudo apt-get install python3 libgtk-3-0 python-appindicator

python3 /opt/ceidArtasIndicator/src/AnnouncementsForCEID-Artas.py &


notify-send 'Announcements For CEID Artas' 'Η εγκατάσταση ολοκληρώθηκε επιτυχώς. Για ότι χρειαστείτε ήμαστε δίπλα σας.\nEυχαριστούμε πολύ. :)' -i /usr/share/icons/gnome/48x48/emblems/emblem-default.png
paplay /usr/share/sounds/freedesktop/stereo/complete.oga

cd ..
rm -R CEID-Artas_Announcements-master
rm CEID-Artas_Announcements-master.zip



