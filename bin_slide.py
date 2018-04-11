# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 15:45:39 2018

@author: Cheng
"""
# -*- coding: utf-8 -*-
"""
Spyder Editor

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

class ImageView(QWidget):
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

class SliderCanny(QWidget):
    '''slide bar  '''
    def __init__(self,img = None):
        super().__init__()
        if img is None:
            raise Exception("Image is Null")
            pass
        self.img = img
        self.gray = cv2.GaussianBlur(cv2.cvtColor(self.img,cv2.COLOR_RGB2GRAY),(3,3),0) #gray& gauss
        self.setWindowTitle("Th")
        self.ImageView = ImageView("Source")
        self.CannyView = ImageView("Canny")
        self.ImageView.setPixmap(self.img)
        self.CannyView.setPixmap(self.img)
        
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.addSliders()
        self.show()
        
    def doCanny(self):
        th1 = self.slider1.value()
        th2 = self.slider2.value()
        #print(th1,th2)
        self.setWindowTitle("TH:{}~{}".format(th1,th2))
        _,threshed = cv2.threshold(self.gray, th1,th2,cv2.THRESH_BINARY_INV)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        morphed = cv2.morphologyEx(threshed, cv2.MORPH_OPEN,kernel,None,(-1,-1),1)
        
        _, cnts, _ = cv2.findContours(morphed,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        canvas = img.copy()
        #cv2.drawContours(canvas,cnts,-1,(0,211,211),1)
        
        #meanArea = 
        areaList = []
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            areaList.append(area)
        meanArea = sum(areaList)/len(areaList)
        
        xcnts = []
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            x,y,w,h=cv2.boundingRect(cnt)
            if area > meanArea :
               continue
            xcnts.append(cnt)
        print("Cell nums:{}".format(len(xcnts)))
        cv2.drawContours(canvas,xcnts,-1,(0,211,211),1)
        #cv2.drawContours(canvas,xcnts,-1,(49,120,120),1)
        #cannyed = cv2.Canny(self.gray,th1,th2)
        
        #mask = cannyed > 0
        #canvas = np.zeros_like(self.img)
        #canvas[mask] = img[mask]
        
        self.CannyView.setPixmap(canvas)
        
    def addSliders(self):
        self.slider1 = QSlider(Qt.Horizontal)
        self.slider2 = QSlider(Qt.Horizontal)
        
        self.slider1.setRange(10,250)
        self.slider2.setRange(10,250)
        self.slider1.setValue(50)
        self.slider2.setValue(200)
        
        self.mainLayout.addWidget(self.slider1)
        self.mainLayout.addWidget(self.slider2)
        
        self.slider1.valueChanged.connect(self.doCanny)
        self.slider2.valueChanged.connect(self.doCanny)
        
        
            

        
if __name__ == "__main__":
    qApp = QApplication([])
    
    #img= cv2.imread("WH/43-1-4x-mod.jpg")
    img = cv2.imread("ZLDOX01/ing1.jpg")
    #img1 = cv2.resize(img,(326,490))
    w2 = SliderCanny(img)
    sys.exit(qApp.exec_())

