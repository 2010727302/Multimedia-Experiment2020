# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np

# 定义卷积操作的函数
def convolution(image, kernel):
    height, width = image.shape
    h, w = kernel.shape

    # 经滑动卷积操作后得到的新的图像的尺寸
    new_h = height - h + 1
    new_w = width - w + 1
    new_image = np.zeros((new_h, new_w), dtype=float)

    # 进行卷积操作,实则是对应的窗口覆盖下的矩阵对应元素值相乘,卷积操作
    for i in range(new_w):
        for j in range(new_h):
            new_image[i, j] = np.sum(image[i:i+h, j:j+w] * kernel)

    # 去掉矩阵乘法后的小于0的和大于255的原值,重置为0和255
    new_image = new_image.clip(0, 255)
    new_image = np.rint(new_image).astype('uint8')
    return new_image


if __name__ == "__main__":
    # 读取图像数据并且转换为对应的numpy下的数组
    A = Image.open(r"E:\大三\{选}多媒体技术与应用\2020实验\实验4\lena_noise.bmp").convert("L")
    a = np.array(A)

    # 卷积核
    kernel_1 = np.array(([1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]))
    kernel_2 = np.array(([-1, 0, 1], [-2, 0, 2], [-1, 0, 1]))
    img1 = convolution(a, kernel_1)
    img1 = Image.fromarray(img1)
    img1.show()
    img1.save(r"E:\大三\{选}多媒体技术与应用\2020实验\实验4\convolution_img1.jpg")
    img2 = convolution(a, kernel_2)
    img2 = Image.fromarray(img2)
    img2.show()
    img2.save(r"E:\大三\{选}多媒体技术与应用\2020实验\实验4\convolution_img2.jpg")