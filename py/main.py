import matplotlib.pyplot as plt
from PIL import Image


# 真彩图转换为灰度图
def rgbTogray(image):
    OrigPixelMap = image.load()
    width, height = image.size
    mode = image.mode

    grayimage = Image.new(mode, (width, height))
    GrayPixelMap = grayimage.load()

    for x in range(width):
        for y in range(height):
            # Grab the current pixel, and the component RGB values.
            origpixel = OrigPixelMap[x, y]
            origr = origpixel[0]
            origg = origpixel[1]
            origb = origpixel[2]
            # print(origb,origr,origg)
            # Copy this data over to the corresponding pixel in the new image.
            # newr = int((origr + origb + origg) / 3)
            # newg = int(newr)
            # newb = int(newr)
            #  按照公式进行转换：y=B*0.299+G*0.587+R*0.114
            newr=int(0.299*origb+0.587*origg+0.114*origr)
            newg = int(newr)
            newb = int(newr)
            new_pixel = (newr, newg, newb)
            GrayPixelMap[x, y] = new_pixel

    return grayimage


# 灰度图转换为二值图
def grayToBin(image):
    threshold = 127
    mode = image.mode
    BinaryImage = Image.new(mode, (width, height))
    GrayPixelMap = image.load()
    BinaryPixelMap = BinaryImage.load()

    for x in range(width):
        for y in range(height):

            GrayPixel = GrayPixelMap[x, y]
            pixel = GrayPixel[0]

            if (pixel > threshold):
                new = 255
            else:
                new = 0

            new_pixel = (new, new, new)
            BinaryPixelMap[x, y] = new_pixel

    return BinaryImage


# 绘制灰度图的直方图
def grayPic(image):
    data = []
    for x in range(width):
        for y in range(height):
            GrayPixelMap = image.load()
            GrayPixel = GrayPixelMap[x, y]
            pixel = GrayPixel[0]
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
# ori_image = Image.open(r'E:\大三\{选}多媒体技术与应用\2020实验\实验1-源图像\346378.jpg')
ori_image = Image.open(r'E:\大三\{选}多媒体技术与应用\2020实验\实验1-源图像\flowers.tif')
# ori_image = Image.open(r'E:\大三\{选}多媒体技术与应用\2020实验\实验1-源图像\cat.bmp')
width, height = ori_image.size
mode = ori_image.mode

# 图片的显示
ori_image.show()

# 真彩图转换为灰度图
grayimage = rgbTogray(ori_image)
grayimage.show()

# 灰度图转换为二值图
bin_image = grayToBin(grayimage)
bin_image.show()

# 绘制灰度图象直方图
grayPic(grayimage)