# -*- coding:utf-8 -*-

'''
File Name: server.py
Create By: feifei
Create Date: 2020-12-11
File Info: flask框架
Change Info: NULL
'''
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from sqlalchemy import PrimaryKeyConstraint
from flask_sqlalchemy import SQLAlchemy
from main.form_class_item import *
import base64
from main.App_Initial import app,db,User,Role
import json
import pandas
import numpy

'''
用json和flask模块中的jsonify其实本质差不多，json.dumps返回的content-type是text/html; charset=utf-8类型的数据；
而jsonify返回的是application/json数据，这样其实更利于前端的数据提取，而且jsonify往往会有压缩数据的功能
'''

# 系统初始登录路由
'''
登录板块
'''
@app.route('/user/login', methods=['POST'])
def login_surface():

    # post请求和get请求获取前端参数的方式不同，
    # 获取前端post请求的方式是调用request.get_json()的方式；
    # 获取get请求参数的方式是调用request.args.get('...')
    user = request.get_json()['username']
    password = request.get_json()['password']
    print('登录用户名:',user,'\n','用户名密码:',password)
    # 数据库用户名和密码匹配
    user = User.query.filter(User.name == user, User.password == password,User.is_delete == False).first()
    if user:
        # url_for()方法传入路由对应的函数就会返回路由对应的地址，
        # redirect()传入路由地址作为参数并且返回就会重定向置该路由执行该路由操作
        return jsonify({'msg':True,'code':200,'token':'abcdefg123456'})
    else:
        return jsonify({'msg':False,'code':500})




# 获取各项指标排名前列的球员信息
'''
球员——排名显示板块
'''
@app.route('/api/player/normRank/',methods=['GET'])
def get_player_rank():
    norm = request.args.get('item')
    if norm == 'final_rank':
        player_rank = pandas.read_csv('NBA_spider/NBA球员数据分析/MVP球员预测/Final_Score.csv',
                                      encoding='GBK',index_col=0).iloc[0:5,:]
        # 将球员名字索引设为列
        player_rank['name'] = player_rank.index
        result = player_rank.to_json(orient='records')
        result = json.loads(result)

        return jsonify({'data':result,'code':200,'token':'abcdefg123456'})

    else:
        player = pandas.read_csv('NBA_spider/stats/常规赛/2019-2020_wash.csv',
                                 encoding='GBK',index_col=0)
        player.sort_values(by=norm,ascending=False,inplace=True)
        player_rank = player[[norm]].iloc[0:6,:]
        player_rank['name'] = player_rank.index

        player_rank.to_json(orient='records')
        player_rank = json.loads(player_rank)

        return jsonify({'player_rank':player_rank,'code':200,'token':'abcdefg123456'})


    # 球员指标数据路由，获取前端传过来的norm指标名称
'''
球员——专项对比板块
'''
@app.route('/api/player/itemRank/',methods=['GET'])
def get_player_norm():
    norm = request.args.get('item')
    # 控制台打印get请求的norm指标参数
    print(norm)

    # 以常规赛2019-2020的数据为基础获取norm指标排名前20的球员信息
    player_norm = pandas.read_csv('NBA_spider/stats/常规赛/2019-2020_wash.csv',
                                     encoding='GBK',index_col=0)[[norm]].iloc[0:20,:]
    player_norm['Rank'] = range(1, len(player_norm) + 1)

    # 将队名附加到经过筛选后的20名球员数据中
    team_name = pandas.read_csv('NBA_spider/stats/常规赛/2019-2020.csv', index_col=5)[['teamName']]
    result = pandas.concat([player_norm, team_name], axis=1, join='inner')
    # 为指标重命名，统一为score，便于数据传给前端方便处理
    result.rename(columns=lambda x: x.replace(norm, 'score'), inplace=True)

    # 季前赛2018-2019的数据作为第一赛季数据
    first_season = pandas.read_csv('NBA_spider/stats/季前赛/2018-2019_wash.csv',
                                   encoding='GBK', index_col=0)[[norm]]
    # 将第一赛季数据与筛选出来的20名球员通过名字合并取交集，并且将norn指标名改成first_season，
    # 为了防止下一个赛季的同一个norm名加进来导致列名冲突，同时这样也能方便前端的数据处理
    result = pandas.concat([result, first_season], axis=1, join='inner')
    result.rename(columns=lambda x: x.replace(norm, 'first_season'), inplace=True)

    '''
    之后每个赛季都和上一次合并后的球员数据进行合并取交集，5个赛季全部合并完成之后
    说明剩余下来的球员5个赛季都有数据，取排名前五的球员作为结果返回
    '''
    second_season = pandas.read_csv('NBA_spider/stats/季前赛/2019-2020_wash.csv',
                                    encoding='GBK', index_col=0)[[norm]]
    result = pandas.concat([result, second_season], axis=1, join='inner')
    result.rename(columns=lambda x: x.replace(norm, 'second_season'), inplace=True)
    third_season = pandas.read_csv('NBA_spider/stats/季后赛/2018-2019_wash.csv',
                                   encoding='GBK', index_col=0)[[norm]]

    result = pandas.concat([result, third_season], axis=1, join='inner')
    result.rename(columns=lambda x: x.replace(norm, 'third_season'), inplace=True)
    forth_season = pandas.read_csv('NBA_spider/stats/常规赛/2018-2019_wash.csv',
                                   encoding='GBK', index_col=0)[[norm]]

    result = pandas.concat([result, forth_season], axis=1, join='inner')
    result.rename(columns=lambda x: x.replace(norm, 'forth_season'), inplace=True)
    fifth_season = pandas.read_csv('NBA_spider/stats/常规赛/2019-2020_wash.csv',
                                   encoding='GBK', index_col=0)[[norm]]

    result = pandas.concat([result, fifth_season], axis=1, join='inner')
    result.rename(columns=lambda x: x.replace(norm, 'fifth_season'), inplace=True)
    # 获取球员img信息，然后与筛选出来的队员合并获取对应球员的img信息
    img = pandas.read_csv('NBA_spider/files/playerInfo1.csv', index_col=1)[['img']]
    result = pandas.concat([result, img], axis=1, join='inner')

    result.sort_values(by='score', ascending=False, inplace=True)
    result = result.iloc[0:5, :]
    result['Rank'] = range(1, len(result) + 1)
    result['name'] = result.index

    # 调用to_json返回的是字符串数据orient参数指定json数据的字典存储格式
    result = result.to_json(orient='records')
    result = json.loads(result)
    # print(result)

    return jsonify({'data':result,'code':200,'token':'abcdefg123456'})



# # 球员排名数据路由
# @app.route('/api/player/rank/',methods=['GET'])
# def get_player_rank():
#     player_rank = pandas.read_csv('NBA_spider/NBA球员数据分析/MVP球员预测/Final_Score.csv',
#                                   encoding='GBK',index_col=0).iloc[0:5,:]
#     # 将球员名字索引设为列
#     player_rank['name'] = player_rank.index
#     result = player_rank.to_json(orient='records')
#
#     return jsonify({'data':result,'code':200,'token':'abcdefg123456'})



# 总球队数据路由
'''
球队——排名显示板块
'''
@app.route('/api/team/',methods=['GET'])
def get_team():
    pageSize = int(request.args.get('pageSize'))
    pageNum = int(request.args.get('pageNum'))

    team_data = pandas.read_csv('NBA_spider/files/team_display.csv', encoding='GBK')
    team_else = pandas.read_csv('NBA_spider/files/team_static_data.csv',
                                encoding='GBK', index_col=0)
    team = pandas.concat([team_data, team_else], axis=1, join='inner')

    select_team = team.iloc[(pageNum-1)*pageSize:pageNum*pageSize,:]
    # team_data.insert(loc=2, column='Rank', value=range(1, len(team_data) + 1))
    select_team_json = select_team.to_json(orient='records')
    select_team_json = json.loads(select_team_json)

    return jsonify({'data':select_team_json,'code':200,'token':'abcdefg123456'})



# 前五支球队各赛季各项指标数据路由
'''
球队——数据对比板块
'''
@app.route('/api/team/itemRank/',methods=['GET'])
def get_team_win_lose():
    # team_firstseason = pandas.read_csv('../NBA_spider/stats/team/2020/team.csv', index_col=0,
    #                             encoding='GBK')[['W', 'L', 'cnname']]
    # # 首先通过win场次的递减排序和lose场次的递增排序
    # team_firstseason.sort_values(by=['W', 'L'], ascending=[False, True], inplace=True)
    # team_firstseason.iloc[0:5,:]

    norm = request.args.get('item')
    # 胜负数是两个数据，和其他指标不同，需要经过判断区分开来
    if norm == 'W_L':
        team_2019 = pandas.read_csv('NBA_spider/stats/team/2019/team.csv', index_col='cnname',
                                    encoding='GBK')[['W', 'L']]
        first_season = pandas.read_csv('NBA_spider/stats/team/2016/team.csv', index_col='cnname',
                                       encoding='GBK')[['W', 'L']]
        second_season = pandas.read_csv('NBA_spider/stats/team/2017/team.csv', index_col='cnname',
                                        encoding='GBK')[['W', 'L']]
        third_season = pandas.read_csv('NBA_spider/stats/team/2018/team.csv', index_col='cnname',
                                       encoding='GBK')[['W', 'L']]
        forth_season = pandas.read_csv('NBA_spider/stats/team/2019/team.csv', index_col='cnname',
                                       encoding='GBK')[['W', 'L']]
        fifth_season = pandas.read_csv('NBA_spider/stats/team/2020/team.csv', index_col='cnname',
                                       encoding='GBK')[['W', 'L']]
    else:
        team_2019 = pandas.read_csv('NBA_spider/stats/team/2019/team.csv', index_col='cnname',
                                    encoding='GBK')[[norm]]
        first_season = pandas.read_csv('NBA_spider/stats/team/2016/team.csv', index_col='cnname',
                                       encoding='GBK')[[norm]]
        second_season = pandas.read_csv('NBA_spider/stats/team/2017/team.csv', index_col='cnname',
                                        encoding='GBK')[[norm]]
        third_season = pandas.read_csv('NBA_spider/stats/team/2018/team.csv', index_col='cnname',
                                       encoding='GBK')[[norm]]
        forth_season = pandas.read_csv('NBA_spider/stats/team/2019/team.csv', index_col='cnname',
                                       encoding='GBK')[[norm]]
        fifth_season = pandas.read_csv('NBA_spider/stats/team/2020/team.csv', index_col='cnname',
                                       encoding='GBK')[[norm]]
    # 将2019年数据作为标准数据，除了PF犯规，其他指标均以降序排列rank
    if norm == 'PF':
        team_2019.sort_values(by=norm, ascending=True, inplace=True)
    # 胜负场按照胜优先再负的方式
    elif norm == 'W_L':
        team_2019.sort_values(by=['W', 'L'], ascending=[False, True], inplace=True)
    else:
        team_2019.sort_values(by=norm, ascending=False, inplace=True)

    # 取指标排名前五支球队
    team_2019 = team_2019.iloc[0:5, :]
    img = pandas.read_csv('NBA_spider/files/team_static_data.csv',
                          encoding='GBK', index_col='nickname')[['img']]
    # 将img附加到球队数据的后面
    result = pandas.concat([team_2019, img], axis=1, join='inner')

    if norm != 'W_L':
        # 将norm指标改名统一
        result.rename(columns=lambda x: x.replace(norm, 'score'), inplace=True)
        result['Rank'] = range(1, len(result) + 1)
        # 将第每一赛季的norm指标数据附加到被选择的球队数据后面然后再将指标名改为赛季名称
        result = pandas.concat([result, first_season], axis=1, join='inner')
        result.rename(columns=lambda x: x.replace(norm, 'first_season'), inplace=True)
        result = pandas.concat([result, second_season], axis=1, join='inner')
        result.rename(columns=lambda x: x.replace(norm, 'second_season'), inplace=True)
        result = pandas.concat([result, third_season], axis=1, join='inner')
        result.rename(columns=lambda x: x.replace(norm, 'third_season'), inplace=True)
        result = pandas.concat([result, forth_season], axis=1, join='inner')
        result.rename(columns=lambda x: x.replace(norm, 'forth_season'), inplace=True)
        result = pandas.concat([result, fifth_season], axis=1, join='inner')
        result.rename(columns=lambda x: x.replace(norm, 'fifth_season'), inplace=True)

    else:
        result.rename(columns={'W': 'score_W'}, inplace=True)
        result.rename(columns={'L': 'score_L'}, inplace=True)
        result['Rank'] = range(1, len(result) + 1)
        # 将第每一赛季的norm指标数据附加到被选择的球队数据后面然后再将指标名改为赛季名称
        result = pandas.concat([result, first_season], axis=1, join='inner')
        result.rename(columns={'W': 'first_season_W'}, inplace=True)
        result.rename(columns={'L': 'first_season_L'}, inplace=True)
        result = pandas.concat([result, second_season], axis=1, join='inner')
        result.rename(columns={'W': 'second_season_W'}, inplace=True)
        result.rename(columns={'L': 'second_season_L'}, inplace=True)
        result = pandas.concat([result, third_season], axis=1, join='inner')
        result.rename(columns={'W': 'third_season_W'}, inplace=True)
        result.rename(columns={'L': 'third_season_L'}, inplace=True)
        result = pandas.concat([result, forth_season], axis=1, join='inner')
        result.rename(columns={'W': 'forth_season_W'}, inplace=True)
        result.rename(columns={'L': 'forth_season_L'}, inplace=True)
        result = pandas.concat([result, fifth_season], axis=1, join='inner')
        result.rename(columns={'W': 'fifth_season_W'}, inplace=True)
        result.rename(columns={'L': 'fifth_season_L'}, inplace=True)

    result['name'] = result.index
    result = result.to_json(orient='records')
    result = json.loads(result)

    return jsonify({'data':result,'code':200,'token':'abcdefg123456'})



# 获取各项指标排名第一的球队的前五个球员信息
'''
球队——数据对比——球队先锋
'''
@app.route('/api/team/firstDetail/',methods=['GET'])
def best_team_player():
    team_name = request.args.get('item')
    team_img_honour = pandas.read_csv('NBA_spider/files/team_static_data.csv',
                                      encoding='GBK', index_col=0).rename(
        columns=lambda x: x.replace('nickname', 'cnName'))

    team = team_img_honour[team_img_honour['cnName'].isin([team_name])][['cnName', 'img']]
    # 从预测球员综合得分的文件中获取队伍排名前五的球员名字，之后用球员们名字对应各赛季取数据交集
    team_player = pandas.read_csv('NBA_spider/NBA球员数据分析/MVP球员预测/Final_Score.csv',
                                  encoding='GBK', index_col=0).reset_index(). \
        rename(columns=lambda x: x.replace('index', 'cnName'))
    player_selected = team_player[team_player.get('teamName') == team_name].reset_index(drop=True)[['cnName']].iloc[0:5,
                      :]
    player_img = pandas.read_csv('NBA_spider/files/playerInfo1.csv', index_col=0)
    player_result = pandas.merge(player_selected, player_img, on='cnName', how='inner')
    player_result = player_result.to_json(orient='records')
    player_result = json.loads(player_result)
    team_result = team.to_json(orient='records')
    team_result = json.loads(team_result)
    player_result.insert(3, team_result[0])

    return jsonify({'data': player_result, 'code': 200, 'token': 'abcdefg123456'})


# 获取球队综合总排名以及综合评分
@app.route('/api/team/finalRank/',methods=['GET'])
def team_finalRank():

    player = pandas.read_csv('NBA_spider/NBA球员数据分析/MVP球员预测/Final_Score.csv',
                             encoding='GBK',index_col=0)
    team_rank = player.groupby(by='teamName').apply(lambda x: numpy.mean(x)).sort_values(by='Score', ascending=False)[
        ['Score']]
    team_rank['Rank'] = range(1, len(team_rank) + 1)
    team = pandas.read_csv('NBA_spider/NBA球员数据分析/MVP球员预测/team_final_rank.csv', encoding='GBK', index_col=0)
    print(team_rank)
    # team
    team_rank = team
    team_rank.to_csv('team_final_rank.csv',encoding='GBK')
    team_rank = team_rank.to_json(orient='records')
    result = json.loads(team_rank)

    return jsonify({'data':result,'code':200,'token':'abcdefg123456'})


# mvp球员数据接口路由
@app.route('/api/mvp/detail/',methods=['GET'])
def player_mvp():
    norm = request.args.get('item')
    player = pandas.read_csv('NBA_spider/NBA球员数据分析/MVP球员预测/Final_Score.csv',
                             encoding='GBK', index_col=0)
    player['playername'] = player.index
    mvp_player = player.iloc[0, :]
    mvp_player = mvp_player.to_json(orient='records')
    mvp_player = json.loads(mvp_player)
    mvp_player_name = mvp_player[4]
    player_firstseason = pandas.read_csv('NBA_spider/stats/季前赛/2018-2019_wash.csv',
                                         encoding='GBK')[['cnName', 'pointsPG', 'fgPCT', 'points' ,'threesPCT'
        , 'assistsPG', 'stealsPG', 'blocksPG', 'turnoversPG', 'foulsPG']]
    player_firstseason = player_firstseason[player_firstseason['cnName'].isin([mvp_player_name])]

    player_secondseason = pandas.read_csv('NBA_spider/stats/季前赛/2019-2020_wash.csv',
                                          encoding='GBK')[['cnName', 'pointsPG', 'fgPCT', 'points' ,'threesPCT'
        , 'assistsPG', 'stealsPG', 'blocksPG', 'turnoversPG', 'foulsPG']]
    player_secondseason = player_secondseason[player_secondseason['cnName'].isin([mvp_player_name])]

    player_thirdseason = pandas.read_csv('NBA_spider/stats/常规赛/2018-2019_wash.csv',
                                         encoding='GBK')[['cnName', 'pointsPG', 'fgPCT', 'points' ,'threesPCT'
        , 'assistsPG', 'stealsPG', 'blocksPG', 'turnoversPG', 'foulsPG']]
    player_thirdseason = player_thirdseason[player_thirdseason['cnName'].isin([mvp_player_name])]

    player_forthseason = pandas.read_csv('NBA_spider/stats/常规赛/2019-2020_wash.csv',
                                         encoding='GBK')[['cnName', 'pointsPG', 'fgPCT', 'points' ,'threesPCT'
        , 'assistsPG', 'stealsPG', 'blocksPG', 'turnoversPG', 'foulsPG']]
    player_forthseason = player_forthseason[player_forthseason['cnName'].isin([mvp_player_name])]

    player_fifthseason = pandas.read_csv('NBA_spider/stats/季后赛/2018-2019_wash.csv',
                                         encoding='GBK')[['cnName', 'pointsPG', 'fgPCT', 'points' ,'threesPCT'
        , 'assistsPG', 'stealsPG', 'blocksPG', 'turnoversPG', 'foulsPG']]
    player_fifthseason = player_fifthseason[player_fifthseason['cnName'].isin([mvp_player_name])]

    player = pandas.concat([player_firstseason, player_secondseason, player_thirdseason, player_forthseason,
                            player_fifthseason], axis=0, join='outer', ignore_index=True)

    # norm = 'foulsPG'
    norm_data = player[norm].values
    result = {'first': norm_data[0], 'second': norm_data[1], 'third': norm_data[2], 'forth': norm_data[3],
              'fifth': norm_data[4]}

    return {'data':result,'code':200,'token':'abcdefg123456'}



if __name__ == '__main__':
    # 注释如果再次运行，数据库已经保存内容
    # db.drop_all()
    # db.create_all()
    #
    # # role_1 = Role(role_name='管理员')
    # role_1 = Role(role_name='admin')
    # role_2 = Role(role_name='user')
    # # role_2 = Role(role_name='用户')
    #
    # db.session.add_all([role_1, role_2])
    # db.session.commit()
    #
    # user_1 = User(name='hzj', password='20000', email='1@qq.com', role_id=role_1.id, is_delete=False)
    # user_2 = User(name='dyf', password='12345', email='2@qq.com', role_id=role_2.id, is_delete=False)
    # user_3 = User(name='admin', password='123456', email='123@qq.com', role_id=role_1.id, is_delete=False)
    # db.session.add_all([user_1, user_2, user_3])
    # db.session.commit()

    # app.run(host='127.0.0.1',port=8080)
    app.run(host='127.0.0.1',port=8080)
