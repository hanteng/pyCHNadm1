# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。

## Loading datasets
import pyCHNadm1 as CHN

## Loading seaborn and other scientific analysis and visualization modules
## More: http://stanford.edu/~mwaskom/software/seaborn/tutorial/axis_grids.html
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib as mpl
import matplotlib.pyplot as plt

## Using seaborn style
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.6, )

## Checking the existing indicators available
indicators_all=CHN.CHNp.items
print indicators_all

## Slicing the data on the year of 2013 on selected indicators
df_2013=CHN.CHNp[['GDP','IPop','websites'],:,2013]

## Using 3ER to get the categorization of CHN regions
df_2013['3ER'] = [CHN.CHNmapping['3ER'][x] for x in df_2013.index]


g = sns.PairGrid(df_2013.reset_index(), hue="3ER")
g.map_diag(plt.hist)
g.map_offdiag(plt.scatter)  # sns.regplot (linear regression)
g.add_legend()              # Add legend
plt.show()


################################################
## Focusing on the relationship between the number of websites (y-axis) to GDP (x-axis)
df=df_2013[['GDP','websites']]
df=df.sort([u'websites'], ascending=False)
df.columns=['x:GDP','y: websites']

def labelix(i,x):
    if i<8:
        return CHN.CHNmapping['name_used'][x]+'\n'+CHN.CHNmapping['name_zhs_one'][x]
    else:
        return '\n'+CHN.CHNmapping['name_zhs_one'][x]

# Changeing indexes for labelling
#df.index=[CHN.CHNmapping['name_zhs_short'][x] for x in df.index] #short Chinese names
#df.index=[CHN.CHNmapping['name_zhs_one'][x]+'\n'+CHN.CHNmapping['name_used'][x] for x in df.index] #English names + name_zhs_one
df.index=[labelix(i,x) for i,x in enumerate(df.index)] #English names + name_zhs_one

from matplotlib.font_manager import FontProperties
ChineseFont = FontProperties('SimHei')

from matplotlib import cm
cmap = cm.get_cmap('Spectral')

fig, ax = plt.subplots()
df.plot('x:GDP', 'y: websites', kind='scatter', ax=ax, s=560, linewidth=0, 
        c=range(len(df)), colormap=cmap, alpha=0.25)

ax.set_xlabel("GDP (100 Million RMB) "+CHN.CHNmeta['indicator']['GDP'],fontproperties = ChineseFont,fontsize=18,)
ax.set_ylabel("Number of Websites (10 Thousand)"+CHN.CHNmeta['indicator']['websites'],fontproperties = ChineseFont,fontsize=18,)

for k, v in df.iterrows():
    ax.annotate(k, v,
                xytext=(-3,10), textcoords='offset points',
                horizontalalignment='center', verticalalignment='center',
                fontproperties = ChineseFont, fontsize=16, color='darkslategrey')

fig.delaxes(fig.axes[1])  #remove color bar

plt.show()
