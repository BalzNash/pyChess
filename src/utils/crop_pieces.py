import xml.etree.ElementTree as ET
from PIL import Image
from .. import definitions

cut_coords = []

root = ET.parse('pieces.xml').getroot()
for cut_tag in root.findall('animation/cut'):
    coord = (float(cut_tag.get('x')), float(cut_tag.get('y')), float(cut_tag.get('x')) + 39, float(cut_tag.get('y')) + 39)
    cut_coords.append(coord)

i = 0
for coord in cut_coords:
    img = Image.open("chess_pieces.png")
    img2 = img.crop((coord))
    img2.save("piece{0}.png".format(i))
    i += 1


