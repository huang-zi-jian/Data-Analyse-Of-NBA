'''
author: feifei
date: 2020-12-17
file info: 读取包含所有球员信息的CSV文件数据并进行数据清洗后存入新的CSV文件
'''

import pandas

def Data_Wash(filepath):
    S_path = filepath + '.csv'
    pan_data = pandas.read_csv(S_path,index_col=0)
    pan_data.set_index(['cnName'],inplace=True)
    pan_data.drop(columns=['doubleDoubles','efficiencyPG','ejections','enName','fgMissed','flagrantFouls',
                           'ftMissed','seasonType','tFouls','teamId','threesMisses','tripleDoubles','teamName',
                           'playerId','seasonId','jerseyNum','assists','blocks','defensiveRebounds',
                           'fgAttempted','fgMade','fouls','ftAttempted','ftMade','offensiveRebounds',
                           'rebounds','steals','threesAttempted','threesMade','turnovers','threesAttemptedPG'],inplace=True)
    E_path = filepath + '_wash.csv'
    pan_data.to_csv(E_path,encoding='GBK')
# with open(file='../stats/季前赛/2014-2015.csv',mode='r',encoding='utf-8') as f:

if __name__ == '__main__':
    Data_Wash('../stats/常规赛/2019-2020')
