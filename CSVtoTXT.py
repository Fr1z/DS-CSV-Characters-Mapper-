import csv
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox


selected_column = ""

def setColumns(selected=""):
        global selected_column
        selected_column = selected
        print(selected_column)

def loadColumns(fieldnames):
    selectcolumngGUI = tk.Tk()
    selectcolumngGUI.title("Select Column in Table")
    frame = ttk.Frame(selectcolumngGUI, padding="10")
    frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
    etichetta = tk.Label(frame, text="Colonna da elaborare")
    etichetta.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    combo1 = ttk.Combobox(frame, state="readonly", values=fieldnames)
    combo1.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
    submit_button = ttk.Button(frame, text="Set", command=lambda: [ 
        setColumns(combo1.get()), 
        selectcolumngGUI.destroy(),
        selectcolumngGUI.quit()
    ] )
    submit_button.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
    selectcolumngGUI.mainloop()
    

def read_csv(csv_path):
    global selected_column
    text_data = []

    # Apre il file CSV in modalità lettura
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        # Utilizza il modulo csv per leggere il contenuto
        known_delimiters = ["\t", ",",  ";"]
        #trova la delimitazione corretta
        for picked_delimiter in known_delimiters:
            reader = csv.DictReader(csvfile, delimiter=picked_delimiter)
            if len(reader.fieldnames)>1:
                break
            else:
                csvfile.seek(0)

        loadColumns(reader.fieldnames) # now we should have a "selected_column"

        for riga in reader:
            valore_text = riga[selected_column].strip() #automatically to lowercase here avoids more mapping #TODO must be option
            
            text_data.append(valore_text)
        return text_data

def write_txt(datacolumn):
    try:
        file_destinazione = filedialog.asksaveasfilename(defaultextension=".txt",
                                                           filetypes=[("File TXT", "*.txt"),
                                                                      ("Tutti i file", "*.*")],
                                                           title="Scegli la destinazione")
        if file_destinazione:
            with open(file_destinazione, 'w', encoding='utf-8', newline="\r\n") as file:
                final_string = "\n".join(datacolumn)
                file.write(final_string)

    except Exception as e:
        print(f"Errore scrittura {e}")
        return
    message = f"File salvato con successo in: {file_destinazione}"
    messagebox.showinfo("Salvataggio completato", message)
    return
#MAIN
file_path = filedialog.askopenfilename(filetypes=[("File CSV", "*.csv *.tsv *.txt"),
                                                       ("Tutti i file", "*.*")],
                                           title="Scegli il file CSV supportato")
if file_path:
    datacolumn = read_csv(file_path)
    write_txt(datacolumn)


