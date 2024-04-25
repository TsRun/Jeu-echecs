# On a besoin d'importer Image de PIL pour ouvrir et analyser l'image uploadée
from PIL import Image
import collections

# Chemin de l'image uploadée
image_path = 'images/capture.png'

# Ouvrir l'image
img = Image.open(image_path)

# Convertir l'image en liste de pixels
pixels = list(img.getdata())

# Création d'un Counter pour compter les occurrences de chaque couleur
color_counter = collections.Counter(pixels)

# Récupérer les 10 couleurs les plus communes
most_common_colors = color_counter.most_common(10)

# Fermer l'image pour libérer des ressources
img.close()

from PIL import Image, ImageDraw

print(most_common_colors)

# Créer une nouvelle image avec un fond blanc
width, height = 400, 400  # ou la taille que vous préférez
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# La largeur de chaque bande de couleur
bar_width = width // len(most_common_colors)

# Dessiner chaque couleur comme une bande horizontale
for i, (color, _) in enumerate(most_common_colors):
    draw.rectangle([i * bar_width, 0, (i + 1) * bar_width, height], fill=color)

# Afficher l'image
image.show()


