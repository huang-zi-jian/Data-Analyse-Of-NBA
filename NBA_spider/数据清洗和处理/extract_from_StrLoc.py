'''
author: feifei
date: 2020-12-18
file info: 将爬取获得的球员位置信息以列表的方式存储（因为有的球员有两个位置）
'''

import shelve

def Extract_from_StrLoc():
    file = shelve.open('../files/dict_team_player/team_player.dat')
    dic_Team = file['dic_team_player']
    file.close()

    # 打印重整前的数据
    print(dic_Team)


    team_dict = {}
    for team_name in dic_Team.keys():
        '''
        爬取的数据中有的球员的位置可能不止一种，所以循环将位置字符串数据分解后再用列表重组；
        team_dict用于存放重组后的数据
        '''
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
            if '中锋' in player[1]:
                position.append('中锋')
            if '后卫' in player[1]:
                position.append('后卫')

            # player_dict字典用于存放一个球员的位置数据
            player_dict = {}
            # 球员name和位置列表作为字典键值对
            player_dict[player_name] = position
            # 将处理后的字典型的队员数据放进队员信息列表
            player_list.append(player_dict)

        # 队名和队员信息列表作为键值对
        team_dict[team_name] = player_list

    # 打印重整后的数据
    print(team_dict)
    '''
    将重组后的数据放入新的对象文件，下次用的时候就不用再次重组原数据
    '''
    file = shelve.open('../files/dict_team_player/team_player_dict.dat')
    file['team_player_dict'] = team_dict
    file.close()

if __name__ == '__main__':
    # 函数执行一次后重整数据就以对象的形式存入dat文件，就不需要再次重整
    Extract_from_StrLoc()