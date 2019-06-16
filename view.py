import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread
from PyQt5 import QtCore

from mainWindow import Ui_Form
from models import ImageProcess, Mora

class StartWindow(QMainWindow, Ui_Form):
    def __init__(self, camera):
        super(StartWindow, self).__init__()
        self.setupUi(self)
        self.init_ui()
        # 相機
        self.camera = camera
        self.movie_thread = MovieThread(self.refreshShow)
        self.process_thread = MovieThread(self.process)
        self.image_process = ImageProcess()
        

    def init_ui(self):
        # 信號與槽連接, PyQt5 與 Qt5相同, 信號可綁定普通成員函數
        self.btn_open.clicked.connect(self.openSlot)
        self.btn_save.clicked.connect(self.saveSlot)
        self.btn_play.clicked.connect(self.play)
        self.btn_quit.clicked.connect(self.close)
        # self.btn_soble.clicked.connect(self.on_soble_click)
        # self.btn_binary.clicked.connect(self.on_binary_click)
        # self.btn_gray.clicked.connect(self.on_gray_click)
        # self.btn_find_contours.clicked.connect(self.on_find_contours)

    def openSlot(self):
        self.movie_thread.start()
        self.btn_quit.setEnabled(True)
        self.btn_save.setEnabled(True)
        self.btn_play.setEnabled(True)
        # self.btn_gray.setEnabled(True)
        # self.btn_binary.setEnabled(True)
        # self.btn_soble.setEnabled(True)
        # self.btn_find_contours.setEnabled(True)
        self.process_thread.start()

    def saveSlot(self):
        # 儲存文件 dialog
        fileName, tmp = QFileDialog.getSaveFileName(
            self, 'Save Image', './_img', '*.png *.jpg *.bmp', '*.png')
        if fileName is '':
            return
        if self.img.size == 1:
            return

        # 用 opencv 寫入圖像
        cv2.imwrite(fileName, self.img)

    def processSlot(self):
        self.movie_thread.stop()

    def refreshShow(self):
        # 提取圖像的尺寸和通道, 用於將 opencv下的 image 轉換成 Qimage
        frame = self.camera.get_frame()
        self.img = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()

        # 將 Qimage 顯示出來
        q_pixmap = QPixmap.fromImage(self.qImg)
        resize_w = self.label_1.width()
        resize_h = self.label_1.height()
        q_pixmap = q_pixmap.scaled(resize_w, resize_h)
        self.label_1.setPixmap(q_pixmap)

    def process(self):
        frame = self.camera.get_frame()

        self.img = frame #cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.image_process.img = self.img.copy()
        self.image_process.sobel()
        self.image_process.gray()
        self.image_process.threshold()
        self.image_process.find_contours()
        try:
            self.image_process.get_larget_cnt()
            self.image_process.convex_hull()
            x, y, w, h = cv2.boundingRect(self.image_process.cnt)  # 該最大 contour 的(x,y)位置及長寬
            cv2.rectangle(self.image_process.img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # mora = Mora()
            # mora.check(self.image_process.ndefects)
            # self.player_plain_text.setPlainText(mora.player)
        except Exception as e:
            print(e)
            pass
        height, width, channel = self.image_process.img.shape
        bytesPerLine = 3 * width

        self.qImg = QImage(self.image_process.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()
                           
        q_pixmap = QPixmap.fromImage(self.qImg)
        resize_w = self.label_2.width()
        resize_h = self.label_2.height()
        q_pixmap = q_pixmap.scaled(resize_w, resize_h)
        # q_pixmap = q_pixmap.scaled(resize, resize, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(q_pixmap)

    def play(self):
        mora = Mora()
        mora.check(self.image_process.ndefects)
        mora.pc_random()
        self.player_plain_text.setPlainText(mora.player)
        self.pc_plain_text.setPlainText(mora.pc)
        self.result_plain_text.setPlainText(mora.compare())

    def on_soble_click(self):
        pass

    def on_gray_click(self):
        pass
    
    def on_binary_click(self):
        pass

    def on_find_contours(self):
        pass

class MovieThread(QThread):
    def __init__(self, job):
        super().__init__()
        self.stop_flas = False
        self.job = job

    def stop(self):
        self.stop_flas = True

    def run(self):
        self.stop_flas = False
        while not self.stop_flas:
            self.job()

