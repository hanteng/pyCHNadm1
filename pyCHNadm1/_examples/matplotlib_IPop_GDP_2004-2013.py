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
mpl.rcParams["figure.subplot.bottom"] = 0.14

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
ChineseFont = FontProperties('SimHei')

from matplotlib import cm
cmap = cm.get_cmap('Spectral')

import statsmodels.api as sm

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
df_regression={}
for y in range(2004,2013+1):#2004
    df_[y]=CHN.CHNp[['GDP','IPop'],:,y]

    ################################################
    ## Focusing on the relationship between the number of IPop (y-axis) to GDP (x-axis)
    df=df_[y][['GDP','IPop']]
    df=df.sort([u'IPop'], ascending=False)
    df.columns=['x:GDP','y:IPop']

    # Changeing indexes for labelling
    #df.index=[CHN.CHNmapping['name_zhs_short'][x] for x in df.index] #short Chinese names
    #df.index=[CHN.CHNmapping['name_zhs_one'][x]+'\n'+CHN.CHNmapping['name_used'][x] for x in df.index] #English names + name_zhs_one
    df.index=[labelix(i,x) for i,x in enumerate(df.index)] #English names + name_zhs_one

    mod=sm.OLS(endog=df['y:IPop'], exog=sm.add_constant(df['x:GDP']))
    res=mod.fit()
    slope, intercept, rsquared=res.params[1], res.params[0], res.rsquared
    lr={"slope":slope,"intercept":intercept,"rsquared":rsquared}
    df_regression[y]=lr
    y_est=res.predict([1,0],[1,70000])
    
    
    fig, ax = plt.subplots()
    df.plot('x:GDP', 'y:IPop', kind='scatter', ax=ax, s=560, linewidth=0, 
            c=range(len(df)), colormap=cmap, alpha=0.25)

    #plotting the regression line, colored in red
    pnt=np.array([0,70000])
    plt.plot(pnt, slope*pnt+intercept, 'r:', alpha=0.3)  # Add the regression line, colored in red

    ax.set_xlabel("GDP (100 Million RMB) "+CHN.CHNmeta['indicator']['GDP'],fontproperties = ChineseFont,fontsize=15,)
    ax.set_ylabel("Number of Internet users (10 Thousand)\n"+CHN.CHNmeta['indicator']['IPop'],fontproperties = ChineseFont,fontsize=15,)

    ax.set_ylim(bottom=-5,top=8000)
    ax.set_xlim(left=-1000,right=70000)


    fig.suptitle('Year {0}'.format(y), fontsize=20)
    for k, v in df.iterrows():
        ax.annotate(k, v,
                    xytext=(-7,0), textcoords='offset points',
                    horizontalalignment='left', verticalalignment='center',
                    fontproperties = ChineseFont, fontsize=16, color='darkslategrey')

    fig.delaxes(fig.axes[1])  #remove color bar

    plt.savefig('CHN_IPop_GDP.png_%s.png' % (y))
    #plt.show()


df_reg=pd.DataFrame(df_regression)
df_reg.transpose()[['slope','intercept','rsquared']].to_csv("IPop_GDP_lr.tsv", sep="\t", keep_default_na=False, na_values=[""], float_format='%.4f')
