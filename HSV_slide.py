# -*- coding: utf-8 -*-
"""
Count Cell numbers using hsv space

Spyder Editor
Author Wanghaotian
This is a temporary script file.
"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import cv2
import os,sys

def mat2qpixmap(img):
    '''numpy.ndarray to qpixmap
    '''
    height, width = img.shape[:2]
    if img.ndim == 3:
        rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    elif img.ndim == 2:
        rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        raise Exception("Unstatisfied image data format!")
    qimage = QImage(rgb[:], width,height,width*3,QImage.Format_RGB888)
    qpixmap = QPixmap.fromImage(qimage)
    return qpixmap

def hsv2qpixmap(img):    #convert the bgr imgae into hsv and show it in widget
    '''numpy.ndarryto qpixmap
    '''
    height, width = img.shape[:2]
    if img.ndim == 3:
        hsvp = cv2.cvtColor(img,cv2.COLOR_HSV2RGB)
    elif img.ndim == 2:
        hsvp = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        raise Exception("Unstatisfied image data format!")
    qimage = QImage(hsvp[:], width,height,width*3,QImage.Format_RGB888)
    qpixmap = QPixmap.fromImage(qimage)
    return qpixmap

class ImageView(QWidget):   #the class to monitor the rgb
    def __init__(self, winname="ImageView"):
        super().__init__()
        self.setWindowTitle(winname)
        self.imageLabel = QLabel(self)
        self.imageLabel.setText(winname)
        self.show()
        
    def setPixmap(self,img):
        #img = cv2.imread("rwby.jpg")
        if img is not None:
            H,W = img.shape[:2]
            qpixmap = mat2qpixmap(img)
            self.imageLabel.setPixmap(qpixmap)
            self.resize(W,H)
            self.imageLabel.resize(W,H)
            
class HSVView(QWidget):    #the class to monitor the hsv
    def __init__(self, winname="HSVView"):
        super().__init__()
        self.setWindowTitle(winname)
        self.imageLabel = QLabel(self)
        self.imageLabel.setText(winname)
        self.show()
        
    def setPixmap(self,img):
        #img = cv2.imread("rwby.jpg")
        if img is not None:
            H,W = img.shape[:2]
            qpixmap = hsv2qpixmap(img)
            self.imageLabel.setPixmap(qpixmap)
            self.resize(W,H)
            self.imageLabel.resize(W,H)


class SliderHSVCounter(QWidget):
    '''slide bar  '''
    def __init__(self,img = None):
        super().__init__()
        if img is None:
            raise Exception("Image is Null")
            pass
        self.img = img
        self.hsvgauss = cv2.GaussianBlur(cv2.cvtColor(self.img,cv2.COLOR_BGR2HSV),(3,3),0)
        self.setWindowTitle("Th")
        self.ImageView = ImageView("Source")
        #self.HSVView = HSVView("HSV")
        self.ImageView.setPixmap(self.img)
        #self.HSVView.setPixmap(self.hsvgauss)
        
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.addSliders()
        self.show()
        
    def doInrange(self):
        th1 = self.slider1.value()
        th2 = self.slider2.value()
        th3 = self.slider3.value()
        #print(th1,th2,th3)
        self.setWindowTitle("TH:{}~{}~{}".format(th1,th2,th3))
        
        upper_t = np.array([255,255,255])
        lower_t = np.array([th1,th2,th3])
        
        #cannyed = cv2.Canny(self.gray,th1,th2)
        mask = cv2.inRange(self.hsvgauss,lower_t,upper_t) #inrange to select the
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        morphed = cv2.morphologyEx(mask, cv2.MORPH_OPEN,kernel,None,(-1,-1),1)
        
        _, cnts, _ = cv2.findContours(morphed,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        canvas = self.img.copy()
        #cv2.drawContours(canvas,cnts,-1,(0,211,211),1)
        
        #meanArea = 
        areaList = []
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            areaList.append(area)
        if (len(areaList) != 0):
            meanArea = sum(areaList)/len(areaList)
        else:
            meanArea = 0
        
        xcnts = []
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            x,y,w,h=cv2.boundingRect(cnt)
            if area > 1.53*meanArea or area < 0.84*meanArea :
               continue
            xcnts.append(cnt)
        print("Cell nums:{}-{}".format(len(xcnts),len(cnts)))
        cv2.drawContours(canvas,xcnts,-1,(0,211,211),1)
        
        self.ImageView.setPixmap(canvas)
        
    def addSliders(self):
        self.slider1 = QSlider(Qt.Horizontal)   #Create 3 hori sliders
        self.slider2 = QSlider(Qt.Horizontal)
        self.slider3 = QSlider(Qt.Horizontal)
        
        self.slider1.setRange(10,255)   #Set th range of hsv sliders
        self.slider2.setRange(10,254)
        self.slider3.setRange(2,255)
        
        self.slider1.setValue(50)  #set the default values of sliders
        self.slider2.setValue(200)
        self.slider3.setValue(15)
        
        self.mainLayout.addWidget(self.slider1)
        self.mainLayout.addWidget(self.slider2)
        self.mainLayout.addWidget(self.slider3)
        
        self.slider1.valueChanged.connect(self.doInrange)
        self.slider2.valueChanged.connect(self.doInrange)
        self.slider3.valueChanged.connect(self.doInrange)
        
        
        
if __name__ == "__main__":
    qApp = QApplication([])
    #img= cv2.imread("WH/11-1-4x-2-mod.jpg")
    img = cv2.imread("ZLDOX01/ing1.jpg")
    w2 = SliderHSVCounter(img)
    sys.exit(qApp.exec_())
