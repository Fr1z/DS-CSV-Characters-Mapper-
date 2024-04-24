import sys
from myFunction import *
#TODO 
# fix import custom value su dropbox da mappatura
# Fix salvataggio (sono in txt) che perde tutta la text_data nella riga sotto dopo averla appena ottenuta
# TODO se trova più di N caratteri da mappare chiedere solo se si ha una mappatura da applicare sul resto applicare un elimina riga
# Inizializza un array vuoto per salvare i caratteri


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
