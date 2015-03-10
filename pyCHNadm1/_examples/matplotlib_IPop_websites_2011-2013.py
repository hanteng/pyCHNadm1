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

# Customizing figures
import matplotlib as mpl

mpl.rcParams["axes.labelsize"] = 18.0
mpl.rcParams["axes.grid"] = True

mpl.rcParams["font.size"] = 14.0#
mpl.rcParams["axes.edgecolor"] = "black" 
mpl.rcParams["axes.labelcolor"] = "black"
mpl.rcParams["grid.color"] = "grey" # or  whatever you want

mpl.rcParams["figure.subplot.wspace"] = 0.4
mpl.rcParams["figure.figsize"] = [8, 6]
mpl.rcParams["figure.subplot.left"] = 0.15
mpl.rcParams["figure.subplot.right"] = 0.99
mpl.rcParams["figure.subplot.bottom"] = 0.18

import matplotlib.pyplot as plt

## Using seaborn style
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.2, )

## Defining labels from CHN.CHNmapping
def labelix(i,x):
    if i<8:
        return CHN.CHNmapping['name_zhs_one'][x]+CHN.CHNmapping['name_used'][x]
    else:
        return CHN.CHNmapping['name_zhs_one'][x]


## Slicing the data on the years of 2011 to 2013 on selected indicators
df_={}
for y in range(2011,2013+1):
    df_[y]=CHN.CHNp[['websites','IPop'],:,y]

    ################################################
    ## Focusing on the relationship between the number of IPop (y-axis) to websites (x-axis)
    df=df_[y][['IPop', 'websites']]
    df=df.sort([u'websites'], ascending=False)
    df.columns=['x:IPop','y:websites']

    # Changeing indexes for labelling
    #df.index=[CHN.CHNmapping['name_zhs_short'][x] for x in df.index] #short Chinese names
    #df.index=[CHN.CHNmapping['name_zhs_one'][x]+'\n'+CHN.CHNmapping['name_used'][x] for x in df.index] #English names + name_zhs_one
    df.index=[labelix(i,x) for i,x in enumerate(df.index)] #English names + name_zhs_one

    from matplotlib.font_manager import FontProperties
    ChineseFont = FontProperties('SimHei')

    from matplotlib import cm
    cmap = cm.get_cmap('Spectral')

    fig, ax = plt.subplots()
    df.plot('x:IPop', 'y:websites', kind='scatter', ax=ax, s=560, linewidth=0, 
            c=range(len(df)), colormap=cmap, alpha=0.25)

    ax.set_xlabel("Number of Internet users (10 Thousand)\n"+CHN.CHNmeta['indicator']['IPop'],fontproperties = ChineseFont,fontsize=15,)
    ax.set_ylabel("Number of websites (10 Thousand)\n"+CHN.CHNmeta['indicator']['websites'],fontproperties = ChineseFont,fontsize=15,)

    ax.set_xlim(left=-5,right=8000)
    ax.set_ylim(bottom=-2,top=60)

    fig.suptitle('Year {0}'.format(y), fontsize=20)
    for k, v in df.iterrows():
        ax.annotate(k, v,
                    xytext=(-7,0), textcoords='offset points',
                    horizontalalignment='left', verticalalignment='center',
                    fontproperties = ChineseFont, fontsize=16, color='darkslategrey')

    fig.delaxes(fig.axes[1])  #remove color bar

    plt.savefig('CHN_websites_IPop.png_%s.png' % (y))
    #plt.show()
