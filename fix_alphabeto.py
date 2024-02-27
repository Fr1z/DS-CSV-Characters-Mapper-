import csv
import sys
import os

# Inizializza un array vuoto per salvare i caratteri
caratteri_da_mappare = []

# Apre il file "alphabet.txt" in modalità lettura
with open('alphabet.txt', 'r', encoding='utf-8') as file:
    # Legge ogni riga del file
    for riga in file:
        # Rimuove eventuali spazi bianchi all'inizio e alla fine della riga
        riga = riga.strip()
        
        # Verifica se la riga inizia con il carattere '#'
        if not riga.startswith('#') and len(riga) > 0:
            # Se la riga non inizia con '#', aggiunge il primo carattere al array
            caratteri_da_mappare.append(riga[0])

# Stampa l'array risultante
print("Caratteri da mappare:", caratteri_da_mappare)

# Verifica che sia fornito un argomento da riga di comando
if len(sys.argv) != 2:
    print("Usage: python fix_alphabeto.py path_to_csv_file")
    sys.exit(1)

# Ottieni il percorso del file CSV dall'argomento da riga di comando
csv_path = sys.argv[1]

# Verifica se il file CSV esiste
if not os.path.isfile(csv_path):
    print(f"File not found: {csv_path}")

# Array per salvare le frasi dalla colonna "sentence"
frasi_da_csv = []
caratteri_non_presenti = []
# Apre il file CSV in modalità lettura
with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
    # Utilizza il modulo csv per leggere il contenuto
    reader = csv.DictReader(csvfile, delimiter=';')
    
    # Verifica che la colonna "sentence" sia presente nel CSV
    if 'sentence' not in reader.fieldnames:
        print("La colonna 'sentence' non è presente nel CSV.")
        sys.exit(1)

    # Legge il contenuto di tutte le righe della colonna "sentence"
    last = False #permette di raggruppare i caratteri strani vicini per poi mapparli ad un unico symbol
    symbol = ''
    for riga in reader:
        for carat in riga['sentence']:
            if carat not in caratteri_da_mappare and carat not in caratteri_non_presenti:
                last=True
                symbol += carat
            else:
                if (last):
                    if (symbol not in caratteri_non_presenti):
                        caratteri_non_presenti.append(symbol)
                    symbol = ''
                    last=False

# Stampa le frasi estratte dal CSV

print("\n\r\n\r")

simboli_da_mappare = sorted(caratteri_non_presenti, key=len, reverse=True)
#print(simboli_da_mappare)
#print("\n\r\n\r")
for symbol in simboli_da_mappare:
    print('\'' + symbol + '\' => \'\',')

print("Caratteri strani trovati: " + str(len(caratteri_non_presenti)))