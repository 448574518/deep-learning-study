import time

import numpy as np
import h5py
import scipy
import matplotlib.pyplot as plt
import pylab
from lr_utils import load_dataset
from PIL import Image
from scipy import ndimage

# 1.先搞清楚问题的的形状
train_set_x_orig, train_set_y, test_set_x_orig, test_set_y, classes = load_dataset()

# 查看图片内容
# index = 26
# plt.imshow(train_set_x_orig[index])
# np.squeeze是压缩变量，压缩前train_set_y[:, index]是[1],压缩后是1，压缩后可以作为classes的index
# print("y=" + str(train_set_y[:, index]) + ", it is a '" + classes[np.squeeze(train_set_y[:, index])].decode("utf-8")
#      + "' picture")
# plt无法展示图片，必须要添加pylab.show()才行
# pylab.show()
m_train = train_set_x_orig[1]

# 2.把每张图片都拉长为[n*1]的向量
# 为了方便，我们要把维度为（64，64，3）的numpy数组重新构造为（64 x 64 x 3，1）的数组,下面一段意思是指把数组变为209行的矩阵
# （因为训练集里有209张图片），但是我懒得算列有多少，于是我就用-1告诉程序你帮我算
train_set_x_flatten = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1).T
test_set_x_flatten = test_set_x_orig.reshape(test_set_x_orig.shape[0], -1).T

# check the result
# print(train_set_x_flatten.shape)
# print(test_set_x_flatten.shape)

# 3.standardize，归一化，把数据都变成[0-1]，便于计算
tran_set_x = train_set_x_flatten / 255
test_set_x = test_set_x_flatten / 255


# 建立神经网络的主要步骤是：
# 1.定义模型结构（例如输入特征的数量）
# 2.初始化模型的参数
# 3.循环：
#   1 计算当前损失（正向传播）
#   2 计算当前梯度（反向传播）
#   3 更新参数（梯度下降）

# 首先定义sigmoid函数

def sigmoid(z):
    s = 1 / (1 + np.exp(-z))
    return s


# test output

# print("sigmoid(0): " + str(sigmoid(0)))
# print("sigmoid(9.2): " + str(sigmoid(9.2)))

def initialize_with_zeros(dim):
    """
    这个方法创建一个纬度为dim，值为0的向量w和初始值为0的b
    :param dim: 创建向量的纬度
    :return: 初始化后的w和b
    """
    w = np.zeros(shape=(dim, 1))
    b = 0

    # 使用断言来确保数据是正确的
    assert (w.shape == (dim, 1))  # w是dim * 1的
    assert (isinstance(b, float) or isinstance(b, int))  # b是float或者int类型

    return w, b


# 初始化测试
# dim = 3
# w, b = initialize_with_zeros(dim)
# print("w: " + str(w))
# print("b: " + str(b))

def propagate(w, b, X, Y):
    """
    实现正向和反向传播的cost function和及其梯度
    :param w:权重，大小不等的向量（px * px * 3, 1）
    :param b:偏差，一个数
    :param X:样本，矩阵为（px * px * 3, 样本数量）
    :param Y:标签矢量（0-非猫，1-猫），矩阵为（1, 样本数量）
    :return:
        cost:lr的负对数似然成本
        dw:相对于w损失的梯度，与w形状相同
        db:相对于b损失的梯度，与b形状相同
    """
    # 获取样本数量
    m = X.shape[1]

    # 正向传播
    A = sigmoid(np.dot(w.T, X) + b)
    cost = (- 1 / m) * np.sum(Y * np.log(A) + (1 - Y) * np.log(1 - A))

    # 反向传播
    dw = (1 / m) * np.dot(X, (A - Y).T)
    db = (1 / m) * np.sum(A - Y)

    # 使用断言保证数据正确
    assert (dw.shape == w.shape)
    assert (db.dtype == float)
    cost = np.squeeze(cost)
    assert (cost.shape == ())

    # 创建一个字典，保存dw，db
    grads = {"dw": dw, "db": db}

    return grads, cost


# 测试propagate
# w, b, X, Y = np.array([[1], [2]]), 2, np.array([[1, 2], [3, 4]]), np.array([[1, 0]])
# print("w.shapr: " + str(w.shape))
# print("X.shape:" + str(X.shape))
# grads, cost = propagate(w, b, X, Y)
# print("dw: " + str(grads["dw"]))
# print("db: " + str(grads["db"]))
# print("cost: " + str(cost))


def optimize(w, b, X, Y, num_iteration, learning_rate, print_cost=False):
    """
    该方法用于通过梯度下降法优化w，b
    :param w:权重，大小不等的向量（px * px * 3, 1）
    :param b:偏差，一个数
    :param X:样本，矩阵为（px * px * 3, 样本数量）
    :param Y:标签矢量（0-非猫，1-猫），矩阵为（1, 样本数量）
    :param num_iteration:学习次数
    :param learning_rate:学习率
    :param print_cost:每100步打印一次损失
    :return:
        params:包含权重w，偏差b的字典
        grads:包含cost function关于w，b的梯度的字典

    步骤说明：
        1，计算w，b的梯度和cost function的时候，使用propagate
        2，使用权重和偏差更新法更新（w = w - adw）
    """
    costs = []

    for i in range(num_iteration):
        grads, cost = propagate(w, b, X, Y)

        dw = grads["dw"]
        db = grads["db"]

        w = w - learning_rate * dw
        b = b - learning_rate * db

        # 每100次记录一次cost
        if i % 100 == 0:
            costs.append(cost)

        if print_cost and (i % 100 == 0):
            print("迭代的次数：%i, 当前的cost：%f" % (i, cost))

    params = {"w": w, "b": b}
    grads = {"dw": dw, "db": db}

    return params, grads, costs


# 测试optimize
# w, b, X, Y = np.array([[1], [2]]), 2, np.array([[1, 2], [3, 4]]), np.array([[1, 0]])
# params, gradsOut, costs = optimize(w, b, X, Y, 100, 0.009, print_cost=False)
# grads, cost = propagate(w, b, X, Y)
# print("w: " + str(params["w"]))
# print("b: " + str(params["b"]))
# print("dw: " + str(gradsOut["dw"]))
# print("db: " + str(gradsOut["db"]))


def predict(w, b, X):
    """
    使用学习过的逻辑回归，用参数w，b来预测结果
    :param w:权重，大小不等的向量（px * px * 3, 1）
    :param b:偏差，一个数
    :param X:样本，矩阵为（px * px * 3, 样本数量）
    :return:
        Y_predict:一个关于X中所有图片的预测(0,1)的numpy数组
    """
    m = X.shape[1]  # 图片数量
    Y_predict = np.zeros((1, m))
    w = w.reshape(X.shape[0], 1)

    # 预测概率
    A = sigmoid(np.dot(w.T, X) + b)
    for i in range(A.shape[1]):
        # 预测大于0.5是猫，小于0.5则非猫
        Y_predict[0, i] = 1 if A[0, i] > 0.5 else 0

    assert (Y_predict.shape == (1, m))
    return Y_predict


def model(X_train, Y_train, X_test , Y_test, num_iteration, learning_rate, print_cost=False):
    """
    逻辑回归整体模型函数
    :param X_train: 训练集，（px * px * 3, m_train）纬度的numpy数组
    :param Y_train: 训练标签集，（1, m_train）纬度的numpy数组
    :param X_test: 测试集，（px * px * 3, m_test）纬度的numpy数组
    :param Y_test:测试标签集，（1, m_test）纬度的numpy数组
    :param num_iteration: 迭代循环次数
    :param learning_rate: 学习率
    :param print_cost: 是否打印cost
    :return:
        d: 模型相关的参数
    """
    # 初始化
    w, b = initialize_with_zeros(X_train.shape[0])

    # 获取训练参数
    parameters, grads, costs = optimize(w, b, X_train, Y_train, num_iteration, learning_rate, print_cost)

    # 用训练结果进行预测
    w, b = parameters["w"], parameters["b"]
    Y_predict_train = predict(w, b, X_train)
    Y_predict_test = predict(w, b, X_test)

    print("训练集准确性：" + format(100 - np.mean(np.abs(Y_predict_train - Y_train)) * 100) + "%")
    print("测试集准确性：" + format(100 - np.mean(np.abs(Y_predict_test - Y_test)) * 100) + "%")

    d = {"w": w,
         "b": b,
         "Y_predict_train": Y_predict_train,
         "Y_predict_test": Y_predict_test,
         "learning_rate": learning_rate,
         "num_iteration": num_iteration,
         "costs": costs
         }
    return d


# 测试一下模型的效果
# d = model(tran_set_x, train_set_y, test_set_x, test_set_y, num_iteration=2000, learning_rate=0.005, print_cost=False)
# costs = np.squeeze(d["costs"])
# plt.plot(costs)
# plt.xlabel("num_iteration(per hundreds)")
# plt.ylabel("cost")
# plt.title("learning_rate: " + str(d["learning_rate"]))
# plt.show()

# 查看预测和实际的差异
# Y_predict_test = d["Y_predict_test"]
# dif = []
# Y_predict_test = Y_predict_test.reshape((1, Y_predict_test.shape[1]))
# for i in range(Y_predict_test.shape[1]):
#     if int(Y_predict_test[0, i]) != int(test_set_y[0, i]):
#         dif.append(i)
#
# for i in range(len(dif)):
#     index = int(dif[i])
#     plt.imshow(test_set_x_orig[index])
#     print("第" + str(index) + "张图片，预测结果为：" + classes[int(Y_predict_test[:, index])].decode("utf-8") +
#           ",实际结果为：" + classes[np.squeeze(test_set_y[:, index])].decode("utf-8"))
#     pylab.show()


# 可以观察一下不同的学习率下，逻辑回归的表现，如果学习率太大，可能会错过最优解，如果太小，有可能会需要迭代太多次才能得到好的效果
learning_rates = [0.01, 0.001, 0.0001]
models = {}
for i in learning_rates:
    print("当前学习率：" + str(i))
    models[str(i)] = model(tran_set_x, train_set_y, test_set_x, test_set_y,
                           num_iteration=2000, learning_rate=i, print_cost=False)
    print('\n' + "--------------------------------------------------------------------------" + '\n')

for i in learning_rates:
    # plt.plot(x, y, )
    plt.plot(np.squeeze(models[str(i)]["costs"]), label=str(models[str(i)]["learning_rate"]))

plt.xlabel("num_iteration")
plt.ylabel("cost")

legend = plt.legend(loc='upper center', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.show()
