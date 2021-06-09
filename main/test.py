import pandas
import json
import numpy

# result = {}
# team_name = '国王'
#
# teamInfo = pandas.read_csv('../NBA_spider/files/team_static_data.csv',encoding='GBK',index_col=0)
# # 通过球队名称匹配对应的球队logo图标
# teamInfo = teamInfo[teamInfo.nickname==team_name]
# teamInfo = teamInfo.to_json(orient='records')
# # json加载后的列表中之后一个字典数据，获取这唯一一个字典作为球队信息
# teamInfo = json.loads(teamInfo)[0]
# result['teamInfo'] = teamInfo
#
# # 获取最终排名的球员信息并将球员名称作为一列数据
# team_player = pandas.read_csv('../NBA_spider/NBA球员数据分析/MVP球员预测/Final_Score.csv',
#                                   encoding='GBK', index_col=0).reset_index(). \
#         rename(columns=lambda x: x.replace('index', 'cnName'))
# # 通过队名选择所有属于该队的球员的name
# player_selected = team_player[team_player.teamName == team_name].reset_index(drop=True)[['cnName']].iloc[0:5, :]
# player_img = pandas.read_csv('../NBA_spider/files/playerInfo1.csv',encoding='utf-8',index_col=0)
# # 将筛选后的球员name和球员img进行匹配获取筛选后球员的img
# teamInfo_imgList = pandas.merge(player_selected,player_img,on=['cnName'],how='inner')
# teamInfo_imgList.rename(columns={'cnName':'name'},inplace=True)
# teamInfo_imgList = teamInfo_imgList.to_json(orient='records')
# teamInfo_imgList = json.loads(teamInfo_imgList)
# # 将 球员-图片 数据放入result中
# result['teamInfo_imgList'] = teamInfo_imgList
#
# teamInfo_player = []


# player = pandas.read_csv('../NBA_spider/NBA球员数据分析/MVP球员预测/Final_Score.csv',
#                              encoding='GBK',index_col=0)
# player['playername'] = player.index
# mvp_player = player.iloc[0,:]
# mvp_player = mvp_player.to_json(orient='records')
# mvp_player = json.loads(mvp_player)
# mvp_player_name = mvp_player[4]
# result = {'name':mvp_player_name,'honour':'2017-18赛季NBA常规赛MVP''\n'
#                                           '8届NBA全明星阵容（2013-20）''\n'
#                                           '6届NBA最佳阵容第一阵容（2014-15；2017-20）''\n'
#                                           '2011-12赛季NBA最佳第六人 、2012-13赛季NBA最佳阵容第三阵容''\n'
#                                           '2016-17赛季NBA助攻王、3届NBA得分王'}
# print(mvp_player)

player = pandas.read_csv('../NBA_spider/NBA球员数据分析/MVP球员预测/Final_Score.csv',
                             encoding='GBK', index_col=0)
player['playername'] = player.index
mvp_player = player.iloc[0, :]
mvp_player = mvp_player.to_json(orient='records')
mvp_player = json.loads(mvp_player)
mvp_player_name = mvp_player[4]
player_firstseason = pandas.read_csv('../NBA_spider/stats/季前赛/2018-2019_wash.csv',
                                     encoding='GBK')[['cnName','pointsPG','fgPCT','threesPCT'
    ,'assistsPG','stealsPG','blocksPG','turnoversPG','foulsPG']]
player_firstseason = player_firstseason[player_firstseason['cnName'].isin([mvp_player_name])]

player_secondseason = pandas.read_csv('../NBA_spider/stats/季前赛/2019-2020_wash.csv',
                                     encoding='GBK')[['cnName','pointsPG','fgPCT','threesPCT'
    ,'assistsPG','stealsPG','blocksPG','turnoversPG','foulsPG']]
player_secondseason = player_secondseason[player_secondseason['cnName'].isin([mvp_player_name])]

player_thirdseason = pandas.read_csv('../NBA_spider/stats/常规赛/2018-2019_wash.csv',
                                     encoding='GBK')[['cnName','pointsPG','fgPCT','threesPCT'
    ,'assistsPG','stealsPG','blocksPG','turnoversPG','foulsPG']]
player_thirdseason = player_thirdseason[player_thirdseason['cnName'].isin([mvp_player_name])]

player_forthseason = pandas.read_csv('../NBA_spider/stats/常规赛/2019-2020_wash.csv',
                                     encoding='GBK')[['cnName','pointsPG','fgPCT','threesPCT'
    ,'assistsPG','stealsPG','blocksPG','turnoversPG','foulsPG']]
player_forthseason = player_forthseason[player_forthseason['cnName'].isin([mvp_player_name])]

player_fifthseason = pandas.read_csv('../NBA_spider/stats/季后赛/2018-2019_wash.csv',
                                     encoding='GBK')[['cnName','pointsPG','fgPCT','threesPCT'
    ,'assistsPG','stealsPG','blocksPG','turnoversPG','foulsPG']]
player_fifthseason = player_fifthseason[player_fifthseason['cnName'].isin([mvp_player_name])]

player = pandas.concat([player_firstseason,player_secondseason,player_thirdseason,player_forthseason,
                        player_fifthseason],axis=0,join='outer',ignore_index=True)
norm = 'foulsPG'
norm_data = list(player[norm].values)
print()
