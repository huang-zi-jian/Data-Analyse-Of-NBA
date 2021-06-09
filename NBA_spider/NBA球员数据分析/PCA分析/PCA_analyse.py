'''
author: feifei
date: 2020-12-15
file info: NBA球员指标的主成分分析
'''

import pandas
from sklearn.decomposition import PCA
import csv
from sklearn.preprocessing import StandardScaler

def Pca_Analyse(filepath):
    norm_data = pandas.read_csv(filepath, index_col=0, encoding='GBK')

    # 数据标准化，
    transfer = StandardScaler()
    # 取DataFrame的前21个特征，第22个特征为location
    norm_data = transfer.fit_transform(norm_data.values[:,:21])


    # 生成PCA预估器，n_components=21是为了查看所有主成分信息
    # transfer = PCA(n_components=0.95,svd_solver='auto')
    transfer = PCA(n_components=21,svd_solver='auto')
    transfer.fit(norm_data)

    # 用PCA构造器对某一个球员的各项指标数据进行PCA降维，注意数据必须是二维的
    # data_148 = transfer.transform([[13.1,0.567,0.386,0.744,62.0,21.4]])

    # 主成分分析components_中每个特征值对应的主成分系数平方和为1
    components_matrix = transfer.components_.T
    print(components_matrix)
    # 计算每一列指标的均值
    # mean_vals = numpy.mean(norm_data,axis=0)
    # trans_data = numpy.dot(norm_data - mean_vals,components_matrix)

    # print(transfer.explained_variance_,'\n',transfer.explained_variance_ratio_)
    # print(transfer.components_[0,0])

    # 将components_矩阵用CSV文件存储起来
    with open(file='components_.csv', mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # component_这里表示降维后的主成分
        temp = ['','component_1','component_2','component_3','component_4','component_5','component_6',
                'component_7','component_8','component_9','component_10','component_11','component_12',
                'component_13','component_14','component_15','component_16','component_17','component_18',
                'component_19','component_20','component_21']
        writer.writerow(temp)

        index = 1
        # 遍历每行数据
        for component in components_matrix:
            temp = []
            # 首先将序号index加入到一组数据的开头，之后index加一指向下一组数据
            temp.append(index)
            index = index + 1
            for norm in component:
                temp.append(norm)
            # temp = []
            # temp.append(index)
            writer.writerow(temp)

    with open(file='variance.csv', mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        temp = ['component','variance_','variance_ratio_/ %','variance_cumulative/ %']
        writer.writerow(temp)

        cumulative = 0
        index = 1
        for variance_,variance_ratio_ in list(zip(transfer.explained_variance_,transfer.explained_variance_ratio_)):

            temp = []
            temp.append(index)
            temp.append(variance_)
            temp.append(variance_ratio_*100)
            cumulative = cumulative + variance_ratio_*100
            temp.append(cumulative)

            writer.writerow(temp)
            index = index + 1

if __name__ == '__main__':
    Pca_Analyse('../../stats/常规赛/2019-2020_back_wash.csv')
