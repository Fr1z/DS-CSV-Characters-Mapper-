import sys
from myFunction import *
#TODO 
# fix import custom value su dropbox da mappatura
# Use     with io.TextIOWrapper(io.BufferedWriter(gzip.open(data_lower, "w+")), encoding="utf-8") as file_out and progressbar


# Verifica che sia fornito un argomento da riga di comando
if len(sys.argv) > 2:
    print("Usage: python fix_alphabeto.py alphabet.txt")
    sys.exit(1)
elif len(sys.argv) == 2:
    # Ottieni il percorso del file alphabet dall'argomento da riga di comando
    alphabet_path = sys.argv[1]
else:
    alphabet_path = 'alphabet.txt'

#start
loadAlphabeth(alphabet_path)
gui_init()
