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
im = QPixmap.grabWindow(QApplication.desktop().winId()).toImage()

im = QImageToCvMat(im)
print im.shape
cv2.imshow("ha", im)
cv2.waitKey(0)
'''
for x in range(0,20):
    for y in range(0,20):
        c = im.pixel(x,y)
        print c
        colors = QColor(c).getRgbF()
        print "(%s,%s) = %s" % (x, y, colors)
'''
