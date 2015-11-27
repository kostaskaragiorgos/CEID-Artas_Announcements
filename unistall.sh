#!/bin/bash

# Αυτό το script δημιουργήθηκε με σκοπό να βοηθήσει τον χρήστη
# να απεγκαταστήσει αν επιθυμεί το Indicator Applet από τον υπολογιστή του.
# Ελπίζουμε να βοηθήσει.  :)

# Created by G-lts Team
# Copyleft (ↄ)

stty -echo
read -p "Password please : " pass
stty echo
printf '\n'

sudo rm ~/.config/autostart/ciedArtas_Indicator.desktop

sudo rm -R /opt/ceidArtasIndicator


