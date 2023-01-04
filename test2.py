import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
import pandas as pd

# Création de la fenêtre principale
window = tk.Tk()
window.title("GBmail")
window.geometry("700x500")
window.configure(bg="black")

# Création d'un canevas qui servira de fond noir
canvas = tk.Canvas(window, bg='black', width=700, height=500)
canvas.pack()

# Création d'un titre
label = tk.Label(canvas, text='GBmail', font=('helvetica', 16, 'bold'), bg='black', fg='white')
label.pack(pady=20)

# Configuration de l'image de fond
image = PhotoImage(file='fond.png')
image = image.zoom(2)
image = image.subsample(2)
fond = tk.Label(image=image)
fond.pack()

# Création du frame des boutons
button_frame = tk.Frame(window, bg='black')
button_frame.pack(pady=20)

# Création d'un bouton pour ouvrir une boîte de dialogue de chargement de fichier
def load_csv():
  filepath = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
  csv_path.set(filepath)

load_csv_button = tk.Button(button_frame, text="Charger un fichier CSV", command=load_csv)

# Configuration du style du bouton
load_csv_button.config(bg='#4285f4', fg='white', font=('helvetica', 12))

load_csv_button.pack(side='left', padx=5) # Ajout de l'espace entre les boutons

# Création d'un bouton pour lancer l'algorithme
def run_algorithm():
  filepath = csv_path.get()
  
  # Vérifiez si un fichier a bien été chargé
  if not filepath:
    tk.messagebox.showwarning("Aucun fichier chargé", "Vous devez charger un fichier CSV avant de lancer l'algorithme")
    return

  # Chargement du fichier CSV en utilisant Pandas
  df = pd.read_csv(filepath)

  # Traitement des données du DataFrame avec votre algorithme de nettoyage et de feature extraction
  features = clean_and_extract_features(df)

  # Appel de votre modèle SVM pour effectuer la classification
  prediction = svm_model.predict(features)

  # Affichage des résultats dans une fenêtre de message
  tk.messagebox.showinfo("Résultats", f"Prédiction : {prediction}")

run_algorithm_button = tk.Button(button_frame, text="Lancer l'algorithme", command=run_algorithm)

# Configuration du style du bouton
run_algorithm_button.config(bg='#4285f4', fg='white', font=('helvetica', 12))

run_algorithm_button.pack(side='left', padx=5) # Ajout de l'espace entre les boutons

# Création d'un bouton pour ouvrir un tutoriel d'utilisation
def open_tutorial():
  messagebox.showinfo("Tutoriel", "Ceci est un tutoriel d'utilisation de l'interface GBmail.\n\nPour charger un fichier CSV, cliquez sur le bouton 'Charger un fichier CSV'.\nPour lancer l'algorithme, cliquez sur le bouton 'Lancer l'algorithme'.\n\nAssurez-vous d'avoir chargé un fichier CSV avant de lancer l'algorithme.")

help_button = tk.Button(button_frame, text='?', command=open_tutorial)

# Configuration du style du bouton
help_button.config(bg='white', fg='#4285f4', font=('helvetica', 14, 'bold'))

help_button.pack(side='right') # Ajout du bouton à droite de la fenêtre

# Création d'une variable qui stockera le chemin du fichier CSV chargé
csv_path = tk.StringVar()

# Création d'un label qui affichera le chemin du fichier CSV chargé
csv_label = tk.Label(window, textvariable=csv_path, font=('helvetica', 12))
csv_label.pack()

window.mainloop()

