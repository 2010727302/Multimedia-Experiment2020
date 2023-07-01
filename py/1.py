import numpy as np

img_EdgeKeeping = np.array([
    [3, 6, 4, 2, 1],
    [4, 7, 3, 2, 1],
    [8, 4, 1, 2, 4],
    [4, 2, 1, 4, 3],
    [4, 3, 2, 5, 3]
])

h, w = img_EdgeKeeping.shape

filter = np.zeros((5, 5))
mask = []

for i in range(h - 4):
    for j in range(w - 4):
        for m in range(5):
            for n in range(5):
                filter[m, n] = img_EdgeKeeping[i + m, j + n]

        mask = []
        mask.append([filter[1, 1], filter[1, 2], filter[1, 3], filter[2, 1], filter[2, 2], filter[2, 3], filter[3, 1], filter[3, 2], filter[3, 3]])
        mask.append([filter[2, 2], filter[1, 1], filter[1, 2], filter[1, 3], filter[0, 1], filter[0, 2], filter[0, 3]])
        mask.append([filter[2, 2], filter[1, 1], filter[2, 1], filter[3, 1], filter[1, 0], filter[2, 0], filter[3, 0]])
        mask.append([filter[2, 2], filter[3, 1], filter[3, 2], filter[3, 3], filter[4, 1], filter[4, 2], filter[4, 3]])
        mask.append([filter[2, 2], filter[1, 3], filter[2, 3], filter[3, 3], filter[1, 4], filter[2, 4], filter[3, 4]])
        mask.append([filter[2, 2], filter[3, 2], filter[2, 3], filter[3, 3], filter[4, 3], filter[3, 4], filter[4, 4]])
        mask.append([filter[2, 2], filter[2, 3], filter[1, 2], filter[1, 3], filter[1, 4], filter[0, 3], filter[0, 4]])
        mask.append([filter[2, 2], filter[1, 2], filter[2, 1], filter[1, 1], filter[0, 1], filter[1, 0], filter[0, 0]])
        mask.append([filter[2, 2], filter[2, 1], filter[3, 2], filter[3, 1], filter[3, 0], filter[4, 1], filter[4, 0]])

        var = []
        for k in range(9):
            var.append(np.var(mask[k]))
        # 输出每个mask的均值和方差，循环遍历
        for k in range(9):
            print(mask[k])
            print("掩模{}:".format(k + 1))
            print("均值:", np.mean(mask[k]))
            print("方差:", np.var(mask[k]))
            print("-" * 20)




        index = var.index(min(var))
        mean = np.mean(mask[index])

        print("坐标 ({}, {}):".format(i + 2, j + 2))
        print("掩模值:")
        for row in mask:
            print(row)
        print("-" * 20)


        img_EdgeKeeping[i+2, j+2] = mean

print("最终结果:")
print(img_EdgeKeeping)
print("像素点 (3, 3) 的值:", img_EdgeKeeping[2, 2])
