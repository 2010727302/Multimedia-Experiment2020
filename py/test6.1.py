from PIL import Image
import numpy as np
from collections import deque 
from numpy.lib.function_base import diff
from numpy.lib.type_check import imag

# 图像分割-预处理
def imageSegmentation_FixedThreshold(image):
    map = image.load()
    new = image.copy()
    newMap = new.load()
    width,height = image.size
    
    for y in range(0,height):
        for x in range(0,width):
            if(map[x,y] < 50):
                newMap[x,y] = 0
            else:
                newMap[x,y] = 255
    return new

        
# 宽度优先搜索
def bfs_research(grid) -> int:
    ans = 0
    for i, l in enumerate(grid):
        for j, n in enumerate(l):
            cur = 0
            q = deque([(i, j)])
            while q:
                cur_i, cur_j = q.popleft()
                if cur_i < 0 or cur_j < 0 or cur_i == len(grid) or cur_j == len(grid[0]) or grid[cur_i][cur_j] != 1:
                    continue
                cur += 1
                grid[cur_i][cur_j] = 0
                for di, dj in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                    next_i, next_j = cur_i + di, cur_j + dj
                    q.append((next_i, next_j))
            ans = max(ans, cur)
    return ans

# 改变
def bfs_change(arr,max,grid):
    for i, l in enumerate(grid):
        for j, n in enumerate(l):
            cur = 0
            q = deque([(i, j)])
            store = deque()
            while q:
                cur_i, cur_j = q.popleft()
                if cur_i < 0 or cur_j < 0 or cur_i == len(grid) or cur_j == len(grid[0]) or grid[cur_i][cur_j] != 1:
                    continue
                cur += 1
                store.append([cur_i,cur_j])
                grid[cur_i][cur_j] = 0
                for di, dj in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                    next_i, next_j = cur_i + di, cur_j + dj
                    q.append((next_i, next_j))
            if(len(store) < max):
                for k in range(len(store)):
                    x = store[k][0]
                    y = store[k][1]
                    arr[x][y] = 0
    return arr

# 根据数组生成图像
def generate(image,arr):
    map = image.load()
    width,height = image.size
    
    for y in range(0,height):
        for x in range(0,width):
            if(arr[y][x] == 1):
                # 保持不变
                pass
            else:
                # 变成黑色,进行提取
                map[x,y] = 0
    return image

ori = Image.open(r'播音员（gray）.jpg')
ori.show()
new = imageSegmentation_FixedThreshold(ori)
new.show()

width,height = new.size
arr = np.array(new)
temp = new.copy()
arr_temp1 = np.array(temp)
arr_temp2 = np.array(temp)

for i in range(len(arr)):
    for j in range(len(arr[i])):
        if(arr[i][j] == 255):
            arr[i][j] = 1

for i in range(len(arr_temp1)):
    for j in range(len(arr_temp1[i])):
        if(arr_temp1[i][j] == 255):
            arr_temp1[i][j] = 1

for i in range(len(arr_temp2)):
    for j in range(len(arr_temp2[i])):
        if(arr_temp2[i][j] == 255):
            arr_temp2[i][j] = 1

# 得到最大的白色区域的面积
maxArea = bfs_research(arr_temp1)

# 开始改变
arr = bfs_change(arr,maxArea,arr_temp2)

# # 这个时候得到的arr是改变后的数组,用这个数组对原始图象进行操作
final = generate(ori,arr)
final.show()