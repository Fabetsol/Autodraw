"""
Autodraw, by Fabetsol (last modification : 28/05/2021)
Please, do not repost.
Read the "README.txt" file to learn how to use Autodraw.
"""

import time
import requests
from PIL import Image
from pynput import mouse
from pynput.mouse import Button, Controller
from pickle import *
from math import *
import pyperclip
import tkinter

souris = Controller()
inputs = (None,None)

pixelsize = 5
def multiTuple(tuple1, tuple2):
    first = (tuple1[0]*tuple2[0])
    second = (tuple1[1]*tuple2[1])
    return (round(first),(round(second)))

def diviseTuple(tuple1, tuple2):
    first = (tuple1[0]/tuple2[0])
    second = (tuple1[1]/tuple2[1])
    return (round(first),(round(second)))

with open("configs","rb") as f: associations = load(f); coef = load(f)

def on_click(x, y, button, pressed):
    if pressed and button == Button.left: global inputs ; inputs = (x,y)
    else: return False

def is_similar(pixel_a, pixel_b):
    x1 = pixel_a[0]
    y1 = pixel_a[1]
    z1 = pixel_a[2]
    x2 = pixel_b[0]
    y2 = pixel_b[1]
    z2 = pixel_b[2]
    return sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

def getPos():
    with mouse.Listener(on_click=on_click) as listener:listener.join()
    départ = inputs
    with mouse.Listener(on_click=on_click) as listener:listener.join()
    fin = inputs
    return départ, fin

def autodraw(départ, fin, link, white):

    h = fin[1] - départ[1]
    w = fin[0] - départ[0]

    image = Image.open(requests.get(link, stream=True).raw)
    image = image.resize(diviseTuple(multiTuple((w,h),coef),(pixelsize,pixelsize)))

    if white == 0:
        allcolor = []
        for color in associations.keys():
            allcolor.append(is_similar(color,(255,255,255)))
        if min(allcolor) < 30: whitepos = list(associations.values())[allcolor.index(min(allcolor))]
        else:white = 1; whitepos = None
    else:whitepos = None

    pixels = []
    for i in range(image.size[1]):
        line = []
        for j in range(image.size[0]):
            similarity = []
            for color in associations.keys() :similarity.append(is_similar(image.getpixel((j, i)), color))
            line.append(list(associations.values())[similarity.index(min(similarity))])
        pixels.append(list(line))

    time.sleep(2)
    for color in associations.values():
        if not (white == 0 and color == whitepos):
            iscolor = False
            for ligne in pixels:
                if color in ligne: iscolor = True
            if iscolor:
                time.sleep(0.02)
                souris.position = color
                time.sleep(0.02)
                souris.click(Button.left, 2)
                time.sleep(0.02)
                for i in range(image.size[1]):
                    for j in range(image.size[0]):
                        if pixels[i][j] == color:
                            souris.position = (multiTuple((départ[0]+j*pixelsize, départ[1]+i*pixelsize),coef))
                            souris.press(Button.left)
                            souris.release(Button.left)

root = tkinter.Tk()
root.title("Autodraw")

départ = "Undifined"
fin = "Undifined"
clip = tkinter.IntVar()
white = tkinter.IntVar()

def positions():
    global départ, fin, root, se
    root.state("withdrawn")
    départ, fin = getPos()
    root.state("normal")
    if fin[1] - départ[1] < 0 or fin[0] - départ[0] < 0 : linktext.config(text = "The end point must be lower and more to the right than the start point !"); return
    se.config(text = f"Start : {str(départ)} | End : {str(fin)}")

def paste():
    global Link
    Link.insert(0, "")
    Link.insert(0, pyperclip.paste())

def draw():
    global Link, départ, fin, root, clip, white
    if départ == "Undifined" or fin == "Undifined": linktext.config(text = "Please, set a start point and a end point !"); return

    if fin[1] - départ[1] < 0 or fin[0] - départ[0] < 0 : linktext.config(text = "The end point must be lower and more to the right than the start point !"); return

    if clip.get() == 1 :linkpicture = ""; linkpicture = pyperclip.paste()
    else: linkpicture = Link.get()

    try : Image.open(requests.get(linkpicture, stream=True).raw)
    except : linktext.config(text = "Please, put a valid image link !"); return

    root.state("withdrawn")
    autodraw(départ, fin, linkpicture, white.get())
    root.state("normal")

def lockLinkSpaces():
    global Link, linkbutton, clip
    if clip.get() == 1: Link["state"] = "disabled"; linkbutton["state"] = "disabled"
    else: Link["state"] = "normal" ; linkbutton["state"] = "normal"

linktext = tkinter.Label(text = "Put the link of the image to copy below :");linktext.pack()
Link = tkinter.Entry();Link.pack()
linkbutton = tkinter.Button(text = "Paste from clipboard", command = paste);linkbutton.pack()
linkcheck = tkinter.Checkbutton(text = "Always take from clipboard",variable = clip, onvalue=1, offvalue=0, command = lockLinkSpaces); linkcheck.pack()
space1 = tkinter.Label(text = " ");space1.pack()
seButton = tkinter.Button(text = "Set Start and End", command = positions);seButton.pack()
se = tkinter.Label(text = f"Start : {str(départ)} | End : {str(fin)}");se.pack()
space2 = tkinter.Label(text = " ");space2.pack()
whitecheck = tkinter.Checkbutton(text = "Draw white pixels", variable = white, onvalue = 1, offvalue = 0); whitecheck.pack()
space3 = tkinter.Label(text = " ");space3.pack()
launchButton = tkinter.Button(text = "Draw", command = draw);launchButton.pack()

root.mainloop()