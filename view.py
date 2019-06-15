import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread

from mainWindow import Ui_Form

class StartWindow(QMainWindow, Ui_Form):
    def __init__(self, camera):
        super(StartWindow, self).__init__()
        self.setupUi(self)
        self.init_ui()
        
        # 相機
        self.camera = camera
        # 初始化一個 img 的 ndarray，用於存儲圖像
        self.img = np.ndarray(())
        self.movie_thread = MovieThread(self)

    def init_ui(self):
        # self.resize(1080, 720)
        # 信號與槽連接, PyQt5 與 Qt5相同, 信號可綁定普通成員函數
        self.btn_open.clicked.connect(self.openSlot)
        self.btn_save.clicked.connect(self.saveSlot)
        self.btn_stop.clicked.connect(self.processSlot)
        self.btn_quit.clicked.connect(self.close)

    def openSlot(self):
        self.movie_thread.start()

    def saveSlot(self):
        # 儲存文件 dialog
        fileName, tmp = QFileDialog.getSaveFileName(
            self, 'Save Image', '_img', '*.png *.jpg *.bmp', '*.png')

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
        q_pixmap = q_pixmap.scaledToHeight(self.label_1.height())
        q_pixmap = q_pixmap.scaledToWidth(self.label_1.width())
        self.label_1.setPixmap(q_pixmap)
        # self.label_2.setPixmap(q_pixmap)

class MovieThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.stop_flas = False
        self.camera = camera

    def stop(self):
        self.stop_flas = True

    def run(self):
        self.stop_flas = False
        while not self.stop_flas:
            self.camera.refreshShow()