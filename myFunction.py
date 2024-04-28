import csv
import sys
import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import pyperclip
from num2words import num2words
from myInitSets import *

##FUNZIONI
def loadAlphabeth(alphabet_path):
    # Verifica se il file CSV esiste
    if not os.path.isfile(alphabet_path):
        messagebox.showerror("No alphabet file found", f"File alphabet not found in {alphabet_path}")
        sys.exit(1)

    try:
        # Apre il file "alphabet.txt" in modalità lettura
        with open(alphabet_path, 'r', encoding='utf-8') as file:
            # Legge ogni riga del file
            for riga in file:
                riga = riga.replace('\r', '').replace('\n', '')
                # Verifica se la riga inizia con il carattere '#'
                if not riga.startswith('#') and len(riga) > 0:
                    # Se la riga non inizia con '#', aggiunge (l unico?) carattere al array
                    riga = riga.replace(' ','<SPAZIO>')
                    caratteri_da_mappare.append(riga)

        # Stampa l'array risultante
        print("Caratteri da mappare:", caratteri_da_mappare)
    except Exception as e:
        messagebox.showerror("Invalid alphabet", f"File alphabet mismatch {alphabet_path}")
        sys.exit(1)


def dropdowns_seeder(mappatura={}):
    global dropdowns
    global simboli_da_mappare
    global elementi_per_colonna
    global finestra
    global frame
    global load_mapper

    if not load_mapper:
        return
    
    # Pulizia vecchie dropdown e label
    for widget in frame.winfo_children():
        if widget.winfo_class() in ['Label', 'TCombobox']:
            widget.destroy()

    dropdowns = [] # reset dropdowns
    for indice, stringa in enumerate(simboli_da_mappare):
        # Calcola la riga e la colonna per l'elemento
        riga = indice % elementi_per_colonna
        colonna = indice // elementi_per_colonna
        etichetta = tk.Label(frame, text=stringa,cursor="hand2")
        etichetta.grid(row=riga, column=colonna * 2, padx=3, pady=3, sticky="w")
        # Aggiungi la funzione di copia_testo alla lista degli eventi del clic su label
        etichetta.bind("<Button-1>", copia_testo)
        
        valore_selezionato = tk.StringVar()
        dropdown = ttk.Combobox(frame, values=caratteri_da_mappare, textvariable=valore_selezionato)
        dropdown.grid(row=riga, column=colonna * 2 + 1, padx=3, pady=3, sticky="w")
        # Aggiungi la dropdown alla lista
        dropdowns.append(dropdown)
    #per ogni dropdown carica il suo valore predefinito o mappato
    for i, dd in enumerate(dropdowns):
        if simboli_da_mappare[i] in mappatura.keys():
            if mappatura[simboli_da_mappare[i]] in caratteri_da_mappare:
                dd.current(caratteri_da_mappare.index(mappatura[simboli_da_mappare[i]]))
            else:
                dd.current(0)
                result = messagebox.askyesno("Question", f"{mappatura[simboli_da_mappare[i]]} non è tra i caratteri mappabili, aggiungere lo stesso custom value?")
                if result:
                    #caratteri_da_mappare.append(mappatura[simboli_da_mappare[i]])
                    dd.insert(1, mappatura[simboli_da_mappare[i]])
                
  
        else:
            #default value
            dd.current(0)
    
    # Set the scroll region to the size of the frame
    finestra.item_canvas.config(scrollregion=finestra.item_canvas.bbox("all"))
    finestra.item_canvas.configure(background='#ffffca') 

def load_file():
    global simboli_da_mappare
    global file_input_path
    global text_data
    global load_mapper

    text_data = {} #reset dei dati precedenti
    # Finestra di dialogo per scegliere il file su cui lavorare
    file_path = filedialog.askopenfilename(filetypes=[("File CSV or TXT", "*.csv *.tsv *.txt"),
                                                       ("Tutti i file", "*.*")],
                                           title="Scegli il file da modificare")

    if file_path:
        load_mapper = True
        file_input_path = file_path
        if file_path.upper().endswith(".TXT"):
            simboli_da_mappare = loadTXT(file_path)
        if file_path.upper().endswith(".CSV") or file_path.upper().endswith(".TSV"):
            simboli_da_mappare = loadCSV(file_path)
        
        dropdowns_seeder()



def loadTXT(txt_path):
    num2words_enabled = ask_num2words_question()
    global text_data, load_mapper
    # Array per salvare le frasi dalla colonna "sentence"
    caratteri_non_presenti = []

    # Apre il file CSV in modalità lettura
    with open(txt_path, 'r', newline='\n', encoding='utf-8') as txtfile:
        # Utilizza il modulo csv per leggere il contenuto
        reader = txtfile.readlines()
        last = False #permette di raggruppare i caratteri strani vicini per poi mapparli ad un unico symbol
        symbol = ''

        for i, riga in enumerate(reader):
            #Se abilitato converte i digits in words
            if num2words_enabled:
                try:
                    # Convert the digits to words
                    words = [num2words(int(word), lang="it") if word.isdigit() else word for word in riga.split(' ')]
                    # Join the words into a single string
                    riga = ' '.join(words)
                except Exception as e:
                    print(f"Error converting to string an unusual number: {e} \nSKIPPED")

            riga = riga.lower().strip()
            text_data[i] = riga
            for carat in riga:
                carat = carat.replace('\t', '[TAB]').replace(' ','[SPAZIO]')
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
    if not len(caratteri_non_presenti):
        messagebox.showinfo("Bene!", "il file è pulito, nessuna elaborazione richiesta")
    if len(caratteri_non_presenti)>mapper_max_number:
        load_mapper = False
        messagebox.showwarning(title="too much symbols", message="Please choose a map file to clean common symbols, others will be deleted.")

    return simboli_strani


# Ask a YES or NO num2words
def ask_num2words_question():
    result = messagebox.askyesno("Question", "Do you want to replace numbers to words?")
    if result:
        return True
    return False

def setColumns(selected=""):
        global selected_column
        selected_column = selected
        print(selected_column)

def loadColumns(reader):
    selectcolumngGUI = tk.Tk()
    selectcolumngGUI.title("Select Column in Table")
    frame = ttk.Frame(selectcolumngGUI, padding="10")
    frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
    etichetta = tk.Label(frame, text="Colonna da elaborare")
    etichetta.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    combo1 = ttk.Combobox(frame, state="readonly", values=reader.fieldnames)
    combo1.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
    submit_button = ttk.Button(frame, text="Set", command=lambda: [ 
        setColumns(combo1.get()), 
        selectcolumngGUI.destroy(),
        selectcolumngGUI.quit()
    ] )
    submit_button.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
    selectcolumngGUI.mainloop()
    
def loadCSV(csv_path):
    global selected_column, text_data, load_mapper
    # Array per salvare le frasi dalla colonna "sentence"
    caratteri_non_presenti = []
    # Apre il file CSV in modalità lettura
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        # Utilizza il modulo csv per leggere il contenuto
    
        known_delimiters = ["\t", ",", ";"]
        #trova la delimitazione corretta
        for picked_delimiter in known_delimiters:
            reader = csv.DictReader(csvfile, delimiter=picked_delimiter, lineterminator="\r\n")
            if len(reader.fieldnames)>1:
                break
            else:
                csvfile.seek(0)
        
        loadColumns(reader) # now we should have a "selected_column"

        num2words_enabled = ask_num2words_question()

        for i, riga in enumerate(reader):
            valore_text = riga[selected_column].lower() #automatically to lowercase here avoids more mapping #TODO must be option
            
            #Se abilitato converte i digits in words
            if num2words_enabled:
                # Convert the digits to words
                words = [num2words(int(word), lang="it") if word.isdigit() else word for word in valore_text.split(' ')]
                # Join the words into a single string
                valore_text = ' '.join(words)

            text_data[i] = valore_text

        last = False #permette di raggruppare i caratteri strani vicini per poi mapparli ad un unico symbol
        symbol = ''

        # Legge il contenuto di tutte le righe della colonna selezionata
        #estrae le sequenze caratteri non presenti in alphabet
        for riga in text_data.values():
            for carat in riga:
                carat = carat.replace(' ','[SPAZIO]')
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
    print("Caratteri strani trovati nel CSV: " + str(len(caratteri_non_presenti)))
    if not len(caratteri_non_presenti):
        messagebox.showinfo("Bene!", "la colonna del file csv risulta pulita, nessuna elaborazione richiesta")
    if len(caratteri_non_presenti)>mapper_max_number:
        load_mapper = False
        messagebox.showwarning(title="too much symbols", message="Please choose a map file to clean common symbols, others will be deleted.")

    return simboli_da_mappare

def final_clean(str):
    str = rimuove_spazi_multipli = re.sub(r'\s+', ' ', str)
    return str.strip()

def sostituisci_simboli(mappa_caratteri):
    updateMinWords()
    global min_words
    global text_data

    new_text_data = {}
    try:
        for i, riga in text_data.items():
            testo = riga
            testo = testo.strip()

            if len(testo)<1 or len(testo.split(" ")) < min_words:
                continue #skip this line 

            for symbol, valore in mappa_caratteri.items():
                #fix sui simboli speciali
                if symbol == "[TAB]":
                    symbol = "\t"
                if symbol == "[SPAZIO]":
                    symbol = " "

                if symbol in testo:
                    if valore == '<VUOTO>':
                        testo = testo.replace(symbol, '')
                    elif valore == '<SPAZIO>':
                        testo = testo.replace(symbol, ' ')
                    elif valore == '<ELIMINA RIGA>':
                        testo = ""
                        break
                    elif valore == '<PERMETTI>':
                        valore = symbol
                    else:
                        testo = testo.replace(symbol, valore)
            #se è rimasto qualcosa al testo pulito rimettilo nel text_data
            testo_pulito = final_clean(testo)
            if len(testo_pulito) and len(testo_pulito.split(" ")) >= min_words:
                new_text_data[i] = testo_pulito
    except Exception as e:
        print(f"Errore durante la lettura e sostituzione del file: {e}")
        return False
    
    text_data = new_text_data.copy()

    return text_data

def carica_mappa():
    global mappatura
    
    # Finestra di dialogo per scegliere il file di mapping
    file_path = filedialog.askopenfilename(filetypes=[("File MAP", "*.MAP *.txt"),
                                                       ("Tutti i file", "*.*")],
                                           title="Scegli il file con la mappatura caratteri")
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.readline()
            #create new mapping dictionary
            mapping = {}

            for line in file:
                if "###" in line: # Skip the first line
                    continue
                try:
                    chmap = line.split('=>>')
                    if len(chmap)==2:
                        simbolo = chmap[0].replace('\r', '').replace('\n', '').replace(' ','[SPAZIO]').replace('\t','[TAB]')
                        valore = chmap[1].replace('\r', '').replace('\n', '')
                        new_map(simbolo)
                        mapping[simbolo] = valore
                except ValueError as e:
                    print(f"Errore valore dropdown: {e}")
            mappatura = mapping
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
                globaltext = '\n'.join(text_data.values())
                file.write(globaltext)
            print(f"File salvato con successo in: {file_destinazione}")

            message = f"File salvato con successo in: {file_destinazione}"
            messagebox.showinfo("Salvataggio completato", message)

    except Exception as e:
        print(f"Errore durante il salvataggio del file: {e}")

#chiamato da genera. salva il file di output
def salva_csv():
    global text_data, file_input_path, selected_column
    # Define the column names
    #column_names = ["wav_filename", "wav_filesize", "transcript"]
    file_destinazione = filedialog.asksaveasfilename(defaultextension=".csv",
                                                       filetypes=[("File CSV", "*.csv"),
                                                                  ("Tutti i file", "*.*")],
                                                       title="Scegli la destinazione")
    if file_destinazione and file_input_path:
        try:
            with open(file_input_path, 'r', encoding='utf-8') as csvread:

                print(f"read from {file_input_path} \n")
                reader = csv.DictReader(csvread, delimiter="\t")
                column_names = reader.fieldnames

                indice_righe_valide = text_data.keys()
                #righe csv originale
                #input_file_rows = len(list(reader))
                #rows_diff = input_file_rows-len(indice_righe_valide)
                #print(f"Il file avrà {len(indice_righe_valide)} righe,{rows_diff} in meno rispetto le {input_file_rows} di partenza")
                
                final_rows=[]

                for i, riga in enumerate(reader):
                    if i in indice_righe_valide:
                        row = {}
                        for column in column_names:
                            if column == selected_column:
                                row[column] = text_data[i]
                            else:
                                row[column] = riga[column]
                        final_rows.append(row)

                with open(file_destinazione, 'w', encoding='utf-8', newline='') as csvfile:
                    # Create a CSV writer object
                    writer = csv.DictWriter(csvfile, fieldnames=column_names, delimiter="\t")
                    
                    # Scriviamo i nomi delle colonne nel file di output
                    writer.writeheader()
                    
                    #scriviamo i dati puliti sul csv finale
                    writer.writerows(final_rows)

                    print(f"File csv salvato con successo in: {file_destinazione}")
                    message = f"File csv salvato con successo in: {file_destinazione} con {len(final_rows)} righe"
                    messagebox.showinfo("Salvataggio completato", message)

        except Exception as e:
            print(f"Errore durante il salvataggio del csv: {e}")
            message = f"errore durante il salvataggio: {e}"
            messagebox.showerror("Errore durante il salvataggio", message)


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
                    symbol = symbol.replace('\r', '').replace('\n', '')
                    valore = valore.replace('\r', '').replace('\n', '')

                    line = symbol + '=>>' + valore + '\r\n'

                    file.write(line)
                    #print(line)

            print(f"File salvato con successo in: {file_destinazione}")
            message = f"File Mappa caratteri salvato con successo in: {file_destinazione}"
            messagebox.showinfo("Salvataggio completato", message)

    except Exception as e:
        print(f"Errore durante il salvataggio del file: {e}")

def updateMinWords():
    global min_words, entry_min_words
    min_words = int(entry_min_words.get())

def add_map():
    newMapGUI = tk.Tk()
    newMapGUI.title("Add Symbol to Fetch")
    frame = ttk.Frame(newMapGUI, padding="10")
    frame.grid(row=1, column=3, sticky=(tk.W, tk.E, tk.N, tk.S))
    etichetta = tk.Label(frame, text="Testo da selezionare")
    etichetta.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    input_text = ttk.Entry(frame, text="sym")
    input_text.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
    submit_button = ttk.Button(frame, text="Add", command=lambda: [ 
        new_map(input_text.get()), 
        newMapGUI.destroy(),
        newMapGUI.quit()
    ] )
    submit_button.grid(row=0, column=2, sticky=tk.W, pady=(10, 0))
    newMapGUI.mainloop()

    
    dropdowns_seeder()
    return

def new_map(simbolo):
    global simboli_da_mappare
    if simbolo not in simboli_da_mappare and len(simbolo):
        #Se il simbolo da mappare è già stato messo in colonna sostituiscine il valore
        simboli_da_mappare.append(simbolo) #aggiungerà una dropdown
    

def genera():
    global file_input_path
    global simboli_da_mappare
    global load_mapper
    global mappatura

    azioni_su_simboli = []
    if load_mapper:
        # Funzione chiamata quando si preme il pulsante "Genera"
        valori_selezionati = [dropdown.get() for dropdown in dropdowns]
        azioni_su_simboli = valori_selezionati
    else:
        #mappa con i valori del file map
        for simbolo in simboli_da_mappare:
            #remap space and tabs
            simbolo = simbolo.replace('\r', '').replace('\n', '').replace(' ','[SPAZIO]').replace('\t','[TAB]')
            
            valore_mappa = mappatura.get(simbolo, "<ELIMINA RIGA>")#se non trovato: elimina riga
            azioni_su_simboli.append(valore_mappa)

    # Creazione di un dizionario utilizzando zip
    mappa_caratteri = dict(zip(simboli_da_mappare, azioni_su_simboli))

    if file_input_path:
        # Salva il file con una finestra di dialogo
        output_data = sostituisci_simboli(mappa_caratteri)
    
        if output_data != False:
            if file_input_path.upper().endswith(".TXT"):
                salva_file()
            else:
                salva_csv()
        return



# Funzione chiamata quando si clicca su un'etichetta
def copia_testo(event):
    etichetta_cliccata = event.widget
    testo_da_copiare = etichetta_cliccata.cget("text")
    pyperclip.copy(testo_da_copiare)

def gui_init():
    global finestra, elementi_per_colonna, dropdowns, entry_min_words, frame
    #GUI SETUP
    # Crea la finestra principale
    finestra = tk.Tk()
    finestra.title("MAP all Symbols to alphabet")

    dropdowns = [] # array delle dropdowns disposte

    finestra.xbar = tk.Scrollbar(finestra, orient="horizontal")
    finestra.ybar = tk.Scrollbar(finestra)
    finestra.item_canvas = tk.Canvas(finestra, width=1720, height=960,
                                     xscrollcommand=finestra.xbar.set,
                                     yscrollcommand=finestra.ybar.set)
    finestra.item_canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    finestra.xbar.grid(row=1, column=0, sticky="ew")
    finestra.ybar.grid(row=0, column=1, sticky="ns")
    finestra.grid_rowconfigure(0, weight=1)
    finestra.grid_columnconfigure(0, weight=1)

    frame = ttk.Frame(finestra.item_canvas, padding="10")

    frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))


    # Crea il pulsante Carica File
    pulsante_load = tk.Button(frame, text="Carica File", command=load_file)
    pulsante_load.grid(row=22, column=5, columnspan=1, sticky="sw", padx=10, pady=10)

    # Crea il pulsante Carica Map
    pulsante_carica_map = tk.Button(frame, text="Carica Mappatura", command=carica_mappa)
    pulsante_carica_map.grid(row=21, column=6, columnspan=1, sticky="sw", padx=10, pady=10)

    # Crea il pulsante Salva
    pulsante_salva_map = tk.Button(frame, text="Salva Mappatura", command=salva_mappa)
    pulsante_salva_map.grid(row=22, column=6, columnspan=1, sticky="sw", padx=10, pady=10)

    # Crea il pulsante Aggiungi Map
    pulsante_addmap = tk.Button(frame, text="Aggiungi Custom Map", command=add_map)
    pulsante_addmap.grid(row=21, column=7, columnspan=1, sticky="sw", padx=10, pady=10)

    # Crea contatore di parole minimo
    entry_min_words = tk.Entry(frame, textvariable=tk.StringVar(value="0"), justify='center')
    entry_min_words.grid(row=22, column=7, columnspan=1, sticky="sw", padx=10, pady=10)

    # Crea il pulsante Genera Clean
    pulsante_genera = tk.Button(frame, text="Esporta File Pulito", command=genera)
    pulsante_genera.grid(row=22, column=8, columnspan=1, sticky="se", padx=10, pady=10)
    
    # Set the scroll region to the size of the frame
    finestra.item_canvas.config(scrollregion=finestra.item_canvas.bbox("all"))
    finestra.item_canvas.configure(background='#ffffca') 
    # Avvia il loop principale della finestra
    finestra.mainloop()