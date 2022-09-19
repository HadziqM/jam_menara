from pickletools import uint8
import cv2
from datetime import datetime as dt
import math as mt
import numpy as np


class assembler():
    def __init__(self, size):
        self.size = size

    def remove_from_alpha(self, pic):
        alpha = pic[:, :, 3]
        return [cv2.bitwise_and(pic, pic, mask=alpha), alpha]

    def remove_from_mask(self, pic, mask):
        return cv2.bitwise_and(pic, pic, mask=mask)

    def remove_alpha(self, pic):
        return cv2.cvtColor(pic, cv2.COLOR_BGRA2BGR)

    def fussion(self, pic1, pic2):
        return cv2.add(pic1, pic2)

    def save_to_media(self, pic, name):
        cv2.imwrite('media2\\'+name, pic)
        return "success"

    def open_from_media(self, name):
        return cv2.resize(cv2.imread('media2\\'+name, cv2.IMREAD_UNCHANGED), (self.size, self.size), interpolation=cv2.INTER_AREA)

    def open_from_media_grey(self, name):
        return cv2.resize(cv2.imread('media2\\'+name, cv2.IMREAD_REDUCED_GRAYSCALE_2), (self.size, self.size), interpolation=cv2.INTER_AREA)

    def draw_time(self, background1):
        center = (int(self.size/2), int(self.size/2))
        radius = int(self.size/2*mt.sqrt(2))
        now = dt.now().time()
        hour = mt.fmod(now.hour, 12)
        minute = now.minute
        second = now.second
        background = background1.copy()

        sec_ang = mt.fmod(second * 6 + 270, 360)
        minute_ang = mt.fmod(minute * 6 + 270, 360)
        hour_ang = mt.fmod((hour * 30) + (minute / 2) + 270, 360)

        sec_x = center[0] + radius * mt.cos(sec_ang * mt.pi / 180)
        sec_y = center[1] + radius * mt.sin(sec_ang * mt.pi / 180)
        cv2.line(background, center, (int(sec_x), int(sec_y)), (255, 0, 0), 3)

        minute_x = center[0] + (radius - 20) * mt.cos(minute_ang * mt.pi / 180)
        minute_y = center[1] + (radius - 20) * mt.sin(minute_ang * mt.pi / 180)
        cv2.line(background, center, (int(minute_x),
                 int(minute_y)), (255, 0, 0), 10)

        hour_x = center[0] + (radius - 50) * mt.cos(hour_ang * mt.pi / 180)
        hour_y = center[1] + (radius - 50) * mt.sin(hour_ang * mt.pi / 180)
        cv2.line(background, center, (int(hour_x),
                 int(hour_y)), (255, 0, 0), 15)

        return background


def start(size):
    ass = assembler(size)
    pic = ass.remove_alpha(ass.open_from_media('jam1.png'))
    pic2 = ass.remove_alpha(ass.remove_from_alpha(
        ass.open_from_media('jam3.png'))[0])
    pic3, mask = ass.remove_from_alpha(ass.open_from_media('jam4.png'))
    pic3 = ass.remove_alpha(pic3)
    pic23 = ass.remove_from_mask(pic2, mask-255)
    front = ass.fussion(pic3, pic23)
    side = ass.remove_alpha(ass.remove_from_alpha(
        ass.open_from_media('jam.png'))[0])
    ass.save_to_media(side, 'side.jpg')
    ass.save_to_media(ass.remove_alpha(
        ass.open_from_media('jam.png')), 'side1.jpg')
    mask_front = ass.remove_from_alpha(ass.open_from_media('jam3.png'))[1]-255
    ret, mask_side = cv2.threshold(ass.open_from_media_grey(
        'anjir.jpg'), 127, 255, cv2.THRESH_BINARY)
    return ass, [front, side, pic, mask_front, mask_side]


if __name__ == '__main__':
    nsize = 300
    damn, you = start(nsize)
    jam = you[2].copy()
    size = (768, 1366, 3)
    scr = np.zeros(size, np.uint8,)+255
    cv2.namedWindow('test', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('test', cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    while True:
        drw = damn.draw_time(jam)
        rmv = damn.remove_from_mask(
            damn.remove_from_mask(drw, you[-1]), you[-2])
        q1 = damn.fussion(damn.fussion(rmv, you[0]), you[1])
        scr[0:nsize, 0:nsize] = q1
        cv2.imshow('test', scr)
        cv2.waitKey(2)
        # cv2.imshow('test2', you[-1])
