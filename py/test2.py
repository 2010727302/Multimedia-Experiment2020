

import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import math


# 线性灰度变换，图像反转
def linearReverse(gray_image):
    # 获取输入灰度图像的像素映射和大小
    gray_pixel_map = gray_image.load()
    width, height = gray_image.size
    mode = gray_image.mode

    # 创建一个新图像，用于存储变换后的像素值
    image = Image.new(mode, (width, height))
    new_pixel_map = image.load()

    # 对每个像素进行线性变换和反转
    for x in range(width):
        for y in range(height):
            gray_pixel = gray_pixel_map[x, y]
            # 线性变换：将像素值减去最大值，然后取反
            new_pixel_map[x, y] = int(255 - (gray_pixel))

    # 返回变换后的图像
    return image

# 非线性灰度变换 对数变换
def logTrans(original_image):
    # 加载像素图
    original_pixel_map = original_image.load()
    # 获取图像宽高
    width, height = original_image.size
    # 获取图像模式
    mode = original_image.mode
    # 创建一个与原始图像大小和模式相同的新图像
    new_image = Image.new(mode, (width, height))
    # 获取新图像的像素图
    new_pixel_map = new_image.load()
    # 找到像素值的最大值
    max_value = -1
    for x in range(width):
        for y in range(height):
            if (original_pixel_map[x, y] > max_value):
                max_value = original_pixel_map[x, y]

    # 对每个像素进行对数变换
    for x in range(width):
        for y in range(height):
            # 获取原始图像上(x, y)坐标处的像素值
            original_pixel = original_pixel_map[x, y]
            # 计算变换后的像素值
            c = 255 / math.log(1 + max_value)
            transformed_pixel = (int)(c * math.log(original_pixel + 1))
            # 将变换后的像素值赋值给新图像
            new_pixel_map[x, y] = transformed_pixel

    return new_image


# 非线性灰度变换 伽马变换
def gammaTrans(original_image):
    original_pixel_map = original_image.load()
    width, height = original_image.size
    mode = original_image.mode
    new_image = Image.new(mode, (width, height))
    new_pixel_map = new_image.load()

    for x in range(width):
        for y in range(height):
            pixel = original_pixel_map[x, y]
            # 伽马值，值越大图片越暗
            gamma = 1.2
            # 调整因子，值越小图片越暗
            c = 0.8
            new_pixel = c * pow(pixel, gamma)
            # 防止像素值超出0-255范围
            if (new_pixel > 255):
                new_pixel = 255
            new_pixel_map[x, y] = (int)(new_pixel)

    return new_image



# 直方图均衡化
def histogramEqualization(ori_image):
    ori_pixel_map = ori_image.load()
    width, height = ori_image.size
    mode = ori_image.mode
    size = height * width
    image = Image.new(mode, (width, height))
    new_pixel_map = image.load()

    ori_arr = [0] * 256

    for x in range(width):
        for y in range(height):
            ori_pixel = ori_pixel_map[x, y]
            ori_arr[ori_pixel] += 1

    # for i in range(0,255):
    #     print(str(i) + str(ori_arr[i]))

    new_arr = [0] * 256
    for i in range(0, 255):
        new_arr[i] = ori_arr[i]

    for i in range(1, 255):
        new_arr[i] += new_arr[i - 1]

    # for i in range(0,255):
    #     print(new_arr[i])

    for i in range(0, 255):
        new_arr[i] = (float)(new_arr[i] / (size))

    for i in range(0, 255):
        new_arr[i] = (int)(new_arr[i] * 255)

    # for i in range(0,255):
    #     print(new_arr[i])

    for x in range(width):
        for y in range(height):
            temp = ori_pixel_map[x, y]
            new_pixel_map[x, y] = new_arr[temp]

    return image


# 绘制灰度图的直方图
def drawHistogram(image):
    width, height = image.size
    data = []
    for x in range(width):
        for y in range(height):
            gray_pixel_map = image.load()
            gray_pixel = gray_pixel_map[x, y]
            # print(type(gray_pixel))
            pixel = gray_pixel
            data.append(pixel)

    plt.hist(data, bins=256, density=0.3, facecolor="blue", edgecolor="black", alpha=0.7, stacked=True)
    # 显示横轴标签
    plt.xlabel("section")
    # 显示纵轴标签
    plt.ylabel("frequency")
    # 显示图标题
    plt.title("Histogram of gray value distribution")
    plt.show()


# 图片的读取
image = Image.open(r'E:\大三\{选}多媒体技术与应用\2020实验\实验2-图像增强\rice.tif')
image.show()
drawHistogram(image)

# 灰度线性变换(反转)
img = linearReverse(image)
drawHistogram(img)
img.show()

# 灰度非线性变换 对数变换
img = logTrans(image)
drawHistogram(img)
img.show()

# 灰度非线性变换 幂律变换(伽马变换)
img = gammaTrans(image)
drawHistogram(img)
img.show()

# 直方图均衡功能
img = histogramEqualization(image)
img.show()
drawHistogram(img)