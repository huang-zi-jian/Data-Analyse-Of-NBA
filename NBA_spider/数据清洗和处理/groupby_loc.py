'''
author: feifei
date: 2020-12-18
file info: 将球员按照位置进行分组，把不同个组的球员放进不同文件
'''

import shelve
import pandas

def GroupBy_Loc(filepath):

    # 读取球队球员数据文件，用于获取队员以及位置信息
    file = shelve.open('../files/dict_team_player/team_player.dat')
    dic_Team = file['dic_team_player']
    file.close()

    '''
    三个位置分别做不同的字典集用于存储相同位置的球员
    之后用pandas.concat的方法将列合并，按照index球员一一对应取交集的方式
    '''
    # 前锋
    Forward = {}
    # 中锋
    Striker = {}
    # 后卫
    Back = {}

    for team_name in dic_Team.keys():
        '''
        将每个位置的所有球员名字放进同一个文件
        这里Forward、Striker、Back变量分别用于存储前锋、中锋和后卫的球员数据
        变量通过name和location键值对的方式存储
        '''
        for player in dic_Team.get(team_name):
            # 获取球员名字
            player_name = player[0]

            position = []
            # 用in判断字符串中是否含有某些指定内容
            if '前锋' in player[1]:
                # Forward中以球员名和 '前锋' 作为键值对
                Forward[player_name] = '前锋'
            if '中锋' in player[1]:
                # Striker中以球员名和 '中锋' 作为键值对
                Striker[player_name] = '中锋'
            if '后卫' in player[1]:
                # Back中以球员名和 '后卫' 作为键值对
                Back[player_name] = '后卫'


    # print(Forward)
    # print(Striker)
    # print(Back)

    '''
    将字典变量Forward、Striker和Back转化为DataFrame结构数据
    '''
    forward = pandas.DataFrame(Forward,index=['location']).T
    print(forward)
    striker = pandas.DataFrame(Striker,index=['location']).T
    print(forward)
    back = pandas.DataFrame(Back,index=['location']).T
    print(back)


    # 读取清洗后的球员指标数据
    path = filepath + '_wash.csv'
    norm_data = pandas.read_csv(path,encoding='GBK',index_col=0)
    '''
    通过上面得到的不同位置所有的球员name数据和清洗后的球员指标数据通过球员名字进行合并，
    axis=1表示列合并；join='inner'取交集，如果要选择指定的列对其，设置join_axes参数
    '''
    forward_result = pandas.concat([norm_data,forward],axis=1,join='inner')
    print(forward_result)
    striker_result = pandas.concat([norm_data,striker],axis=1,join='inner')
    print(striker_result)
    back_result = pandas.concat([norm_data,back],axis=1,join='inner')
    print(back_result)


    '''
    将合并后的数据写入CSV文件
    '''
    forward_path = filepath + '_forward' + '_wash.csv'
    forward_result.to_csv(forward_path,encoding='GBK')
    striker_path = filepath + '_striker' + '_wash.csv'
    striker_result.to_csv(striker_path,encoding='GBK')
    back_path = filepath + '_back' + '_wash.csv'
    back_result.to_csv(back_path,encoding='GBK')


if __name__ == '__main__':
    GroupBy_Loc('../stats/季前赛/2019-2020')