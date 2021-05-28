from PIL import ImageGrab
from pynput import mouse
from pynput.mouse import Controller
from pickle import *
import time
import tkinter
souris = Controller()

root = tkinter.Tk()
root.title("Autodraw CONFIG")

inputs = (None,None)
def on_click(x, y, button, pressed):
    if pressed: global inputs ; inputs = (x,y)
    else: return False

def diviseTuple(tuple1, tuple2):
    first = (tuple1[0]/tuple2[0])
    second = (tuple1[1]/tuple2[1])
    return (first,second)

def multiTuple(tuple1, tuple2):
    first = (tuple1[0]*tuple2[0])
    second = (tuple1[1]*tuple2[1])
    return (round(first),(round(second)))

def config():
    global root, colorstext, colornumber

    try:int(colornumber.get())
    except: colorstext.config(text = "Please, put a number of colors to config !"); return

    root.state("withdrawn")
    associations = {}

    screenshot = ImageGrab.grab()

    souris.position = (screenshot.size)
    souris.move(-1,0);souris.move(1,0)

    coef = diviseTuple(souris.position,screenshot.size)

    for i in range(int(colornumber.get())):
        with mouse.Listener(on_click=on_click) as listener:listener.join()
        associations[screenshot.getpixel(inputs)] = multiTuple(inputs,coef)

    with open("configs","wb") as f:dump(associations, f); dump(coef, f)

    time.sleep(1.5)
    for position in associations.values():
        souris.position = position
        time.sleep(0.25)
    
    root.destroy()

colorstext = tkinter.Label(text = "How many colors do you want to set :")
colornumber = tkinter.Entry()
launch = tkinter.Button(text = "Start configuration", command = config)
colorstext.pack(); colornumber.pack(); launch.pack()

root.mainloop()