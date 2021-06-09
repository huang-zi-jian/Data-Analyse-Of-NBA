import pandas

# python版本原因这里需要指定engine为openpyxl
img = pandas.read_excel('img.xlsx',sheet_name='Sheet1',engine='openpyxl',index_col=0)
img.rename(columns={'src':'img'},inplace=True)
img.to_csv('team_img.csv',encoding='GBK')