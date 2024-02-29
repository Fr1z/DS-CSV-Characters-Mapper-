import csv
import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pyperclip

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

print("Caratteri strani trovati: " + str(len(caratteri_non_presenti)))

def sostituisci_simboli(file_path, mappa_caratteri):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            testo = file.read()

        for symbol, valore in mappa_caratteri.items():
            if valore == '<VUOTO>':
                testo = testo.replace(symbol, '')
            elif valore == '<IGNORA>':
                #in teoria per , si ignora ma andrebbe replaced se dentro colonna testo
                continue
            elif valore == '<ELIMINA RIGA>':
                # Divide il testo in righe
                righe = testo.splitlines()
                # Filtra le righe che contengono il carattere 'z'
                righe_filtrate = [riga for riga in righe if valore not in riga]
                # Unisce le righe di nuovo in una stringa
                testo = '\n'.join(righe_filtrate)
            else:
                testo = testo.replace(symbol, valore)

        return testo
    except Exception as e:
        print(f"Errore durante la lettura e sostituzione del file: {e}")
        return None
    
def loadmap():
    # Finestra di dialogo per scegliere il file di mapping
    file_path = filedialog.askopenfilename(filetypes=[("File MAP", "*.MAP, *.txt"),
                                                       ("Tutti i file", "*.*")],
                                           title="Scegli il file con la mappatura caratteri")
    if file_path:
        for dd in dropdowns:
            dd.current(1)

def salva_file(testo_sostituito):
    try:
        file_destinazione = filedialog.asksaveasfilename(defaultextension=".csv",
                                                           filetypes=[("File CSV", "*.csv"),
                                                                      ("Tutti i file", "*.*")],
                                                           title="Scegli la destinazione")
        if file_destinazione:
            with open(file_destinazione, 'w', encoding='utf-8') as file:
                file.write(testo_sostituito)
            print(f"File salvato con successo in: {file_destinazione}")
    except Exception as e:
        print(f"Errore durante il salvataggio del file: {e}")

def salva_mappa(mappa_caratteri):
    try:
        file_destinazione = filedialog.asksaveasfilename(defaultextension=".MAP",
                                                           filetypes=[("File MAP", "*.MAP"),
                                                                      ("Tutti i file", "*.*")],
                                                           title="Scegli la destinazione del file di mappa")
        
        #fine mappatura
        if file_destinazione:
            with open(file_destinazione, 'w', encoding='utf-8') as file:
                for symbol, valore in mappa_caratteri.items():
                    line=symbol + '=>>' + valore + '\n'

                    file.write(line)
                    print(line)

            print(f"File salvato con successo in: {file_destinazione}")
    except Exception as e:
        print(f"Errore durante il salvataggio del file: {e}")
##PARTE GUI

def genera():
    # Funzione chiamata quando si preme il pulsante "Genera"
    valori_selezionati = [dropdown.get() for dropdown in dropdowns]

    # Creazione di un dizionario utilizzando zip
    mappa_caratteri = dict(zip(simboli_da_mappare, valori_selezionati))

    #questa parte utile per salvare la mappatura caratteri
    #for symbol, valore in mappa_caratteri.items():
    #    print(symbol + '=>>' + valore + '\n\r')
    #fine mappatura
        
    # Finestra di dialogo per scegliere il file su cui lavorare
    file_path = filedialog.askopenfilename(filetypes=[("File CSV", "*.csv, *.tsv"),
                                                       ("Tutti i file", "*.*")],
                                           title="Scegli il file da modificare")

    if file_path:
        # Esegue il replace dei simboli nel file
        testo_sostituito = sostituisci_simboli(file_path, mappa_caratteri)

        if testo_sostituito is not None:
            # Salva il file con una finestra di dialogo
            salva_file(testo_sostituito)
        
        salva_mappa(mappa_caratteri=mappa_caratteri)

    finestra.destroy()

# Funzione chiamata quando si clicca su un'etichetta
def copia_testo(event):
    etichetta_cliccata = event.widget
    testo_da_copiare = etichetta_cliccata.cget("text")
    pyperclip.copy(testo_da_copiare)

# Crea la finestra principale
finestra = tk.Tk()
finestra.title("MAP all Symbols to alphabet")

# Crea una lista di variabili StringVar per tenere traccia delle selezioni nelle dropdown
caratteri_da_mappare.insert(0, '<ELIMINA RIGA>')
caratteri_da_mappare.insert(0, '<IGNORA>')
caratteri_da_mappare.insert(0, '<VUOTO>')

num_colonne = 2  # Numero di colonne
elementi_per_colonna = 20  # Numero di elementi per colonna

dropdowns = [] # array delle dropdowns disposte

# Crea il pulsante Carica Map
pulsante_salva = tk.Button(finestra, text="Carica Mappatura", command=loadmap)
pulsante_salva.grid(row=100, column=1, columnspan=2, sticky="se", padx=10, pady=10)

# Crea il pulsante Salva
pulsante_salva = tk.Button(finestra, text="Genera", command=genera)
pulsante_salva.grid(row=100, column=2, columnspan=2, sticky="se", padx=10, pady=10)

# Crea etichette e dropdown nella finestra
for indice, stringa in enumerate(simboli_da_mappare):
    # Calcola la riga e la colonna per l'elemento
    riga = indice % elementi_per_colonna
    colonna = indice // elementi_per_colonna

    etichetta = tk.Label(finestra, text=stringa,cursor="hand2")
    etichetta.grid(row=riga, column=colonna * 2, padx=5, pady=5, sticky="w")

    # Aggiungi la funzione di copia_testo alla lista degli eventi del clic
    etichetta.bind("<Button-1>", copia_testo)
    
    valore_selezionato = tk.StringVar()
    dropdown = ttk.Combobox(finestra, values=caratteri_da_mappare, textvariable=valore_selezionato)
    dropdown.grid(row=riga, column=colonna * 2 + 1, padx=5, pady=5, sticky="w")

    # Aggiungi la dropdown alla lista
    dropdowns.append(dropdown)

#add defalut value for all dropdowns
for dd in dropdowns:
    dd.current(0)
    
# Avvia il loop principale della finestra
finestra.mainloop()