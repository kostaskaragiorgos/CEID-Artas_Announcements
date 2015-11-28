#!/bin/bash

# Αυτό το script δημιουργήθηκε με σκοπό να βοηθήσει τον χρήστη
# με την εγκατάσταση του Indicator Applet στον υπολογιστή του.
# Ελπίζουμε να βοηθήσει.  :)

# Created by G-lts Team
# Copyleft (ↄ)


sudo mkdir /opt/ceidArtasIndicator
sudo mv src images unistall.sh /opt/ceidArtasIndicator/

# Για να προστεθεί το πρόγραμμα στα προγράμματα εκκίνησης, ούτως ώστε να ξεκινάει αυτόματα : 

mv ciedArtas.desktop ~/.config/autostart

python3 /opt/ceidArtasIndicator/src/AnnouncementsForCEID-Artas.py &


notify-send 'Announcements For CEID Artas' 'Η εγκατάσταση ολοκληρώθηκε επιτυχώς. Για ότι χρειαστείτε ήμαστε δίπλα σας.\nEυχαριστούμε πολύ. :)' -i /usr/share/icons/gnome/48x48/emblems/emblem-default.png
paplay /usr/share/sounds/freedesktop/stereo/complete.oga


#rm README.md .gitignore
# Για να διαγραφούν όλα τα αρχεία που κατέβασε ο χρήστης και είναι για την εγκατάταση :
cd ..
rm -R CEID-Artas_Not-Up-master





