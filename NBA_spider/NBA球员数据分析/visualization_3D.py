'''
author: feifei
date: 2020-12-17
file info: 将数据降至3维然后进行可视化观察降维后的数据分布
'''

import shelve
import pandas
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from matplotlib import pyplot


# 从文件中读取爬虫数据对象
# file = shelve.open('../files/player.dat')
# dic_Player = file['dic_Player']
# file.close()

norm_data = pandas.read_csv('../stats/常规赛/2018-2019_wash.csv',index_col=0,encoding='GBK')

transfer = PCA(n_components=3,svd_solver='auto')
transfer.fit(norm_data)

total_variance = sum(transfer.explained_variance_ratio_[0:3])

# 将主成分前面的系数用coefficients列表存储
coefficients = []
for i in range(0,3):
    coefficients.append(transfer.explained_variance_ratio_[i]/total_variance)

# 将球员的名字顺序存放在列表中
player_name_list = []


# 将原始特征数据转换为降维后的主成分数据并用trans_norm_list列表存储
trans_norm_data = transfer.transform(norm_data)
ax = Axes3D(pyplot.figure())
ax.scatter(trans_norm_data[:,0], trans_norm_data[:,1], trans_norm_data[:,2])
# 为3维视图设置坐标名称
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

pyplot.show()