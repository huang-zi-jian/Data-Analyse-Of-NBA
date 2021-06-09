'''
author: feifei
date: 2020-12-20
file info: 将所有评分好的球员信息汇总生成总成员评分表
'''

import pandas
import numpy
import shelve

def Gather_Final_Score():
    back_csv = pandas.read_csv('re_score_back.csv', encoding='GBK', index_col=0)
    forward_csv = pandas.read_csv('re_score_forward.csv', encoding='GBK', index_col=0)
    striker_csv = pandas.read_csv('re_score_striker.csv', encoding='GBK', index_col=0)
    # print(back_csv)
    # print(forward_csv)
    # print(striker_csv)

    result_frame = pandas.concat([back_csv,forward_csv,striker_csv],axis=0)
    '''
    DataFrame经过groupby之后，apply方法传入lambda匿名函数，
    lambda参数 x 就相当于对groupby之后的每个组作为参数迭代传入，
    groupby之后分组的因素会更新原来的一列
    而且groupby之后返回的仍然是DataFrame结构数据，
    numpy.mean(x) 对每个group的每一列求均值
    '''
    result_frame = result_frame.groupby(result_frame.index).apply(lambda x:numpy.mean(x))
    print(result_frame)

    # 读取原球队-球员数据
    file = shelve.open('../../files/dict_team_player/team_player.dat')
    dic_Team = file['dic_team_player']
    file.close()
    # print(dic_Team)

    # 将球员信息和对应的位置信息按字典方式存储
    players_dict = {}
    for team in dic_Team.values():
        for player in team:
            # player[0]为球员名，player[1]为球员位置
            players_dict[player[0]] = player[1]

    players_loc = pandas.DataFrame(players_dict,index=['Location']).T
    # print(players_loc)

    # 对球员位置信息以及球员最终得分进行整合，再按照得分进行Rank，最后重置Rank
    result_gather = pandas.concat([result_frame,players_loc],axis=1,join='inner')
    result_gather.sort_values(by='Score',ascending=False,inplace=True)
    result_gather['Rank'] = range(1,len(result_gather) + 1)

    # 增加球员对应的球队信息
    playername_teamname = pandas.read_csv('../../stats/常规赛/playername_teamname.csv',
                                          encoding='GBK',index_col=0)
    result_gather = pandas.concat([result_gather,playername_teamname],axis=1,join='inner')

    # 存入文件
    result_gather.to_csv('Final_Score.csv',encoding='GBK')


if __name__ == '__main__':
    Gather_Final_Score()