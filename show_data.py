
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymssql
import re
# In[8]:

try:
    con = pymssql.connect(host='welldatadb.c9rukeih98lt.us-west-1.rds.amazonaws.com',user='welltitled',password='Welltitled888', database='WellDataDB',charset="utf8")
    sql = "select d.id,d.date,d.is_download,d.case_id from welldata_project p left join  welldata_case c on p.id=c.project_id left join dbo.welldata_downloadfile d on c.name_en=d.case_id where p.name_en='USBank'"
    dfGSE = pd.read_sql(con=con, sql=sql)
    print dfGSE.head()
    sns.catplot(x="case_id", kind="count", palette="ch:.25", data=dfGSE)
    print(plt.show())
except pymssql.Error as e:
    print e

print 0.392157*2.750408e+08
# # `OrigYear` and `wac`

# In[40]:


# get_ipython().run_cell_magic(u'time', u'', u"\ndfSumm_wac = \\\ndfGSE[['origyear', 'histdate', 'wac', 'fico', 'vsmm', 'curbal']] \\\n.assign(wac = lambda row: 0.5 * np.round(row.wac / 0.5) \\\n       ,fico = lambda row: 100 * np.round(row.fico / 100) \\\n       ,vsmm = lambda row: row.vsmm * row.curbal \\\n       ) \\\n.groupby(['origyear', 'histdate', 'wac'], as_index = False) \\\n.agg({'vsmm': 'sum' \\\n     , 'curbal': 'sum'}) \\\n.assign(vsmm = lambda row: row.vsmm / row.curbal \\\n       ,histdate = lambda row: pd.to_datetime(row.histdate)) \\")
#
#
# # In[44]:
#
#
# sns.FacetGrid(data = dfSumm_wac.query('origyear > 2009 & wac > 3 & wac < 6.5'), col = 'origyear'
#               , row = 'wac',
#              despine = False, height = 3) \
# .map_dataframe(plt.plot, 'histdate', 'vsmm')
#
#
# # # `Origyear` and `wac` and `fico`
# #
# # 下边 `arrWAC`和 `arrFICO` 是用户的选择。格式是：
# #
# # `arrWAC = np.array([最小值,最大值,宽度值])
# #
# # 这个的目的是尽量保留数据， 把筛选留到最后
#
# # In[153]:
#
#
# get_ipython().run_cell_magic(u'time', u'', u"\narrWAC = np.array([3.5, 6.5, 0.5])\narrFICO = np.array([500, 800, 100])\n\ndfSumm_wac_fico = \\\ndfGSE[['origyear', 'histdate', 'wac', 'fico', 'vsmm', 'curbal', 'cnt']] \\\n.assign(wac = lambda row: arrWAC[2] * \\\n        np.round( \\\n                 np.where(row.wac < arrWAC[0] \\\n                          , arrWAC[0]\n                          ,np.where(row.wac > arrWAC[1]\n                                   , arrWAC[1]\n                                   , row.wac) \\\n                         ) \\\n                 / arrWAC[2]) \\\n       ,fico = lambda row: arrFICO[2] * \\\n        np.round( \\\n                 np.where(row.fico < arrFICO[0] \\\n                          , arrFICO[0] \\\n                          , np.where(row.fico > arrFICO[1] \\\n                                   , arrFICO[1] \\\n                                   , row.fico))\\\n                 / arrFICO[2]) \\\n       ,vsmm = lambda row: row.vsmm * row.curbal \\\n       ) \\\n.groupby(['origyear', 'histdate', 'wac', 'fico'], as_index = False) \\\n.agg({'vsmm': 'sum' \\\n     , 'curbal': 'sum'\\\n     , 'cnt': 'sum'}) \\\n.assign(vsmm = lambda row: row.vsmm / row.curbal \\\n       ,histdate = lambda row: pd.to_datetime(row.histdate)) \\")
#
#
# # In[154]:
#
#
# dfSumm_wac_fico_orig = dfSumm_wac_fico[['origyear', 'histdate', 'wac', 'fico', 'curbal', 'cnt']] .groupby(['origyear', 'histdate', 'wac', 'fico'], as_index = False) .agg('sum') .groupby(['origyear', 'wac', 'fico'], as_index = False) .agg('max') .rename(index = str, columns = {'curbal': 'curbal_orig', 'cnt': 'cnt_orig'}) .drop(['histdate'], axis = 1)
#
#
#
# # In[155]:
#
#
# dfSumm_wac_fico = dfSumm_wac_fico .merge(dfSumm_wac_fico_orig
#        , left_on = ['origyear', 'wac', 'fico']
#        , right_on = ['origyear', 'wac', 'fico']) \
#
#
# # In[161]:
#
#
# sns.FacetGrid(data = dfSumm_wac_fico               .query('origyear > 2009 & origyear < 2014 & cnt_orig > 20000')
#               , col = 'origyear'
#               , row = 'wac', hue = 'fico'
#               , sharey = False
#              ,despine = False, height = 3) \
# .map_dataframe(sns.lineplot, 'histdate', 'vsmm', lw = 3)

