'''
author: feifei
date: 2020-12-16
file info: 初步计算NBA球员的能力数值，将可选择球员范围缩小
'''
import pandas
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def First_Filter(filepath):
    norm_data_loc_else = pandas.read_csv(filepath, index_col=0, encoding='GBK')
    # 将球员的名字顺序存放在列表中
    player_name_list = norm_data_loc_else.index
    # 提取除location以外的所有指标数据，不过返回的数据是numpy.ndarray数组
    norm_data = norm_data_loc_else.values[:,:-1]
    # 数据标准化
    transfer = StandardScaler()
    standar_trans_norm_data = transfer.fit_transform(norm_data)

    # PCA降维
    transfer = PCA(n_components=0.95,svd_solver='auto')
    transfer.fit(standar_trans_norm_data)
    trans_norm_data = transfer.transform(standar_trans_norm_data)

    # 将主成分前面的系数用coefficients列表存储
    total_variance = sum(transfer.explained_variance_ratio_)
    coefficients = []
    for i in range(0,len(transfer.explained_variance_)):
        coefficients.append(transfer.explained_variance_ratio_[i]/total_variance)

    # 创建一个pred_list列表用于存储预测后的球员能力值
    pred_list = []
    for trans_norm in trans_norm_data:
        pred = 0
        # 分别获取主成分指标和对应系数
        for norm, coef in list(zip(trans_norm,coefficients)):
            # pred = pred + abs(norm)
            pred = pred + coef*norm

        pred_list.append(pred)

    # 向原数据中插入score得分列
    norm_data_loc_else.insert(loc=22,column='Score',value=pred_list)
    norm_data_loc_else.sort_values(by='Score',ascending=False,inplace=True)
    # rank = pandas.DataFrame([player_name_list,pred_list],index=['name','score']).T.sort_values(by='score',ascending=False,ignore_index=True)

    # head获取DataFrame结构数据的前n行数据
    # rank = rank.head(n=30)
    # print(rank)

    # DataFrame结构的数据调用insert方法可以指定插入的列位置
    norm_data_loc_else.insert(loc=23,column='Rank',value=range(1,len(norm_data_loc_else)+1))

    # index=False表示将DataFrame结构数据写入CSV文件不需要将index也写入文件
    # 编码设置为GBK为了中文系统的Excel打开不出现乱码
    norm_data_loc_else.to_csv('rank_.csv',encoding='GBK')
    print(norm_data_loc_else)


if __name__ == '__main__':
    First_Filter('../../../stats/常规赛/2019-2020_back_wash.csv')