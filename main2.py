from asyncore import loop
from tkinter import Tk, Label
import math as mt
from PIL import Image, ImageTk
from datetime import datetime as dt


class normal():
    def __init__(self, size):
        self.size = size
        self.det = [Image.open(
            f"media3//d{i+1}.png").resize((size, size)) for i in range(60) if (i+1) % 5 != 0]
        self.men = [Image.open(
            f"media3//m{i}.png").resize((size, size)) for i in range(60)]
        self.jam = [Image.open(
            f"media3//j{i+1}.png").resize((size, size)) for i in range(12)]
        self.bg = Image.open("media3//bg.png").resize((size, size))
        self.bgj = Image.open("media3//full_hour.png").resize((size, size))

    def draw_hour(self, bg):
        now = dt.now().time()
        hour = int(mt.fmod(now.hour, 12))

        return Image.alpha_composite(Image.alpha_composite(bg, self.bgj), self.jam[hour-1])

    def draw_minute(self, bg):
        now = dt.now().time()
        minutes = now.minute

        return Image.alpha_composite(bg, self.men[minutes])

    def draw_sec(self, bg):
        now = dt.now().time()
        seconds = now.second

        if seconds % 5 != 0:
            return Image.alpha_composite(bg, self.det[seconds-1 - int(seconds/5)])
        else:
            return bg


class kinter(Tk):
    def __init__(self, norm):
        super().__init__()
        self.title('Jam menara Masjid')
        self.resizable(0, 0)
        self.geometry(f'{norm.size}x{norm.size}')

        self.label1 = Label(self)
        self.label1.pack()
        self.norm = norm

    def loop(self):
        return self.norm.draw_hour(self.norm.draw_sec(self.norm.draw_minute(self.norm.bg)))

    def passm(self):
        image = ImageTk.PhotoImage(self.loop())
        self.label1.image = image
        self.label1.configure(image=image)
        self.label1.after(1000, self.passm)


if __name__ == '__main__':
    norm = normal(400)
    tkin = kinter(norm)
    # norm.draw_hour(norm.draw_minute(norm.draw_sec(norm.bg))).show()
    tkin.passm()
    tkin.mainloop()
