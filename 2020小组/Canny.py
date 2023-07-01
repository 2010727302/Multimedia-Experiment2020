import numpy as np
import cv2
import math


def Canny(img,threshold1,threshold2):
    #step1:高斯滤波
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    new_gray=cv2.GaussianBlur(gray,(5,5),1)

    #展示高斯滤波后的图片
    # gaus_result=new_gray.copy()
    gaus_result=np.uint8(np.copy(new_gray))
    cv2.imshow('gaus',gaus_result)
    # cv2.waitKey(0)

    #step2:求梯度值及梯度方向
    H1,W1=new_gray.shape
    print(new_gray.shape)
    dx=np.zeros([H1-1,W1-1])
    dy=np.zeros([W1-1,W1-1])
    #求出的图像值
    d=np.zeros([H1-1,W1-1])
    #梯度方向
    dgree=np.zeros([H1-1,W1-1])
    for i in range(1,H1-1):
        for j in range(1,W1-1):
            #dx水平方向
            dx[i,j]=new_gray[i-1,j-1]+2*new_gray[i,j-1]+new_gray[i+1,j-1]-\
                    new_gray[i-1,j+1]-2*new_gray[i,j+1]-new_gray[i+1,j+1]
            #dy垂直方向
            dy[i,j]=new_gray[i-1,j-1]+2*new_gray[i-1,j]+new_gray[i-1,j+1]-\
                    new_gray[i+1,j-1]-2*new_gray[i+1,j]-new_gray[i+1,j+1]
            #G=sqrt(Gx**2+Gy**2)
            d[i,j]=np.sqrt(np.square(dx[i,j])+np.square(dy[i,j]))
            #math.atan2求出弧度，math.degrees转为角度
            dgree[i,j]=math.degrees(math.atan2(dy[i,j],dx[i,j]))
            if dgree[i,j]<0:
                dgree+=360

    #
    d_show=np.uint8(np.copy(d))
    cv2.imshow('d_show',d_show)

    #非极大值抑制
    H2, W2=d.shape
    NMS=np.uint8(np.copy(d))
    NMS[0,:]=NMS[W2-1,:]=NMS[:,0]=NMS[:,H2-1]=0
    for i in range(1,H2-1):
        for j in range(1,W2-1):
            if d[i,j]==0:
                NMS[i,j]=0
            else:
                g1=None
                g2=None
                #也可以使用插值方法，此处为设定角度计算
                #0度水平方向
                if (dgree[i,j]<=22.5 and dgree[i,j]>=0) or (dgree[i,j]>=337.5):
                    g1=NMS[i,j-1]
                    g2=NMS[i,j+1]
                #45度方向
                elif (dgree[i,j]<=67.5 and dgree[i,j]>22.5) or (dgree[i,j]<=337.5 and dgree[i,j]>292.5):
                    g1=NMS[i-1,j+1]
                    g2=NMS[i+1,j-1]
                #90度方向
                elif (dgree[i,j]<=112.5 and dgree[i,j]>67.5) or (dgree[i,j]<=292.5 and dgree[i,j]>247.5):
                    g1=NMS[i-1,j]
                    g2=NMS[i+1,j]
                #135度方向
                elif (dgree[i,j]<=157.5 and dgree[i,j]>112.5) or (dgree[i,j]<=247.5 and dgree[i,j]>202.5):
                    g1=NMS[i-1,j-1]
                    g2=NMS[i+1,j+1]
                #180度方向
                else:
                    g1=NMS[i,j-1]
                    g2=NMS[i,j+1]
                #如果当前值小于梯度方向上的任一值，则NMS[i,j]=0，否则保留原值
                if NMS[i,j]<g1 or NMS[i,j]<g2:
                    NMS[i,j]=0

    cv2.imshow('NMS_show',NMS)

    #双阈值算法检测，连接边缘
    H3,W3=NMS.shape
    DT=np.zeros([H3,W3])
    #定义高低阈值
    TL=min(threshold1,threshold2)
    TH=max(threshold1,threshold2)

    for i in range(1,H3-1):
        for j in range(1,W3-1):
            #小于TL的值设置为0
            if (NMS[i,j]<TL):
                DT[i,j]=0
            #大于TH的值设置为255，即边缘
            elif (NMS[i,j]>TH):
                DT[i,j]=255
            #对于在TL~TH之间的数，如果相邻点大于TH，即和边缘值有连接，则也为边缘值，设置为255
            else:
                if NMS[i-1,j]>TH or NMS[i-1,j-1]>TH or NMS[i-1,j+1]>TH or NMS[i,j-1]>TH \
                    or NMS[i,j+1]>TH or NMS[i+1,j]>TH or NMS[i+1,j-1]>TH or NMS[i+1,j+1]>TH:
                    DT[i,j]=255

    return DT

img=cv2.imread('data/lena.png')
cv2.imshow('orginal_img',img)
canny_img=Canny(img,50,140)
cv2.imshow('canny_img',canny_img)
cv2.waitKey(0)