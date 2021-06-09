'''
author: feifei
date: 2020-12-23
file info: 整合程序
'''
import pandas
import json
import numpy

def unify():
    player = pandas.read_csv('Final_Score.csv',encoding='GBK',index_col=0)
    team_rank = player.groupby(by='teamName').apply(lambda x: numpy.mean(x)).sort_values(by='Score', ascending=False)[
        ['Score']]
    team_rank['Rank'] = range(1, len(team_rank) + 1)
    team = pandas.read_csv('team_final_rank.csv',encoding='GBK',index_col=0)
    # print(team_rank)
    team_rank = team
    team_rank['teamName'] = team_rank.index
    team_img = pandas.read_csv('../../../NBA_spider/files/team_img.csv',encoding='GBK').\
        rename(columns=lambda x: x.replace('nickname', 'teamName'), inplace=True)
    result = pandas.merge(team_rank,team_img,on='teamName',how='inner')
    result.to_csv('team_final_rank.csv',encoding='GBK')
    result = result.to_json(orient='records')

    result = json.loads(result)

    return result

if __name__ == '__main__':
    print(unify())