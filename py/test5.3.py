
# 分水岭
# -*- coding: utf-8 -*-
from PIL import Image
import matplotlib.pyplot as plt  # plt 用于显示图片
import numpy as np
import cv2

def  watershed(img):
    #转化成灰度图，方便处理
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #二值化
    ret,thresh=cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    #去除噪音(要不然最终成像会导致过度分割)
    kernel=np.ones((3,3),np.uint8)
    opening=cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=2)

    #确定非对象区域
    sure_bg=cv2.dilate(opening,kernel,iterations=3)#进行膨胀操作

    #确定对象区域
    dist_transform=cv2.distanceTransform(opening,1,5)
    ret,sure_fg=cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

    #寻找未知的区域
    sure_fg=np.uint8(sure_fg)
    unknown=cv2.subtract(sure_bg,sure_fg)#非对象区域减去对象区域就是不确定区域

    # 为对象区域类别标记
    ret, markers = cv2.connectedComponents(sure_fg)
    # 为所有的标记加1，保证非对象是0而不是1
    markers = markers+1
    # 现在让所有的未知区域为0
    markers[unknown==255] = 0

    #执行 watershed
    markers = cv2.watershed(img,markers)
    img[markers == -1] = [255,0,0]

    #解决中文显示问题
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.subplot(231), plt.imshow(gray, 'gray'), plt.title('输入图片'),plt.axis('off')
    plt.subplot(232), plt.imshow(opening,'gray'), plt.title('二值化去噪之后'),plt.axis('off')
    plt.subplot(233), plt.imshow(sure_bg,'gray'), plt.title('确定非对象区域'),plt.axis('off')
    plt.subplot(234), plt.imshow(dist_transform,'gray'), plt.title('确定对象区域'),plt.axis('off')
    plt.subplot(235), plt.imshow(unknown,'gray'), plt.title('未知区域'),plt.axis('off')
    plt.subplot(236), plt.imshow(img,'gray'), plt.title(' watershed'),plt.axis('off')

    plt.show()
# watershed
img3 = cv2.imread("coin.jpg")#读图
result3 =  watershed(img3)




