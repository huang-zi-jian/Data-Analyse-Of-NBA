'''
author: feifei
date: 2020-12-16
file info: NBA球员各指标之间的相关性分析
'''

from scipy.stats import pearsonr
import pandas
import csv

def R_p_value_Analyse(filepath):
    norm_data = pandas.read_csv(filepath, index_col=0, encoding='GBK')

    with open(file='relativity.csv', mode='w', newline='', encoding='GBK') as f:
        writer = csv.writer(f)
        # list(DataFrame)返回特征名列表
        # norm_name_list = list(norm_data)

        # columns[:-1]获取除最后一列以外的所有特征值名称
        norm_name_list = norm_data.columns[:-1]
        norm_temp = ['']
        norm_temp.extend(norm_name_list)
        writer.writerow(norm_temp)

        for norm_i in norm_name_list:
            temp = []
            temp.append(norm_i)

            for norm_j in norm_name_list:
                # r_p获取元祖，两个指标名相同就跳出循环
                if norm_j==norm_i:
                    r,p_value = pearsonr(norm_data[norm_i], norm_data[norm_j])
                    temp.append(r)
                    break

                r,p_value = pearsonr(norm_data[norm_i],norm_data[norm_j])
                temp.append(format(r,'.3f'))

            writer.writerow(temp)



    with open(file='p_value.csv', mode='w', newline='', encoding='GBK') as f:
        writer = csv.writer(f)
        # list(norm_data)获取DataFrame结构数据的列名列表
        # norm_list = list(norm_data)

        norm_name_list = norm_data.columns[:-1]
        norm_temp = ['']
        norm_temp.extend(norm_name_list)
        writer.writerow(norm_temp)

        for norm_i in norm_name_list:
            temp = []
            temp.append(norm_i)

            for norm_j in norm_name_list:
                # r_p获取元祖，两个指标名相同就跳出循环
                if norm_j==norm_i:
                    r,p_value = pearsonr(norm_data[norm_i], norm_data[norm_j])
                    temp.append(p_value)
                    break

                r,p_value = pearsonr(norm_data[norm_i],norm_data[norm_j])
                temp.append(format(p_value,'.3f'))

            writer.writerow(temp)

if __name__ == '__main__':
    R_p_value_Analyse('../../stats/常规赛/2019-2020_forward_wash.csv')