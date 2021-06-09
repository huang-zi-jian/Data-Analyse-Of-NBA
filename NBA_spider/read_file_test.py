'''
author: feifei
date: 2020-12-18
file info: 将球队对应的队员以及队员战场位置信息进行处理
'''

import shelve
import pandas

file = shelve.open('files/dict_team_player/team_player.dat')
dic_Team = file['dic_team_player']
file.close()

print(dic_Team)

palyers_location = {}
for team in dic_Team.values():
    for player in team:
        palyers_location[player[0]] = player[1]

result = pandas.DataFrame(palyers_location,index=['location']).T
result.to_csv('files/players_loc_display.csv',encoding='GBK')
# 新做一个字典数据集
team_dict = {}


# 前锋
Forward = {}
# 中锋
Striker = {}
# 后卫
Back = {}
for team_name in dic_Team.keys():
    # 将球员信息放进列表
    player_list= []
    # print(team_name)
    for player in dic_Team.get(team_name):
        # 获取球员名字
        player_name = player[0]

        position = []
        # 用in判断字符串中是否含有某些指定内容
        if '前锋' in player[1]:
            position.append('前锋')
            Forward[player_name] = '前锋'
        if '中锋' in player[1]:
            position.append('中锋')
            Striker[player_name] = '中锋'
        if '后卫' in player[1]:
            position.append('后卫')
            Back[player_name] = '后卫'

        player_dict = {}
        player_dict[player_name] = position
        # 将处理后的字典型的队员数据放进队员信息列表
        player_list.append(player_dict)

    team_dict[team_name] = player_list

file = shelve.open('files/dict_team_player/team_player_dict.dat')
file['team_player_dict'] = team_dict
file.close()

print(team_dict)
print(Forward)
print(Striker)
print(Back)

import pandas

forward = pandas.DataFrame(Forward,index=['location']).T
print(forward)
striker = pandas.DataFrame(Striker,index=['location']).T
print(forward)
back = pandas.DataFrame(Back,index=['location']).T
print(back)

norm_data = pandas.read_csv('stats/常规赛/2019-2020_wash.csv',encoding='GBK',index_col=0)
forward_result = pandas.concat([norm_data,forward],axis=1,join='inner')
print(forward_result)
striker_result = pandas.concat([norm_data,striker],axis=1,join='inner')
print(striker_result)
back_result = pandas.concat([norm_data,back],axis=1,join='inner')
print(back_result)