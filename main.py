import cv2 as cv
import math as mt
from tkinter import Tk, Label, mainloop
from PIL import Image, ImageTk
from datetime import datetime as dt
from configparser import ConfigParser


def config(section, filename="jam.ini"):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return db


class pars:
    def __init__(self):
        a = config("jam")
        self.color = a["color"]
        self.size = a["size"]
        self.gambar = a["picture"]


parsing = pars()
size = int(parsing.size)
take = tuple(int(parsing.color[1:][i: i + 2], 16) for i in (0, 2, 4))
color = ()
for i in reversed(take):
    color = color + (i,)

win = Tk()
win.geometry(f"{size}x{size}")
label = Label(win)
label.grid(row=0, column=0)


radius = int(size * 3 / 8)
center = (int(size / 2), int(size / 2))


bg = cv.imread(parsing.gambar, cv.IMREAD_UNCHANGED)
bg = cv.resize(bg, [size, size], cv.INTER_AREA)


def draw_time(background):
    now = dt.now().time()
    hour = mt.fmod(now.hour, 12)
    minute = now.minute
    second = now.second

    sec_ang = mt.fmod(second * 6 + 270, 360)
    minute_ang = mt.fmod(minute * 6 + 270, 360)
    hour_ang = mt.fmod((hour * 30) + (minute / 2) + 270, 360)

    sec_x = center[0] + radius * mt.cos(sec_ang * mt.pi / 180)
    sec_y = center[1] + radius * mt.sin(sec_ang * mt.pi / 180)
    cv.line(background, center, (int(sec_x), int(sec_y)), color, 3)

    minute_x = center[0] + (radius - 20) * mt.cos(minute_ang * mt.pi / 180)
    minute_y = center[1] + (radius - 20) * mt.sin(minute_ang * mt.pi / 180)
    cv.line(background, center, (int(minute_x), int(minute_y)), color, 8)

    hour_x = center[0] + (radius - 70) * mt.cos(hour_ang * mt.pi / 180)
    hour_y = center[1] + (radius - 70) * mt.sin(hour_ang * mt.pi / 180)
    cv.line(background, center, (int(hour_x), int(hour_y)), color, 15)

    return background


def loop1():
    bg1 = bg.copy()
    disp = draw_time(bg1)
    image = cv.cvtColor(disp, cv.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    label.image = image
    label.configure(image=image)
    label.after(1000, loop1)
    mainloop()


label.after(1000, loop1)
mainloop()
