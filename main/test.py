import tkinter as tk

def afficher_coup(coup):
    # Ajouter le coup à la liste des coups joués
    coups_joues.append(coup)

    # Effacer le canevas pour rafraîchir l'affichage
    canvas.delete("coups_joues")

    # Réinitialiser la position Y
    y_position = 20

    # Réafficher tous les coups joués
    for index, coup in enumerate(coups_joues, start=1):
        # Ajouter le numéro de coup et le coup joué
        texte = f"{index}. {coup} "
        # Ajouter le texte sur le canevas avec une position Y fixe et une position X variable
        canvas.create_text(10, y_position, text=texte, anchor="nw", tag="coups_joues")
        # Incrémenter la position Y pour passer à la ligne suivante
        y_position += 20

# Fonction pour gérer un clic sur le canevas
def on_click(event):
    # Exemple : Ajouter un coup et afficher les coups joués
    afficher_coup("e4")
    afficher_coup("e5")
    afficher_coup("Nf3")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Affichage des coups joués")

# Création du canevas
canvas = tk.Canvas(root, width=200, height=200)
canvas.pack()

# Initialisation de la liste des coups joués
coups_joues = []

# Liaison de la fonction on_click à l'événement clic sur le canevas
canvas.bind("<Button-1>", on_click)

# Lancement de la boucle principale
root.mainloop()
