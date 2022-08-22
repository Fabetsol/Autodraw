"""
Autodraw, by Fabetsol (last modification : 27/08/2021)
Please, do not repost.
Read the "README.txt" file to learn how to use Autodraw.
"""

import time
import requests
from PIL import Image, ImageGrab, ImageDraw
from pynput import mouse
from pynput.mouse import Button, Controller
from pickle import *
from math import *
import pyperclip
import tkinter as tk
from tkinter import ttk
import tkinter.colorchooser

souris = Controller()
inputs = (None,None)
PIXELSIZE = 5
textcolor = "black"

def multiTuple(tuple1, tuple2, Round:bool=True):
    first = (tuple1[0]*tuple2[0])
    second = (tuple1[1]*tuple2[1])
    return (round(first),(round(second))) if Round else (first,second)

def diviseTuple(tuple1, tuple2, Round:bool=True):
    first = (tuple1[0]/tuple2[0])
    second = (tuple1[1]/tuple2[1])
    return (round(first),(round(second))) if Round else (first,second)

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
    START = inputs
    with mouse.Listener(on_click=on_click) as listener:listener.join()
    FIN = inputs
    return START, FIN

def color():
    global textcolor
    textcolor = tkinter.colorchooser.askcolor("black")[0]

def autodraw(START, FIN, link, white):

    h = FIN[1] - START[1]
    w = FIN[0] - START[0]

    image = Image.open(requests.get(link, stream=True).raw)
    image = image.resize(diviseTuple(multiTuple((w,h),coef),(PIXELSIZE,PIXELSIZE)))

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
                            souris.position = (multiTuple((START[0]+j*PIXELSIZE, START[1]+i*PIXELSIZE),coef))
                            souris.press(Button.left)
                            souris.release(Button.left)

def autodrawtext(START, FIN, text, color = "black"):

    h = FIN[1] - START[1]
    w = FIN[0] - START[0]

    image = Image.new("RGBA", (5000,5000), (0,0,0))
    draw = ImageDraw(image)
    wTexte, hTexte = draw.textsize(text)
    image = Image.new((wTexte,hTexte))
    draw = ImageDraw(image)
    draw.text((0,0), text)
    image = image.resize(diviseTuple(multiTuple((w,h),coef),(PIXELSIZE,PIXELSIZE)))

    allcolor = []
    for color in associations.keys():
        allcolor.append(is_similar(color,(255,255,255)))
    if min(allcolor) < 30: whitepos = list(associations.values())[allcolor.index(min(allcolor))]
    else:white = 1; whitepos = None

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
                            souris.position = (multiTuple((START[0]+j*PIXELSIZE, START[1]+i*PIXELSIZE),coef))
                            souris.press(Button.left)
                            souris.release(Button.left)

root = tk.Tk()
root.title("Autodraw")

n = ttk.Notebook(root); n.pack()
pictureDraw = ttk.Frame(n); pictureDraw.pack()
textDraw = ttk.Frame(n); textDraw.pack()
configFrame = ttk.Frame(n); configFrame.pack()
n.add(pictureDraw, text="Picture")
n.add(textDraw, text="Text")
n.add(configFrame, text="Config")

START = "Undifined"
FIN = "Undifined"
clip = tk.IntVar()
white = tk.IntVar()




def positions():
    global START, FIN, root, se, setext
    root.state("withdrawn")
    START, FIN = getPos()
    root.state("normal")
    if FIN[1] - START[1] < 0 or FIN[0] - START[0] < 0 : linktext.config(text = "The end point must be lower and more to the right than the start point !"); return
    se.config(text = f"Start : {str(START)} | End : {str(FIN)}")
    setext.config(text = f"Start : {str(START)} | End : {str(FIN)}")

def paste():
    global Link
    Link.insert(0, "")
    Link.insert(0, pyperclip.paste())

def pasteText():
    global Texte
    Texte.insert(0, "")
    Texte.insert(0, pyperclip.paste())

def draw():
    global Link, START, FIN, root, clip, white
    if START == "Undifined" or FIN == "Undifined": linktext.config(text = "Please, set a start point and a end point !"); return

    if FIN[1] - START[1] < 0 or FIN[0] - START[0] < 0 : linktext.config(text = "The end point must be lower and more to the right than the start point !"); return

    if clip.get() == 1 :linkpicture = ""; linkpicture = pyperclip.paste()
    else: linkpicture = Link.get()

    try : Image.open(requests.get(linkpicture, stream=True).raw)
    except : linktext.config(text = "Please, put a valid image link !"); return

    root.state("withdrawn")
    autodraw(START, FIN, linkpicture, white.get())
    root.state("normal")

def drawtext():
    global Texte, START, FIN, root, textcolor
    if START == "Undifined" or FIN == "Undifined": linktext.config(text = "Please, set a start point and a end point !"); return

    if FIN[1] - START[1] < 0 or FIN[0] - START[0] < 0 : linktext.config(text = "The end point must be lower and more to the right than the start point !"); return

    if clip.get() == 1 :text = ""; text = pyperclip.paste()
    else: text = Texte.get()

    root.state("withdrawn")
    textDraw(START, FIN, text, textcolor)
    root.state("normal")

def lockLinkSpaces():
    global Link, linkbutton, clip
    if clip.get() == 1: Link["state"] = "disabled"; linkbutton["state"] = "disabled"
    else: Link["state"] = "normal" ; linkbutton["state"] = "normal"

def config():
    global root, colorstext, colornumber

    try:int(colornumber.get())
    except: colorstext.config(text = "Please, put a number of colors to config !"); return

    root.state("withdrawn")
    associations = {}

    screenshot = ImageGrab.grab()
    print(1)

    souris.position = (screenshot.size)
    souris.move(-1,0); souris.move(1,0)

    coef = diviseTuple(souris.position,screenshot.size, False)

    for i in range(int(colornumber.get())):
        with mouse.Listener(on_click=on_click) as listener:listener.join()
        associations[screenshot.getpixel(inputs)] = multiTuple(inputs,coef)

    with open("configs","wb") as f:dump(associations, f); dump(coef, f)

    time.sleep(1.5)
    for position in associations.values():
        souris.position = position
        time.sleep(0.25)
    
    root.state("normal")

colorstext = tk.Label(configFrame, text = "How many colors do you want to set :"); colorstext.pack()
colornumber = tk.Entry(configFrame); colornumber.pack()
launch = tk.Button(configFrame, text = "Start configuration", command = config); launch.pack()

linktext = tk.Label(pictureDraw, text = "Put the link of the image to copy below :"); linktext.pack()
Link = tk.Entry(pictureDraw); Link.pack()
linkbutton = tk.Button(pictureDraw, text = "Paste from clipboard", command = paste); linkbutton.pack()
linkcheck = tk.Checkbutton(pictureDraw, text = "Always take from clipboard",variable = clip, onvalue=1, offvalue=0, command = lockLinkSpaces); linkbutton.pack()
space1 = tk.Label(pictureDraw, text = " "); space1.pack()
seButton = tk.Button(pictureDraw, text = "Set Start and End", command = positions); seButton.pack()
se = tk.Label(pictureDraw, text = f"Start : {str(START)} | End : {str(FIN)}"); se.pack()
space2 = tk.Label(pictureDraw, text = " "); space2.pack()
whitecheck = tk.Checkbutton(pictureDraw, text = "Draw white pixels", variable = white, onvalue = 1, offvalue = 0); whitecheck.pack()
launchButton = tk.Button(pictureDraw, text = "Draw", command = draw);launchButton.pack()

textTexte = tk.Label(textDraw, text = "Put the link of the image to copy below :"); textTexte.pack()
Texte = tk.Entry(textDraw); Texte.pack()
TexteButton = tk.Button(textDraw, text = "Paste from clipboard", command = pasteText); TexteButton.pack()
Textcolorbutton = tk.Button(textDraw, text = "Choose Text Color", command = color); Textcolorbutton.pack()
space5 = tk.Label(textDraw, text = " "); space5.pack()
seButtontext = tk.Button(textDraw, text = "Set Start and End", command = positions); seButtontext.pack()
setext = tk.Label(textDraw, text = f"Start : {str(START)} | End : {str(FIN)}"); setext.pack()
space6 = tk.Label(textDraw, text = " "); space6.pack()
launchButtontext = tk.Button(textDraw, text = "Draw", command = drawtext); launchButtontext.pack()

root.mainloop()