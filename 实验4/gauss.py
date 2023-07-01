import numpy as np

def gaussian(x, y, mean=0, std=0.8):
    g = (1 / (2 * np.pi * std ** 2)) * np.exp(-(((x - mean) ** 2 + (y - mean) ** 2) / (2 * std ** 2)))
    return g


def make_gaussian_kernel(kernel_size=3):
    print("初始化高斯模板坐标...大小为{}×{}...".format(kernel_size, kernel_size))
    # 找到行与列的关系，用于生成横纵坐标
    if kernel_size % 2 == 1:
        t = (kernel_size - 1) // 2
        # 坐标的范围
        m = np.arange(-t, t + 1)
        # 重复得到x坐标
        x = np.repeat(m, kernel_size)
        # 重复得到y坐标
        y = np.repeat(m.reshape(1, -1), kernel_size, axis=0).flatten()
        # 利用zip得到坐标数组
        point = list(zip(x, y))
        # 循环输出坐标, 调整成行和列的形式
        for i in range(kernel_size):
            print(point[i * kernel_size:i * kernel_size + kernel_size])
        return x, y
    else:
        print("请正确输入模板大小...")


def normalize_kernel(kernel):
    print("\n正在进行归一化...权重和为1...")
    kernel = kernel / np.sum(kernel)
    print(kernel)
    return kernel


def integerize_kernel(kernel):
    print("\n整形化高斯模板...")
    # 取第一个值，然后将左上角第一个值变成1，其它的值对应改变，并转换成整形
    v = kernel[0][0]
    kernel = np.int32(kernel / v)
    s = np.sum(kernel)
    print(kernel, '   1/' + str(np.sum(kernel)))
    return kernel


if __name__ == '__main__':
    # 设置高斯模板大小，模板请输入奇数
    kernel_size = 3
    # 初始化高斯模板
    x, y = make_gaussian_kernel(kernel_size=kernel_size)
    # 设置高斯函数的均值和标准差
    mean = 0
    std = 0.8
    # 得到结果
    result = gaussian(x, y, mean=mean, std=std)
    # reshape
    gaussian_kernel = np.reshape(result, (kernel_size, kernel_size))
    print("\n高斯模板如下:\n", gaussian_kernel)
    # 归一化
    normalized_kernel = normalize_kernel(gaussian_kernel)
    # 整数化
    integerized_kernel = integerize_kernel(normalized_kernel)
