'''
File Name: team_data.py
Create By: feifei
Create Date: 2020-12-10
File Info: 虎扑NBA球队信息数据爬取
Change Info: 获取球队指标信息文件——2020-12-26
'''

import requests
import random
from parsel import Selector
from time import sleep
import csv

def GetData():

        user_Agent = [
                "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
                "NOKIA5700/ UCWEB7.0.2.37/28/999",
                "Openwave/ UCWEB7.0.2.37/28/999",
                "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
            ]

        # 虎扑网址
        url = 'https://nba.hupu.com/stats/teams'

        response = requests.get(url, headers={"User-Agent": random.choice(user_Agent)}, timeout=2)
        sleep(1)

        html_data = Selector(response.text)

        # 获取球队信息
        tr_list = html_data.xpath('//div[@class="tables"]/table/tbody/tr[position()>2]')
        team_list = []
        for tr in tr_list:
                team = {}
                rank = tr.xpath('./td[1]/text()').extract_first()
                team_name = tr.xpath('./td[2]/a/text()').extract_first()
                shot_accuracy = tr.xpath('./td[3]/text()').extract_first()  # 投篮命中率
                treble_accuracy = tr.xpath('./td[6]/text()').extract_first()  #  三分命中率
                penalty_accuracy = tr.xpath('./td[9]/text()').extract_first()  #  罚球命中率
                rebounds = tr.xpath('./td[12]/text()').extract_first()  #  总篮板
                assist = tr.xpath('./td[15]/text()').extract_first()  # 助攻
                fault = tr.xpath('./td[16]/text()').extract_first()  # 失误
                intercept = tr.xpath('./td[17]/text()').extract_first()  # 抢断
                nut_cap = tr.xpath('./td[18]/text()').extract_first()  # 盖帽
                illegal = tr.xpath('./td[19]/text()').extract_first()  # 犯规
                scores = tr.xpath('./td[20]/text()').extract_first()  # 总得分

                team['Rank'] = rank
                team['TeamName'] = team_name
                team['ShotAccuracy'] = shot_accuracy
                team['TrebleAccuracy'] = treble_accuracy
                team['PenaltyAccuracy'] = penalty_accuracy
                team['Rebounds'] = rebounds
                team['Assist'] = assist
                team['Fault'] = fault
                team['Intercept'] = intercept
                team['NutCap'] = nut_cap
                team['Illegal'] = illegal
                team['Scores'] = scores

                # 加入每支球队的信息
                team_list.append(team)

        return team_list

        '''
        # 定义数据分类获取函数
        def data_classfy(html_data,num):
                dict_list = {3: scores, 9: backboard, 14: assisting ,15: assisting_rate, 17: fault, 18: intercept ,
                        19: not_cap, 22: three_shot, 26: penalty_shot, 27: penalty_shot_rate, 28: break_rule}
                dict_replace = {3: 'scores', 9: 'backboard', 14: 'assisting' ,15: 'assisting_rate', 17: 'fault', 18: 'intercept'
                        , 19: 'not_cap', 22: 'three_shot', 26: 'penalty_shot', 27: 'penalty_shot_rate', 28: 'break_rule'}

                add_r = '//div[@class="main"]/ul/li[' + str(num) + ']/a/@href'
                li_url = 'https:' + html_data.xpath(add_r).extract_first()
                response_else = requests.get(li_url, headers={"User-Agent": random.choice(user_Agent)}, timeout=2)
                sleep(1)
                html_data = Selector(response_else.text)
                li_list = html_data.xpath('//ul[@class="J-all-rank team-rank-page"]/li[position()>1 and position()<17]')
                for li in li_list:
                        team = []
                        rank = li.xpath('./span[1]/text()').extract_first()
                        img_link = li.xpath('./img/@src').extract_first()
                        team_name = li.xpath('./h1/text()').extract_first()
                        data = li.xpath('./span[2]/text()').extract_first()

                        team.append(rank)
                        team.append(img_link)
                        team.append(team_name)
                        team.append(data)
                        dict_list.get(num).append(team)
                # 将数据以字典的方式存储，字典值的key用英文名
                dict_data[dict_replace.get(num)] = dict_list.get(num)

        '''


# def GetHtml(keyword):
#
#         user_Agent = [
#                 "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
#                 "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
#                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
#                 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
#                 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
#                 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
#                 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
#                 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
#                 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
#                 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
#                 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
#                 "NOKIA5700/ UCWEB7.0.2.37/28/999",
#                 "Openwave/ UCWEB7.0.2.37/28/999",
#                 "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
#         ]
#
#         # 虎扑网址
#
#         dict = {'team': 'https://m.hupu.com/nba/stats/teams',
#         'player': 'https://m.hupu.com/nba/stats/players',
#         'history': 'https://m.hupu.com/nba/stats/players/leaders',
#         'awards': 'https://m.hupu.com/nba/awards'}
#
#         response = requests.get(dict.get(keyword), headers={"User-Agent": random.choice(user_Agent)}, timeout=2)
#         return response.text


if __name__ == '__main__':
    team_data = GetData()
    with open(file='../NBA_spider/files/team_display.csv',mode='w',encoding='GBK',newline='') as file:
        writer = csv.writer(file)
        temp = ['Rank','TeamName','ShotAccuracy','TrebleAccuracy','PenaltyAccuracy','Rebounds',
                'Assist','Fault','Intercept','NutCap','Illegal','Scores']
        writer.writerow(temp)
        for team in team_data:
                temp = []
                for norm in team.values():
                        temp.append(norm)

                writer.writerow(temp)



