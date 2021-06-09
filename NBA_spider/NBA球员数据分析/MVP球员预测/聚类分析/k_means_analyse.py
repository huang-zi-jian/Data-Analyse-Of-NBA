'''
author: feifei
date: 2020-12-18
file info: 通过k-means无监督对初步提取的数据进行分类，观察效果;
'''

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas


def K_Means_Analyse(random_state):
    '''

    :param random_state: 用于之后k-means确定伪随机数，使得最后输出标签的结果相同
    :return:
    '''
    first_filter = pandas.read_csv('../一轮评分/rank_.csv', index_col=0, encoding='GBK')
    first_filter_values = first_filter.values[:,:-3]

    # 数据标准化
    Stand_transfer = StandardScaler()
    first_filter_Stand = Stand_transfer.fit_transform(first_filter_values)

     # 数据降维
    Pca_transfer = PCA(n_components=0.95)
    first_filter_Pca = Pca_transfer.fit_transform(first_filter_Stand)

    # 无监督二分类
    estimator = KMeans(n_clusters=2,max_iter=10000,random_state=random_state)
    estimator.fit(first_filter_Pca)

    # 聚类中心，相当于多维坐标
    # centers = estimator.cluster_centers_

    # 获取分类器分类后的结果标签
    fit_lables = estimator.labels_
    # lable = estimator.transform(first_filter_Pca)

    # 将分类标签加入原数据之后存入新的文件中
    first_filter['k-means-lable'] = fit_lables
    first_filter.to_csv('rank_add_k-means.csv',encoding='GBK')

    # 用分类器对原数据进行预测获取标签并和真实标签对比，
    # pred_lables = estimator.predict(first_filter_Pca)
    # print(fit_lables==pred_lables)

    # 对k-means结果进行轮廓系数评估
    sci_score = silhouette_score(first_filter_Pca,labels=fit_lables)
    print('sci结果评估：',sci_score)


if __name__ == '__main__':
    K_Means_Analyse(0)