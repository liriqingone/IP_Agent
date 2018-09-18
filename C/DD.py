# coding: utf-8


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymssql
from io import StringIO

dfGSE = pd.read_csv('e:/test.csv')
print dfGSE.head()

##OrigYear
dfSumm = dfGSE[['origyear', 'histdate', 'wac', 'fico', 'vsmm', 'curbal']] \
    .assign(wac=lambda row: 0.5 * np.round(row.wac / 0.5)
            , fico=lambda row: 100 * np.round(row.fico / 100)
            , vsmm=lambda row: row.vsmm * row.curbal
            ) \
    .groupby(['origyear', 'histdate'], as_index=False) \
    .agg({'vsmm': 'sum'
             , 'curbal': 'sum'}) \
    .assign(vsmm=lambda row: row.vsmm / row.curbal
            , histdate=lambda row: pd.to_datetime(row.histdate))

sns.FacetGrid(data=dfSumm.query('origyear > 2009'), col='origyear', col_wrap=3,
              despine=False, height=3).map_dataframe(plt.plot, 'histdate', 'vsmm')

fig = plt.gcf()

plt.show()

fig.savefig('E:/aa.png', dpi=100)

