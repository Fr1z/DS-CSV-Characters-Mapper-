import csv
import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import pyperclip


#TODO 
# CSV -> replace only in column sentence -> formato pronto per stt
# si possono caricare e salvare i txt puliti secondo la mappatura csv ( escludendo i caratteri non in alphabet )


# Inizializza un array vuoto per salvare i caratteri
caratteri_da_mappare = ['<ELIMINA RIGA>', '<IGNORA>', '<VUOTO>', '<SPAZIO>']
simboli_da_mappare = []
wavs_data = []
text_data = []
file_input_path = ""

# Verifica che sia fornito un argomento da riga di comando
if len(sys.argv) > 2:
    print("Usage: python fix_alphabeto.py alphabet.txt")
    sys.exit(1)
elif len(sys.argv) == 2:
    # Ottieni il percorso del file alphabet dall'argomento da riga di comando
    alphabet_path = sys.argv[1]
else:
    alphabet_path = 'alphabet.txt'


# Verifica se il file CSV esiste
if not os.path.isfile(alphabet_path):
    messagebox.showerror("No alphabet file found", f"File alphabet not found in {alphabet_path}")
    sys.exit(1)

try:
    # Apre il file "alphabet.txt" in modalità lettura
    with open(alphabet_path, 'r', encoding='utf-8') as file:
        # Legge ogni riga del file
        for riga in file:
            # Rimuove eventuali spazi bianchi all'inizio e alla fine della riga
            riga = riga.strip()
            
            # Verifica se la riga inizia con il carattere '#'
            if not riga.startswith('#') and len(riga) > 0:
                # Se la riga non inizia con '#', aggiunge (l unico?) carattere al array
                caratteri_da_mappare.append(riga)

    # Stampa l'array risultante
    print("Caratteri da mappare:", caratteri_da_mappare)
except Exception as e:
    messagebox.showerror("Invalid alphabet", f"File alphabet mismatch {alphabet_path}")
    sys.exit(1)

##PARTE funzioni GUI

def dropdowns_seeder(mappatura=[]):
    global dropdowns
    global simboli_da_mappare

    # Crea etichette e dropdown nella finestra (solo CSV)
    if finestra is not None:
        dropdowns = [] # reset dropdowns

        for indice, stringa in enumerate(simboli_da_mappare):
            # Calcola la riga e la colonna per l'elemento
            riga = indice % elementi_per_colonna
            colonna = indice // elementi_per_colonna

            etichetta = tk.Label(frame, text=stringa,cursor="hand2")
            etichetta.grid(row=riga, column=colonna * 2, padx=5, pady=5, sticky="w")

            # Aggiungi la funzione di copia_testo alla lista degli eventi del clic
            etichetta.bind("<Button-1>", copia_testo)
            
            valore_selezionato = tk.StringVar()
            dropdown = ttk.Combobox(frame, values=caratteri_da_mappare, textvariable=valore_selezionato)
            dropdown.grid(row=riga, column=colonna * 2 + 1, padx=5, pady=5, sticky="w")

            # Aggiungi la dropdown alla lista
            dropdowns.append(dropdown)

        #add defalut value for all dropdowns
        can_map = True if range(len(mappatura))==range(len(simboli_da_mappare)) else False

        for i, dd in enumerate(dropdowns):
            if can_map:
                if mappatura[i] in caratteri_da_mappare:
                    dd.current(caratteri_da_mappare.index(mappatura[i]))
                else:
                    dd.current(0)
            else:
                dd.current(0)
    else: 
        print("finestra is none!")

def load_file():
    global simboli_da_mappare
    global file_input_path
    # Finestra di dialogo per scegliere il file su cui lavorare
    file_path = filedialog.askopenfilename(filetypes=[("File CSV or TXT", "*.csv *.tsv *.txt"),
                                                       ("Tutti i file", "*.*")],
                                           title="Scegli il file da modificare")

    if file_path:
        file_input_path = file_path
        if file_path.upper().endswith(".TXT"):
            #se file txt chiedi se vuoi salvarlo pulito secondo mappatura corrente
            loadTXT(file_path)
        if file_path.upper().endswith(".CSV") or file_path.upper().endswith(".TSV"):
            simboli_da_mappare = loadCSV(file_path)
            dropdowns_seeder()



def loadTXT(txt_path):
    # Array per salvare le frasi dalla colonna "sentence"
    caratteri_non_presenti = []
    # Apre il file CSV in modalità lettura
    with open(txt_path, 'r', newline='\n', encoding='utf-8') as txtfile:
        # Utilizza il modulo csv per leggere il contenuto
        reader = txtfile.readlines()
        last = False #permette di raggruppare i caratteri strani vicini per poi mapparli ad un unico symbol
        symbol = ''

        for riga in reader:
            text_data.append(riga)
            for carat in riga:
                if carat not in caratteri_da_mappare and carat not in caratteri_non_presenti: #and not in symboli da mapapre (global) cancellare tutti 
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
    simboli_strani = sorted(caratteri_non_presenti, key=len, reverse=True)
    print("Caratteri strani trovati: " + str(len(caratteri_non_presenti)))
    return simboli_strani


def setColumns(wav_path="", sentecetext=""):
        global selected_columns
        selected_columns = [wav_path, sentecetext]
        print(selected_columns)

def loadColumns(reader):
    selectcolumngGUI = tk.Tk()
    selectcolumngGUI.title("Select Column Values")
    frame = ttk.Frame(selectcolumngGUI, padding="10")
    frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
    etichetta = tk.Label(frame, text="WAV Filename")
    etichetta.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    combo1 = ttk.Combobox(frame, state="readonly", values=reader.fieldnames)
    combo1.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
    etichetta = tk.Label(frame, text="Transcript",cursor="hand2")
    etichetta.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    combo2 = ttk.Combobox(frame, state="readonly", values=reader.fieldnames)
    combo2.grid(row=1, column=1, sticky=tk.W, padx=(0, 10))
    submit_button = ttk.Button(frame, text="Set", command=lambda: [ 
        setColumns(combo1.get(), combo2.get()), 
        selectcolumngGUI.destroy(),
        selectcolumngGUI.quit()
    ] )
    submit_button.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
    selectcolumngGUI.mainloop()
    
def loadCSV(csv_path):
    global selected_columns, text_data, wavs_data
    # Array per salvare le frasi dalla colonna "sentence"
    caratteri_non_presenti = []
    # Apre il file CSV in modalità lettura
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        # Utilizza il modulo csv per leggere il contenuto
        
        reader = csv.DictReader(csvfile, delimiter="\t")
        #Open a Tkinker gui with two combobox to select a value in reader.fieldnames array
        #and un set button to close this gui and pick the values selected
        loadColumns(reader)

        vaws_column = selected_columns[0]
        text_column = selected_columns[1]

        for riga in reader:
            valore_wav = riga[vaws_column]
            valore_text = riga[text_column]
            wavs_data.append(valore_wav)
            text_data.append(valore_text)

        last = False #permette di raggruppare i caratteri strani vicini per poi mapparli ad un unico symbol
        symbol = ''

        # Legge il contenuto di tutte le righe della colonna "sentence"
        #estrae le sequenze caratteri non presenti in alphabet
        for riga in text_data:
            for carat in riga:
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
    return simboli_da_mappare

def sostituisci_simboli(mappa_caratteri):
    global file_input_path, wavs_data, text_data
    file_path = file_input_path

    try:
        testo = '\n'.join(text_data)
        for symbol, valore in mappa_caratteri.items():
            if valore == '<VUOTO>':
                testo = testo.replace(symbol, '')
            elif valore == '<IGNORA>':
                #in teoria per , si ignora ma andrebbe replaced se dentro colonna testo
                continue
            elif valore == '<SPAZIO>':
                testo = testo.replace(symbol, ' ')
            elif valore == '<ELIMINA RIGA>':
                # Divide il testo in righe
                righe = testo.splitlines()
                # Filtra le righe che contengono il carattere 'z'
                righe_filtrate = [riga for riga in testo if symbol not in riga]
                #se sto sostituendo su un csv devo eliminare la wav della riga corrispondente a quella filtrata
                if not file_path.upper().endswith(".TXT"):
                    #TODO rifare il sostituisci simboli che non faccia la join di text_data perchè se csv ci mette una vita a trovare l indice ed eliminarlo
                    #fa una diff tra righe e righe_filtrate
                    #trovando tutti gli indici delle righe eliminate (e reimposta anche le wavs)
                    # Find the indices where an element of a is not in b
                    indici_da_eliminare = [i for i, riga in enumerate(righe) if riga not in righe_filtrate]
                    wavs_data = [wav for i, wav in enumerate(wavs_data) if i not in indici_da_eliminare]
                
                # Unisce le righe di nuovo in una stringa
                testo = '\n'.join(righe_filtrate)
            else:
                testo = testo.replace(symbol, valore)

        return testo
    except Exception as e:
        print(f"Errore durante la lettura e sostituzione del file: {e}")
        return None
    

        
def carica_mappa():
    global simboli_da_mappare
    
    # Finestra di dialogo per scegliere il file di mapping
    file_path = filedialog.askopenfilename(filetypes=[("File MAP", "*.MAP *.txt"),
                                                       ("Tutti i file", "*.*")],
                                           title="Scegli il file con la mappatura caratteri")
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.readline()
            #reset prev map
            mapping = []

            for line in file:
                if "###" in line: # Skip the first line
                    continue
                try:
                    chmap = line.split('=>>')
                    simboli_da_mappare.append(chmap[0])
                    mapping.append(chmap[1].strip())
                except ValueError as e:
                    print(f"Errore valore dropdown: {e}")

            dropdowns_seeder(mapping)



#chiamato da genera. salva il file di output
def salva_file():
    global text_data
    try:
        file_destinazione = filedialog.asksaveasfilename(defaultextension=".txt",
                                                           filetypes=[("File TXT", "*.txt"),
                                                                      ("Tutti i file", "*.*")],
                                                           title="Scegli la destinazione")
        if file_destinazione:
            with open(file_destinazione, 'w', encoding='utf-8') as file:
                file.write(text_data)
            print(f"File salvato con successo in: {file_destinazione}")

            message = f"File salvato con successo in: {file_destinazione}"
            messagebox.showinfo("Salvataggio completato", message)

    except Exception as e:
        print(f"Errore durante il salvataggio del file: {e}")

#chiamato da genera. salva il file di output
def salva_csv():
    global text_data, wavs_data
    # Define the column names
    column_names = ["wav_filename", "wav_filesize", "transcript"]
    try:
        file_destinazione = filedialog.asksaveasfilename(defaultextension=".csv",
                                                           filetypes=[("File CSV", "*.csv"),
                                                                      ("Tutti i file", "*.*")],
                                                           title="Scegli la destinazione")
        if file_destinazione:
            with open(file_destinazione, 'w', encoding='utf-8') as csvfile:
                # Create a CSV writer object
                writer = csv.writer(csvfile, delimiter=",")
                    # Write the column names to the CSV file
                writer.writerow(column_names)

                # Write the data to the CSV file
                for i in range(len(wavs_data)):
                    writer.writerow([wavs_data[i], "0", text_data[i]])

            print(f"File salvato con successo in: {file_destinazione}")
            message = f"File salvato con successo in: {file_destinazione}"
            messagebox.showinfo("Salvataggio completato", message)

    except Exception as e:
        print(f"Errore durante il salvataggio del file: {e}")


def salva_mappa():
    # Funzione chiamata quando si preme il pulsante "Salva mappa"
    valori_selezionati = [dropdown.get() for dropdown in dropdowns]
    # Creazione di un dizionario utilizzando zip
    mappa_caratteri = dict(zip(simboli_da_mappare, valori_selezionati))

    try:
        file_destinazione = filedialog.asksaveasfilename(defaultextension=".MAP",
                                                           filetypes=[("File MAP", "*.MAP"),
                                                                      ("Tutti i file", "*.*")],
                                                           title="Scegli la destinazione del file di mappa")
        
        #fine mappatura
        if file_destinazione:
            with open(file_destinazione, 'w', encoding='utf-8') as file:
                file.write("###Charachter MAP###\n")
                for symbol, valore in mappa_caratteri.items():
                    line=symbol + '=>>' + valore + '\n'

                    file.write(line)
                    print(line)

            print(f"File salvato con successo in: {file_destinazione}")
            message = f"File Mappa caratteri salvato con successo in: {file_destinazione}"
            messagebox.showinfo("Salvataggio completato", message)

    except Exception as e:
        print(f"Errore durante il salvataggio del file: {e}")


def genera():
    global file_input_path
    global simboli_da_mappare
    # Funzione chiamata quando si preme il pulsante "Genera"
    valori_selezionati = [dropdown.get() for dropdown in dropdowns]

    # Creazione di un dizionario utilizzando zip
    mappa_caratteri = dict(zip(simboli_da_mappare, valori_selezionati))

    if file_input_path:
        # Esegue il replace dei simboli nel file
        try:
            testo_sostituito = sostituisci_simboli(mappa_caratteri)
        except Exception as e:
            messagebox.showerror("Errore elaborazione file", e)
            return
        
        # Salva il file con una finestra di dialogo
        if testo_sostituito is not None:
            if file_input_path.upper().endswith(".TXT"):
                salva_file(testo_sostituito)
            else:
                salva_csv(testo_sostituito)
        return

# Funzione chiamata quando si clicca su un'etichetta
def copia_testo(event):
    etichetta_cliccata = event.widget
    testo_da_copiare = etichetta_cliccata.cget("text")
    pyperclip.copy(testo_da_copiare)


#GUI SETUP
# Crea la finestra principale
finestra = tk.Tk()
finestra.title("MAP all Symbols to alphabet")

num_colonne = 2  # Numero di colonne
elementi_per_colonna = 20  # Numero di elementi per colonna

dropdowns = [] # array delle dropdowns disposte

frame = ttk.Frame(finestra, padding="10")
frame.grid(row=20, column=6, sticky=(tk.W, tk.E, tk.N, tk.S))

# Crea il pulsante Carica Map
pulsante_load = tk.Button(frame, text="Carica File", command=load_file)
pulsante_load.grid(row=22, column=4, columnspan=1, sticky="sw", padx=10, pady=10)

# Crea il pulsante Carica Map
pulsante_carica_map = tk.Button(frame, text="Carica Mappatura", command=carica_mappa)
pulsante_carica_map.grid(row=21, column=5, columnspan=1, sticky="sw", padx=10, pady=10)

# Crea il pulsante Salva
pulsante_salva_map = tk.Button(frame, text="Salva Mappatura", command=salva_mappa)
pulsante_salva_map.grid(row=22, column=5, columnspan=1, sticky="sw", padx=10, pady=10)

# Crea il pulsante Genera Clean
pulsante_genera = tk.Button(frame, text="Salva File", command=genera)
pulsante_genera.grid(row=22, column=6, columnspan=1, sticky="se", padx=10, pady=10)
    
# Avvia il loop principale della finestra
finestra.mainloop()