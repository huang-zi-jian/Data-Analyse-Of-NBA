'''
author: feifei
date: 2020-12-19
file info: 对数据进行逻辑回归并取出对应的概率值
'''

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import pandas
import numpy


def LogisticRegress(location):
    second_filter = pandas.read_csv('../rank_add_k-means.csv', index_col=0, encoding='GBK')
    second_filter_values = second_filter.values[:,:-4]

    # 标准化
    Stand_transfer = StandardScaler()
    second_filter_values = Stand_transfer.fit_transform(second_filter_values)

    # 降维
    Pca_transfer = PCA(n_components=0.95,svd_solver='auto')
    second_filter_values = Pca_transfer.fit_transform(second_filter_values)

    # lables用于逻辑回归
    lables = second_filter['k-means-lable']
    score = second_filter['Score']
    avg_value = second_filter[['Score','k-means-lable']].groupby(['k-means-lable']).apply(lambda x:numpy.mean(x))
    avg_value.set_index(avg_value['k-means-lable'],inplace=True)
    # avg_lable0 = avg_value.loc[0,'Score']
    # avg_lable1 = avg_value.loc[1,'Score']

    # 构造逻辑回归拟合器
    estimator = LogisticRegression()
    estimator.fit(second_filter_values,lables)

    # proba = estimator.predict_proba(second_filter_values)[:,0]
    # 获取逻辑回归预测概率值
    proba = estimator.predict_proba(second_filter_values)
    # 获取逻辑回归概率和对应标签均值的和作为第二轮评分
    proba_score = numpy.dot(proba,avg_value)[:,0]
    # 分别求出两轮评分的极差
    score_length = score.max() - score.min()
    proba_score_length = max(proba_score) - min(proba_score)
    # 按照各极差占比加权结果作为这两轮的综合评分
    Score = proba_score*score_length/(score_length + proba_score_length) + \
            score*proba_score_length/(score_length + proba_score_length)
    # Score = score + proba_score

    '''
    # 将第一轮评分转化到第二轮评分的量纲上
    Scaler_transfer = MinMaxScaler(feature_range=(min(proba_score), max(proba_score)))
    Scaler_score = Scaler_transfer.fit_transform(pandas.DataFrame(score))
    
    舍弃：分析结果不好
    '''

    '''
    # 将一轮筛选的分数乘上逻辑回归的概率再和原分数加和取平均值，之后将该平均值归一化
    # proba_score = numpy.multiply(proba,score)
    # Score = (score + proba_score)/2
    
    舍弃：误差很大
    '''

    # 先将Series结构转化为DataFrame结构数据，方便之后的归一化处理
    Score = pandas.DataFrame(Score)

    # Score调整到（0.5,1）归一化处理
    Scaler_transfer = MinMaxScaler(feature_range=(0.5,1))
    Score = Scaler_transfer.fit_transform(Score)

    print(numpy.mean(Score))
    # Score = Score**2 - numpy.mean(Score)**2
    scores = []
    # 评估得分大于平均值的加上(xi - 均值)的平方加分项，评估得分低于平均值减去该平方项
    for score in Score:
        # score为ndarray类型数据，取score[0]
        if score[0] > numpy.mean(Score):
            score = score[0] + (score[0] - numpy.mean(Score))**2
            scores.append(score)

        else:
            score = score[0] - (score[0] - numpy.mean(Score))**2
            scores.append(score)

    # 将score新数据覆盖原文件的Score列数据
    second_filter['Score'] = scores
    second_filter.sort_values(by='Score',ascending=False,inplace=True)
    # 重新排序后Rank列也要重置
    second_filter['Rank'] = range(1,len(second_filter)+1)
    '''
    ['Rank','Score','location'...]获取多行DataFrame结构数据，最后返回DataFrame结构数据
    只传入一个，比如'Rank'只会返回一列并且是Series结构的数据
    '''
    extract_informs = second_filter[['Rank','Score','location']]

    extract_informs.to_csv('re_score_' + location + '.csv',encoding='GBK')

    # print(estimator.coef_,estimator.intercept_)
    # print(estimator.predict(second_filter_values)==lables)


if __name__ == '__main__':
    '''
    经过对样本数据岭回归的分析发现结果并不是很好，可以从以下的层面进行理解：
        岭回归主要还是遵循了最小二乘法的原理，最后结果还是会尽量使得损失函数最小，
        这种情况下会对某些比较重要的节点判断失误，比如说，对于评分均值小而且分数还普遍偏低的球员集体而言，
        如果出现某个球员的评分很高，那么这个球员的能力绝对是更有价值的，
        但是因为回归分析的结果必定是会偏离哪些极端数据的（这里高评分球员其实就相当于极端数据），
        这种情况下球员的预测评分必定很大程度地比实际偏低，所以对球员分数最后再进行回归分析必定是错误的选择
    '''
    LogisticRegress('back')