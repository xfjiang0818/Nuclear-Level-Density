import numpy as np

# --------------------------------------------------------------
# 使用内部功能函数
# --------------------------------------------------------------
# 1D
array = np.arange(20)
print(array)
# 数组元素可变，因此可以进行赋值
# 但是，数组元素是同质的，因此不能将一个字符串赋值到数组中

# 2D
array = np.arange(20).reshape(4,5)
print(array)

# 3D
array = np.arange(27).reshape(3,3,3)
print(array)

# others
# zeros 函数
array = np.zeros((2, 4))
print(array)
# ones 函数
array = np.ones((2, 4))
print(array)
# empty 函数
# 返回指定大小的数组，元素随机，取决于内存状态
array = np.empty((2, 4))
print(array)
# full 函数
array = np.full((2, 4), "n")
print(array)
# eye 函数
# 返回对角元为 1，非对角元为 0 的矩阵
array = np.eye(4, 4)
print(array)
# linspace 函数
# 在指定间隔内返回均匀分布的数字，这个间隔左右两端都是闭合的
array = np.linspace(0, 10, num = 4)
print(array)



# --------------------------------------------------------------
# 从 Python 列表转换
# --------------------------------------------------------------
array = np.array([4,5,6])
print(array)

pylist = [1, 3, 4]
array = np.array(pylist)
print(array)

# array 是否可以转化为 python 列表？可以~！
array = np.array([1, 2, 3, 6, 8])
alist = list(array)
print(alist)



# --------------------------------------------------------------
# 使用特殊的库函数
# --------------------------------------------------------------
array = np.random.random((2,2))
print(array)