#coding=utf-8
from pykeyboard import PyKeyboard
from PyQt4.QtGui import QImage, QPixmap, QApplication, QColor
import numpy as np
import sys
import time
import cv2

def QImageToCvMat(incomingImage):
    '''  Converts a QImage into an opencv MAT format  '''

    incomingImage = incomingImage.convertToFormat(QImage.Format_RGB32)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.constBits()
    ptr.setsize(incomingImage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    return arr

kb = PyKeyboard()
'''
while 1:
    kb.tap_key(" ")
    time.sleep(1)
'''

app = QApplication(sys.argv)
game_im = QPixmap.grabWindow(QApplication.desktop().winId()).toImage()
game_im = QImageToCvMat(game_im)
btn_im = cv2.imread("button.png")

game_gim = cv2.cvtColor(game_im, cv2.COLOR_BGRA2GRAY)
btn_gim = cv2.cvtColor(btn_im, cv2.COLOR_BGRA2GRAY)

lower = 80
upper = 100
res = (game_im[:,:,0] >= lower) & (game_im[:,:,1] >= lower) & (game_im[:,:,2] >= lower)
res = res & (game_im[:,:,0] <= upper) & (game_im[:,:,1] <= upper) & (game_im[:,:,2] <= upper)
game_im[~res] = 255

#kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))
#game_im = cv2.morphologyEx(game_im, cv2.MORPH_OPEN, kernel)
#game_im = cv2.morphologyEx(game_im, cv2.MORPH_CLOSE, kernel)

res = cv2.matchTemplate(game_gim, btn_gim, cv2.TM_SQDIFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  
print min_val, max_val, min_loc, max_loc

if min_val > 0.10:
    print ("Not Found Game")
    sys.exit(0)
#cv2.imshow("ha2", res)
#cv2.waitKey(0)

LOC = min_loc
BUTTON_X = 282
BUTTON_Y = 75
SCREEN_W = 600
SCREEN_H = 150
SCREEN_X = LOC[0] - BUTTON_X
SCREEN_Y = LOC[1] - BUTTON_Y

while 1:
    game_im = QPixmap.grabWindow(QApplication.desktop().winId(), x = SCREEN_X, y = SCREEN_Y, width = SCREEN_W, height = SCREEN_H).toImage()
    game_im = QImageToCvMat(game_im)
    CHECK_X = 110
    CHECK_Y = 113
    CHECK_W = 5
    CHECK_H = 5
    if (game_im[CHECK_Y:CHECK_Y+CHECK_H, CHECK_X:CHECK_X+CHECK_W, 0] != 255).any():
        kb.tap_key(" ")
    game_im[CHECK_Y:CHECK_Y+CHECK_H, CHECK_X:CHECK_X+CHECK_W, 0] = 0
    game_im[CHECK_Y:CHECK_Y+CHECK_H, CHECK_X:CHECK_X+CHECK_W, 1] = 0
    game_im[CHECK_Y:CHECK_Y+CHECK_H, CHECK_X:CHECK_X+CHECK_W, 2] = 255
    cv2.imshow("game", game_im)
    cv2.waitKey(25)
    #time.sleep(1)
