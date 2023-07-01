from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy.lib.function_base import diff
from numpy.lib.type_check import imag
# 真彩图转换为灰度图
def rgbTogray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def drawHistogram(image):
    pic = np.array(image)
    plt.hist(pic[:, :].ravel(), bins=256,facecolor='#black', edgecolor='#898312')
    plt.show()

#   卷积
def convolution(image,ck):
    map = image.load()
    new = image.copy()
    newMap = new.load()
    width,height = image.size

    for y in range(0,height-2):
        for x in range(0,width-2):
            pixel = 0
            for i in range(0,3):
                for j in range(0,3):
                    cur = map[x+i,y+j]*ck[i][j]
                    pixel = pixel + (int)(cur)
            newMap[x+1,y+1] = pixel
    return new

# 卷积核
PrewittX = [[-1,-1,-1],[0,0,0],[1,1,1]]
PrewittY = [[-1,0,1],[-1,0,1],[-1,0,1]]
SobelX = [[-1,-2,-1],[0,0,0],[1,2,1]]
SobelY = [[-1,0,1],[-2,0,2],[-1,0,1]]
Laplacain1 = [[0,1,0],[1,-4,1],[0,1,0]]
Laplacain2 = [[0,-1,0],[-1,4,-1],[0,-1,0]]
Laplacain3 = [[1,1,1],[1,-8,1],[1,1,1]]
Laplacain4 = [[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]

# image = Image.open(r'播音员（gray）.jpg')
image = Image.open(r'img1.jpg')
# image.show()
# Convert the image to grayscale
gray_image = image.convert('L')

# Display the grayscale image
# gray_image.show()

image = convolution(gray_image,Laplacain4)
# image.show()
# Assuming `image` is the grayscale image obtained after convolution
# inverted_image = Image.eval(image, lambda x: 255 - x)
inverted_image = ImageOps.invert(image)
# Display the inverted image
inverted_image.show()