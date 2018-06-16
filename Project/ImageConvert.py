from PIL import Image

def RGBtoRGBA(path):
    return Image.open(path).convert("RGBA")