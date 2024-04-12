import os
import csv
import subprocess

# Definisci la cartella di input e output

cartella_input = input("Inserisci il percorso della cartella degli ogg: ")
cartella_output = cartella_input+"/output"

# Verifica se la cartella di output esiste, altrimenti creala
if not os.path.exists(cartella_output):
    os.makedirs(cartella_output)

# Apre il file CSV per scrivere i risultati
with open('risultati.csv', 'w', encoding="utf-8", newline="") as csvfile:
    campo_nomi = ['wav_filename', 'wav_filesize', 'transcript']
    writer = csv.DictWriter(csvfile, fieldnames=campo_nomi, delimiter="\t")
    writer.writeheader()

    # Itera attraverso tutti i file nella cartella di input
    for i, filename in enumerate(os.listdir(cartella_input)):
        if filename.endswith(".ogg"):
            # Estrai il nome del file senza estensione e senza caratteri tra parentesi
            nome_file = os.path.splitext(filename)[0]
            nome_file_senza_parentesi = nome_file.split('(')[0].strip().lower() 

            # Crea il percorso completo per il file di input e output
            percorso_input = os.path.join(cartella_input, filename)
            nome_file_output = "mydataset_" + str(i)
            percorso_output = os.path.join(cartella_output, f"{nome_file_output}.wav")

            # Esegui la conversione da .ogg a .wav utilizzando ffmpeg
            subprocess.run(["ffmpeg", "-i", percorso_input, "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le", percorso_output])

            # Ottieni la dimensione del file wav convertito
            dimensione_file = os.path.getsize(percorso_output)

            # Scrivi i risultati nel file CSV
            writer.writerow({'wav_filename': nome_file_output+".wav", 'wav_filesize': dimensione_file, 'transcript': nome_file_senza_parentesi})
