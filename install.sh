#!/bin/bash

# Αυτό το script δημιουργήθηκε με σκοπό να βοηθήσει τον χρήστη
# με την εγκατάσταση του Indicator Applet στον υπολογιστή του.
# Ελπίζουμε να βοηθήσει.  :)

# Created by G-lts Team
# Copyleft (ↄ)

stty -echo
read -p "Password please : " pass
stty echo
printf '\n'

sudo mkdir /opt/ceidArtasIndicator
sudo mv src images unistall.sh /opt/ceidArtasIndicator/

# Για να προστεθεί το πρόγραμμα στα προγράμματα εκκίνησης, ούτως ώστε να ξεκινάει αυτόματα : 

mv ciedArtas.desktop ~/.config/autostart

rm README.md

python3 /opt/ceidArtasIndicator/src/AnnouncementsForCEID-Artas.py &





