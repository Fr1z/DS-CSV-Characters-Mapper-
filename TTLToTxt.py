import re

from tkinter import filedialog
import tkinter.messagebox as messagebox

#TODO
#ignorare tutte le linee che hanno meno di 12 caratteri
#
#rimuovere link e percorsi come : (quindi / )
#  http://pad2
#com/images/thumb/b/b3/Fix-a-Split-Nail-Step-1
#jpg/300px-Fix-a-Split-Nail-Step-1
#
#stripping di ogni linea
#fermare lettura  a carattere {largeimage|Ge o  {\\displaystyle F_{n}=F_{n-1}+F_{n-2}}



# Define the regular expression pattern
pattern = r'dbo:abstract """(.*?)(?="""|<script)'


# Define the regular expression pattern for HTML tags
html_pattern = r'<.*?>'


def read_abstracts_from_ttl_file(file_path):
    # Open the Turtle Text file in read mode with UTF-8 encoding
    with open(file_path, "r", encoding="utf-8") as f:
        # Read the contents of the file as a string
        ttl_string = f.read()
        
    # Find all occurrences of the pattern in the Turtle Text file
    matches = re.findall(pattern, ttl_string, re.DOTALL)
    return matches

def write_txt(matches):
    try:
        file_destinazione = filedialog.asksaveasfilename(defaultextension=".txt",
                                                           filetypes=[("File TXT", "*.txt"),
                                                                      ("Tutti i file", "*.*")],
                                                           title="Scegli la destinazione")
        if file_destinazione:
            with open(file_destinazione, 'w', encoding='utf-8') as file:
                # Print the matched text
                for match in matches:
                    # Remove HTML tags from the string
                    final_string = re.sub(html_pattern, '', match)
                    final_string = final_string.strip().replace('.', '\n') 

                    if not final_string.endswith('\n'):
                        final_string += '\n'

                    file.write(final_string)

    except Exception as e:
        print(f"Errore scrittura {e}")
        return
    message = f"File salvato con successo in: {file_destinazione}"
    messagebox.showinfo("Salvataggio completato", message)
    return
#MAIN
file_path = filedialog.askopenfilename(filetypes=[("File TurtleText", "*.ttl *.txt"),
                                                       ("Tutti i file", "*.*")],
                                           title="Scegli il file TTL supportato")
if file_path:
    matches = read_abstracts_from_ttl_file(file_path)
    write_txt(matches)


