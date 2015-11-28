#!/bin/bash

# Αυτό το script δημιουργήθηκε με σκοπό να βοηθήσει τον χρήστη
# με την εγκατάσταση του Indicator Applet στον υπολογιστή του.
# Ελπίζουμε να βοηθήσει.  :)

# Created by G-lts Team
# Copyleft (ↄ)


sudo mkdir /opt/ceidArtasIndicator
sudo mv src images unistall.sh /opt/ceidArtasIndicator/

sudo chmod o+x /opt/ceidArtasIndicator/unistall.sh

# Για να προστεθεί το πρόγραμμα στα προγράμματα εκκίνησης, ούτως ώστε να ξεκινάει αυτόματα : 

mv ciedArtas.desktop ~/.config/autostart

python3 /opt/ceidArtasIndicator/src/AnnouncementsForCEID-Artas.py &


notify-send 'Announcements For CEID Artas' 'Η εγκατάσταση ολοκληρώθηκε επιτυχώς. Για ότι χρειαστείτε ήμαστε δίπλα σας.\nEυχαριστούμε πολύ. :)' -i /usr/share/icons/gnome/48x48/emblems/emblem-default.png
paplay /usr/share/sounds/freedesktop/stereo/complete.oga

cd ..
rm -R CEID-Artas_Not-Up-master
rm CEID-Artas_Not-Up-master.zip





