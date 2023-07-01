from typing import Match
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import numpy as np
import math

# 直方图规定化函数，传入的参数为源图像和目标图像的累计直方图（数组）
def HistogramMatching(image, refTotal):
    # 获取像素值
    pixel_map = image.load()
    # 获取图像的宽和高
    width, height = image.size
    # 获取图像的模式
    mode = image.mode
    # 计算图像的像素总数
    size = height * width

    #   map 源图像的直方图
    # 创建一个长度为 256 的数组，用于记录每个灰度级出现的次数
    map = [0] * 256
    for x in range(width):
        for y in range(height):
            # 获取像素值
            pixel = pixel_map[x, y]
            # 统计该灰度级出现的次数
            map[pixel] = map[pixel] + 1

    #   totalmap 原始图像的累计直方图
    # 创建一个长度为 256 的数组，用于记录每个灰度级在图像中出现的像素总数
    mapTotal = [0] * 256
    for i in range(1, 256):
        # 计算累计像素总数
        mapTotal[i] = map[i] + mapTotal[i - 1]

    #   new数组用来对应源图像的灰度值（0-255）到处理后图像的灰度值的映射关系
    # 创建一个长度为 256 的数组，用于记录每个源图像灰度级到目标图像灰度级的映射关系
    new = [0]
    index = -1

    #   对于每一个灰度值（i），找到规定直方图中对应的最接近的灰度值（j）
    for i in range(0, 256):
        ans = 1000
        for j in range(0, 256):
            # 计算源图像的累计直方图和目标图像的累计直方图之间的差距
            cur = abs(mapTotal[i] / size - refTotal[j] / size_ref)
            if (cur < ans):
                ans = cur
                index = j
        # 将映射关系添加到 new 数组中
        new.append(index)

    #   创建新图像，一一对应
    # 创建一个新图像，宽度和高度与源图像相同，模式为灰度图像
    new_image = Image.new(mode, (width, height))
    new_map = new_image.load()
    for x in range(width):
        for y in range(height):
            # 获取源图像的灰度值，根据 new 数组中的映射关系将其转换为目标图像的灰度值
            new_pixel = new[(pixel_map[x, y])]
            # 将目标图像的灰度值赋值给新图像
            new_map[x, y] = (new_pixel)

    return new_image


size_ref = 32640
refTotal = [i for i in range(256)]
for i in range(1, 256):
    # ref 参考图像累计直方图
    refTotal[i] += refTotal[i - 1]

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
image = Image.open(r'E:\大三\{选}多媒体技术与应用\2020实验\实验3\cat.JPG')

#   方便起见,调用库函数转化为灰度图
image = ImageOps.grayscale(image)
drawHistogram(image)
image.show()
new_image = HistogramMatching(image, refTotal)
drawHistogram(new_image)
new_image.show()
# # 给出图像规定化后的累计直方图
# new_image = np.array(new_image)
# new_image.show()