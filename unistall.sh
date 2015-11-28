#!/bin/bash

# Αυτό το script δημιουργήθηκε με σκοπό να βοηθήσει τον χρήστη
# να απεγκαταστήσει αν επιθυμεί το Indicator Applet από τον υπολογιστή του.
# Ελπίζουμε να βοηθήσει.  :)

# Created by G-lts Team
# Copyleft (ↄ)


sudo rm ~/.config/autostart/ciedArtas.desktop

sudo rm -R /opt/ceidArtasIndicator

notify-send 'Announcements For CEID Artas' 'Η εφαρμογή απεγκαταστάθηκε επιτυχώς.' -i /usr/share/icons/gnome/48x48/actions/edit-delete.png
paplay /usr/share/sounds/freedesktop/stereo/complete.oga



