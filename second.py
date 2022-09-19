import cv2 as cv
import math as mt
import numpy as np
from tkinter import Tk, Label
from PIL import Image, ImageTk
from datetime import datetime as dt
from configparser import ConfigParser


class pars:
    def __init__(self):
        a = self.config("menara")
        self.color_in = self.rgb_conv(a["color_inner"])
        self.color_out = self.rgb_conv(a["color_outer"])
        self.size = int(a["size"])
        self.gambar = "media\\"+a["picture"]
        self.photo = "media\\"+a["photo"]
        self.pin = "media\\"+a["pin"]
        self.hide = a["hide"]
        self.radius = int(self.size * 3 / 8)
        self.center = (int(self.size / 2), int(self.size / 2))

        self.bg = cv.imread(self.gambar, cv.IMREAD_UNCHANGED)
        self.bg = cv.cvtColor(self.bg, cv.COLOR_BGRA2BGR)
        self.bg = cv.resize(self.bg, [self.size, self.size], cv.INTER_AREA)
        self.pict = cv.imread(self.photo, cv.IMREAD_UNCHANGED)
        self.pict = cv.cvtColor(self.pict, cv.COLOR_BGRA2BGR)
        self.logo = cv.imread(self.pin, cv.IMREAD_UNCHANGED)
        self.logo = cv.cvtColor(self.logo, cv.COLOR_BGRA2BGR)

    def rgb_conv(self, color):
        take = tuple(int(color[1:][i: i + 2], 16) for i in (0, 2, 4))
        rgb = ()
        for i in reversed(take):
            rgb = rgb + (i,)
        return rgb

    def config(self, section, filename="media\\jam.ini"):
        parser = ConfigParser()
        parser.read(filename)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(
                "Section {0} not found in the {1} file".format(
                    section, filename)
            )

        return db

    def picture(self, bg, pict, par):
        d = int(par * self.size)
        r = int(d/2)
        residu = d - 2*r
        pict = cv.resize(pict, [d, d], cv.INTER_AREA)
        roi = bg[(self.center[0]-r):(self.center[0]+r+residu),
                 (self.center[1]-r):(self.center[1]+r+residu)]
        mask1 = np.zeros((d, d, 1), np.uint8)
        mask1 = cv.circle(mask1, (r, r), r, (255, 255, 255), -1)
        mask2 = 255-mask1
        roi = cv.bitwise_and(roi, roi, mask=mask2)
        pict = cv.bitwise_and(pict, pict, mask=mask1)
        res = cv.add(roi, pict)
        bg[(self.center[0]-r):(self.center[0]+r+residu),
           (self.center[1]-r):(self.center[1]+r+residu)] = res
        return bg

    def draw_time(self, background):
        center = self.center
        radius = self.radius
        color = self.color_in
        color2 = self.color_out
        now = dt.now().time()
        hour = mt.fmod(now.hour, 12)
        minute = now.minute
        second = now.second

        sec_ang = mt.fmod(second * 6 + 270, 360)
        minute_ang = mt.fmod(minute * 6 + 270, 360)
        hour_ang = mt.fmod((hour * 30) + (minute / 2) + 270, 360)

        sec_x = center[0] + radius * mt.cos(sec_ang * mt.pi / 180)
        sec_y = center[1] + radius * mt.sin(sec_ang * mt.pi / 180)
        cv.line(background, center, (int(sec_x), int(sec_y)), color2, 3)

        minute_x = center[0] + (radius - 20) * mt.cos(minute_ang * mt.pi / 180)
        minute_y = center[1] + (radius - 20) * mt.sin(minute_ang * mt.pi / 180)
        minute_x2 = center[0] + (radius - 10) * \
            mt.cos(minute_ang * mt.pi / 180)
        minute_y2 = center[1] + (radius - 10) * \
            mt.sin(minute_ang * mt.pi / 180)
        cv.line(background, center, (int(minute_x2), int(minute_y2)), color2, 10)
        cv.line(background, center, (int(minute_x), int(minute_y)), color, 7)

        hour_x = center[0] + (radius - 50) * mt.cos(hour_ang * mt.pi / 180)
        hour_y = center[1] + (radius - 50) * mt.sin(hour_ang * mt.pi / 180)
        hour_x2 = center[0] + (radius - 40) * mt.cos(hour_ang * mt.pi / 180)
        hour_y2 = center[1] + (radius - 40) * mt.sin(hour_ang * mt.pi / 180)
        cv.line(background, center, (int(hour_x2), int(hour_y2)), color2, 15)
        cv.line(background, center, (int(hour_x), int(hour_y)), color, 12)

        return background


class watch(Tk):
    def __init__(self):
        super().__init__()

        par = pars()
        size = int(par.size)
        self.title('Jam menara Masjid')
        self.resizable(0, 0)
        self.geometry(f'{size}x{size}')

        self.label1 = Label(self)
        self.label1.pack()
        self.label1.after(1000, self.update)

    def none(self):
        return None

    def test(self):
        par = pars()
        if par.hide == "true":
            return par.picture(par.picture(par.draw_time(par.bg), par.pict, 0.45), par.logo, 0.1)
        return par.picture(par.draw_time(par.picture(par.bg, par.pict, 0.45)), par.logo, 0.1)

    def update(self):
        image = cv.cvtColor(self.test(), cv.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.label1.image = image
        self.label1.configure(image=image)
        self.label1.after(1000, self.update)


ws = watch()
ws.mainloop()
