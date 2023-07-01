# ex4_2.py：图像分割
# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
from math import pow


# 通过阈值进行图片分割
def segmentation(img, threshold):
    image_pixel = np.array(img)
    # 按照阈值二值化图像
    for x in range(img.height):
        for y in range(img.width):
            image_pixel[x][y] = (255 if image_pixel[x][y]
                                 > threshold else 0)

    # 保存图片
    segmentation_image = Image.fromarray(image_pixel).convert('1')
    segmentation_image.save("leave2.jpg")
    segmentation_image.show()
    return True


# OTSU阈值分割
def otsuSegmentation(image_url):
    img = Image.open(image_url).convert('L')
    threshold = 127

    # 获取图片像素总数量and分布直方图数据
    total_pixel_num = img.height * img.width
    histogram = img.histogram()

    # 计算图片总平均灰度值
    total_gray = 0
    for i in range(len(histogram)):
        total_gray += i * histogram[i]
    total_average_gray = total_gray / total_pixel_num

    list = [0] * len(histogram)
    for k in range(1, len(histogram) - 2):
        # 获取C1类像素概率和平均像素值
        c1_hist = histogram[:k]
        c1_total_gray = 0
        for i in range(len(c1_hist)):
            c1_total_gray += i * c1_hist[i]

        # C1像素数目
        c1_pixel_num = sum(c1_hist)
        # C1像素概率
        c1_rate = c1_pixel_num / total_pixel_num
        if c1_pixel_num == 0:
            c1_pixel_num = 1
        # C1平均灰度
        c1_average_gray = c1_total_gray / c1_pixel_num

        # 获取C2类像素概率和平均像素值
        c2_hist = histogram[k:len(histogram)]
        c2_total_gray = 0
        for i in range(len(c2_hist)):
            c2_total_gray += i * c2_hist[i]

        # C1像素数目
        c2_pixel_num = sum(c2_hist)
        # C1像素概率
        c2_rate = c2_pixel_num / total_pixel_num
        if c2_pixel_num == 0:
            c2_pixel_num = 1
        # C1平均灰度
        c2_average_gray = c2_total_gray / c2_pixel_num

        # 求co和cl的类间方差
        list[k] = c1_rate * pow(total_average_gray - c1_average_gray, 2) + \
            c2_rate * pow(total_average_gray - c2_average_gray, 2)

    # 获取最大的类方差值
    threshold = int(list.index(max(list)))
    segmentation(img, threshold)
    return True


if __name__ == "__main__":
    otsuSegmentation("img1.jpg")

