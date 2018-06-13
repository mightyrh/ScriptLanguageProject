from tkinter import *
from io import BytesIO
import urllib.request
from PIL import Image, ImageTk

root = Tk()
root.geometry("500x500+500+200")

# openapi로 이미지 url을 가져옴.
url = "https://maps.googleapis.com/maps/api/staticmap?center=40.714728,-73.998672&zoom=13&size=400x400&key=AIzaSyCWJAM-nuDT2BaF08b6VR9dQXn3um7puaA"
with urllib.request.urlopen(url) as u:
    raw_data = u.read()

im = Image.open(BytesIO(raw_data))
image = ImageTk.PhotoImage(im)

label = Label(root, image=image, height=400, width=400)
label.pack()
label.place(x=0, y=0)
root.mainloop()