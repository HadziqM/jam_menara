import cv2
from datetime import datetime as dt
import math as mt


def alpha1(bg, bg2):
    alp = bg[:, :, 3]
    beta = alp-255
    res = cv2.bitwise_and(bg, bg, mask=alp)
    res2 = cv2.bitwise_and(bg2, bg2, mask=beta)
    return cv2.add(res, res2)


def background(back):
    bg = cv2.imread("jam kuno.png", cv2.IMREAD_UNCHANGED)
    bg2 = back
    y, x, _ = bg.shape
    roi = bg[0+8:y-8, 0+8:x-8]
    res = alpha1(bg2, roi)
    bg[0+8:y-8, 0+8:x-8] = res
    return bg


def foto(background):
    bg = cv2.imread("founder.png", cv2.IMREAD_UNCHANGED)
    bg2 = cv2.imread("jam kuno3.png", cv2.IMREAD_UNCHANGED)
    y, x, _ = bg2.shape
    print(y)
    bg = cv2.resize(bg, (x-50, y-50), cv2.INTER_AREA)
    roi = bg2[0+25:y-25, 0+25:x-25]
    res = alpha1(bg, roi)
    bg2[0+25:y-25, 0+25:x-25] = res
    y2, x2, _ = background.shape
    print(y2)
    dif = int((y2-y)/2)
    residu = (y2-y) - 2*dif
    roi2 = background[0+dif:y2-dif+residu, 0+dif:x2-dif+residu]
    res2 = alpha1(bg2, roi2)
    background[0+dif:y2-dif+residu, 0+dif:x2-dif+residu] = res2
    return background


def draw_time(background):
    alp = background.copy()
    h, w, _ = background.shape
    center = (int(h/2), int(w/2))
    radius = int(w/2*mt.sqrt(2))
    color = (0, 0, 0)
    now = dt.now().time()
    hour = mt.fmod(now.hour, 12)
    minute = now.minute
    second = now.second

    sec_ang = mt.fmod(second * 6 + 270, 360)
    minute_ang = mt.fmod(minute * 6 + 270, 360)
    hour_ang = mt.fmod((hour * 30) + (minute / 2) + 270, 360)

    sec_x = center[0] + radius * mt.cos(sec_ang * mt.pi / 180)
    sec_y = center[1] + radius * mt.sin(sec_ang * mt.pi / 180)
    cv2.line(background, center, (int(sec_x), int(sec_y)), color, 3)

    minute_x = center[0] + (radius) * mt.cos(minute_ang * mt.pi / 180)
    minute_y = center[1] + (radius) * mt.sin(minute_ang * mt.pi / 180)
    cv2.line(background, center, (int(minute_x), int(minute_y)), color, 10)

    hour_x = center[0] + (radius) * mt.cos(hour_ang * mt.pi / 180)
    hour_y = center[1] + (radius) * mt.sin(hour_ang * mt.pi / 180)
    cv2.line(background, center, (int(hour_x), int(hour_y)), color, 20)

    background[:, :, 3] = alp[:, :, 3]

    return background


bg = cv2.imread("jam kuno1.png", cv2.IMREAD_UNCHANGED)

while True:
    cp = bg.copy()
    res = draw_time(cp)
    res = background(res)
    res = foto(res)
    cv2.imshow("test", res)
    cv2.waitKey(10)
# res = draw_time(bg)
# cv2.imshow("test", res[:, :, 3])
# cv2.waitKey(0)
