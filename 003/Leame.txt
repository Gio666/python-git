#File: procesarPadron.py

import sys

nombreDeArchivo = 'Leame.txt'

with open(nombreDeArchivo) as f:
    for line in f:
        print line