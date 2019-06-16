import cv2
import numpy as np
import math
from random import randint
from enum import Enum

class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.initialize()

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)

    def get_frame(self):
        ret, self.last_frame = self.cap.read()
        return self.last_frame

    def set_brightness(self, value):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

    def get_brightness(self):
        return self.cap.get(cv2.CAP_PROP_BRIGHTNESS)

    def close_camera(self):
        self.cap.release()

    def __str__(self):
        return f'OpenCV Camera {self.cam_num}'

    def __del__(self):
        self.close_camera()
        # print(f'camera {self.cam_num} is release!')

class ImageProcess:
    def __init__(self):
        self.img = None
        self.img_binary = None
        self.img_gray = None
        self.img_sobel = None
        self.ndefects = None
        self.contours = None
        
    def get_eucledian_distance(self, a, b):
        d = (a[0]-b[0])**2 + (a[1]-b[1])**2
        return math.sqrt(d)
    
    # 邊緣檢測
    def sobel(self):
        x = cv2.Sobel(self.img, cv2.CV_16S, 1, 0)
        y = cv2.Sobel(self.img, cv2.CV_16S, 0, 1)
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        self.img_sobel = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
        return self.img_sobel

    def gray(self):
        self.img_gray = cv2.cvtColor(self.img_sobel, cv2.COLOR_BGR2GRAY)
        return self.img_gray

    def threshold(self):
        _, self.img_binary = cv2.threshold(self.img_gray, 20, 255, cv2.THRESH_BINARY)
        return self.img_binary

    # 輪廓檢測
    def find_contours(self):
        self.contours, hierarchy = cv2.findContours(
            self.img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(self.img, self.contours, -1, (0, 0, 255), 2)
        return self.contours

    # 取得輪廓的特徵
    def get_larget_cnt(self):
        areas = [cv2.contourArea(c) for c in self.contours]  # 各個contours的面積
        max_index = np.argmax(areas)  # 取得最大面積contour的編號值
        self.cnt = self.contours[max_index]
        return self.cnt

    # 缺陷
    ## 根據圖像中凹凸點中的 (開始點, 結束點, 遠點)的坐
    ## 利用餘弦定理計算兩根手指之間的夾角 其必為銳角 根據銳角的個數判別手勢
    def convex_hull(self):
        hull = cv2.convexHull(self.cnt, returnPoints=False)
        defects = cv2.convexityDefects(self.cnt, hull)
        self.ndefects = 0
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(self.cnt[s][0])
            end = tuple(self.cnt[e][0])
            far = tuple(self.cnt[f][0])
            a = self.get_eucledian_distance(start, end)
            b = self.get_eucledian_distance(start, far)
            c = self.get_eucledian_distance(end, far)
            angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

            if angle < math.pi/4:
                self.ndefects += + 1
            cv2.line(self.img, start, end, [255, 255, 0], 2)
            cv2.circle(self.img, far, 5, [255, 0, 255], -1)
        print(self.ndefects)
        return self.ndefects

class Mora:
    def __init__(self):
        self.MORA = ['石頭', '剪刀', '布']
        self.pc = None
        self.player = None
        
    def pc_random(self):
        self.pc = self.MORA[randint(0, len(self.MORA)-1)]

    def check(self, ndefects):
        if ndefects <= 1:
            self.player = self.MORA[0]
        elif ndefects >= 2 and ndefects <=3:
            self.player = self.MORA[1]
        elif ndefects > 3: 
            self.player = self.MORA[2]
    
    def compare(self):
        you_win = '你贏惹'
        you_lose = '你輸惹'
        if (self.player == self.MORA[0] and self.pc == self.MORA[1]) or \
            (self.player == self.MORA[1] and self.pc == self.MORA[2]) or \
            (self.player == self.MORA[2] and self.pc == self.MORA[0]):
            return you_win
        elif (self.pc == self.MORA[0] and self.player == self.MORA[1]) or \
            (self.pc == self.MORA[1] and self.player == self.MORA[2]) or \
            (self.pc == self.MORA[2] and self.player == self.MORA[0]):
            return you_lose
        else:
            return '平手'

if __name__ == "__main__":
    print('ok')