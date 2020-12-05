from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        # capture from web cam
        while True:
            # if ret:
            self.change_pixmap_signal.emit(self.queue.get())


class App(QWidget):
    def __init__(self,queue):
        super().__init__()
        self.queue = queue
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640*2
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width/2, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread(queue)
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()



    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


from tkinter import *
import webbrowser
class listBox:
    def deleteAll(self):
        self.listbox = Listbox(top, height = 10,  
                        width = 15,  
                        bg = "grey", 
                        activestyle = 'dotbox',  
                        font = "Helvetica", 
                        fg = "yellow") 
    def internet(self,l):
        weblink = self.listbox.get(ACTIVE).split()[1]
        print(weblink)
        webbrowser.open("https://www.google.com/search?q=define+" + weblink)
    def __init__(self,results):
        # create a root window. 
        self.top = Tk() 
        
        # create listbox object 
        self.listbox = Listbox(self.top, height = 20,  
                        width = 150,  
                        bg = "grey", 
                        activestyle = 'dotbox',  
                        font = "Helvetica", 
                        fg = "yellow") 
        
        # Define the size of the window. 
        self.top.geometry("300x250")   
        
        # Define a label for the list.   
        label = Label(self.top, text = "Found Words, double click for definition.")
        # insert elements by their 
        # index and names. 

        for i in range(len(results)):
            self.listbox.insert(i, str(results[i][1]) + " " + results[i][0])
        self.listbox.bind( "<Double-Button-1>" , self.internet )
        # pack the widgets 
        label.pack() 
        self.listbox.pack() 
        
        
        # Display untill User  
        # exits themselves. 
        self.top.mainloop() 
