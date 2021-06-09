'''
author: feifei
date: 2020-12-16
file info: 展示爬取的NBA球员位置信息
'''

import shelve
import pandas

# 将球员及其对应的位置信息写入文件
def Location_Display():
    file = shelve.open('../../files/dict_team_player/team_player.dat')
    dic_Team = file['dic_team_player']
    file.close()
    # print(dic_Team)

    palyers_location = {}
    for team in dic_Team.values():
        for player in team:
            palyers_location[player[0]] = player[1]

    result = pandas.DataFrame(palyers_location,index=['location']).T
    result.to_csv('players_location.csv',encoding='GBK')


if __name__ == '__main__':
    Location_Display()