from PIL import Image, ImageDraw

desired_size = 800

img = Image.open('publicidad.jpg')
print(img.size)

# Se ajusta tamaño de la imagen
old_size = img.size
ratio = float(desired_size)/max(old_size)
new_size = tuple([int(x*ratio) for x in old_size])
img = img.resize(new_size, Image.ANTIALIAS)
print(img.size)

# se comenta la imagen con el nombre del diseñador y fecha
draw = ImageDraw.Draw(img)
draw.text((10, 10), "Diseñador y fecha", fill="white")

# Se guarda nueva imagen
img.save('publicidad_new.png')
