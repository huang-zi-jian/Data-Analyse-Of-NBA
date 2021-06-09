'''
author: feifei
date: 2020-12-16
file info: NBA球员指标的统计量分析
'''
import pandas
import csv

def Statistics_Analyse(filepath):
    norm_data = pandas.read_csv(filepath, index_col=0, encoding='GBK')
    '''
    describe函数输出指标含义：
        count：数量统计，此列共有多少有效值
        unipue：不同的值有多少个
        std：标准差
        min：最小值
        25%：四分之一分位数
        50%：二分之一分位数
        75%：四分之三分位数
        max：最大值
        mean：均值
    '''
    print(norm_data.describe().T)

    # list(DataFrame)返回DataFrame数据的列名列表
    # norm_name_list = list(norm_data)

    # 获取除了最后一列location外的所有列属性名称
    norm_name_list = norm_data.columns[:-1]
    with open(file='forward_statistics.csv', mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        temp = ['','Num','Mean','Median','Min','Max','Std','Skew','Kurt','Var']
        writer.writerow(temp)

        for norm_name in norm_name_list:
            temp = []
            temp.append(norm_name)
            temp.append(norm_data[norm_name].count())
            temp.append(format(norm_data[norm_name].mean(),'.2f'))
            temp.append(format(norm_data[norm_name].median(),'.2f'))
            temp.append(format(norm_data[norm_name].min(),'.2f'))
            temp.append(format(norm_data[norm_name].max(),'.2f'))
            temp.append(format(norm_data[norm_name].std(),'.2f'))
            # skew是偏态系数，相对正态分布而言的偏态指标
            temp.append(format(norm_data[norm_name].skew(),'.2f'))
            # Kurt是峰态系数，正态分布的峰态系数是3，均匀分布的峰态系数为1.8，峰态系数越大表明峰的形状更加陡峭
            temp.append(format(norm_data[norm_name].kurt(),'.2f'))
            # var是变异系数: 标准差/均值，用于衡量数据的离散程度，不受量纲影响，值越大越离散
            temp.append(format(norm_data[norm_name].var(),'.2f'))

            writer.writerow(temp)


if __name__ == '__main__':
    Statistics_Analyse('../../stats/常规赛/2019-2020_forward_wash.csv')