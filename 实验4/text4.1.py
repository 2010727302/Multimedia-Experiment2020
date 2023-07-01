from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.function_base import diff
from numpy.lib.type_check import imag

def drawHistogram(image):
    pic = np.array(image)
    plt.hist(pic[:, :].ravel(), bins=256,facecolor='#328121', edgecolor='#898312')
    plt.show()

#   卷积
def convolution(image,ck):
    map = image.load()
    new = image.copy()
    newMap = new.load()
    width,height = image.size
    
    for x in range(0,height-2):
        for y in range(0,width-2):
            pixel = 0
            for i in range(0,3):
                for j in range(0,3):
                    cur = map[x+i,y+j]*ck[i][j]
                    pixel = pixel + (int)(cur)
            newMap[x+1,y+1] = pixel
    return new

# 中值滤波法 3x3
def medianFilter_3(image):
    map = image.load()
    width,height = image.size
    new = image.copy()
    newMap = new.load()

    for x in range(1,height-1):
        for y in range(1,width-1):
            list = []
            for i in range(-1,2):
                for j in range(-1,2):
                    list.append(map[x+i,y+j])
            list.sort()
            pixel = list[4]
            newMap[x,y] = pixel
    return new

# 中值滤波法 5x5
def medianFilter_5(image):
    map = image.load()
    width,height = image.size
    new = image.copy()
    newMap = new.load()

    for x in range(2,height-2):
        for y in range(2,width-2):
            list = []
            for i in range(-2,3):
                for j in range(-2,3):
                    list.append(map[x+i,y+j])
            list.sort()
            pixel = list[12]
            newMap[x,y] = pixel
    return new

# 卷积核
box = [[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]]
gauss = [[1/16,2/16,1/16],[2/16,4/16,2/16],[1/16,2/16,1/16]]

image = Image.open(r'E:\大三\{选}多媒体技术与应用\2020实验\实验4\lena_noise.bmp')
image.show()

# 去除噪声
image1 = convolution(image,box)
image1.show()
image2 = convolution(image,gauss)
image2.show()
image3 = medianFilter_3(image)
image3.show()
image4 = medianFilter_3(image)
image4.show()
