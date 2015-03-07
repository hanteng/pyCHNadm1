# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import pandas as pd
import os

__all__ = ["CHNmapping", "CHNp", "CHNmeta", "CHNyearl", "CHNsize"]
__all__ = [str(u) for u in __all__]
_ROOT = os.path.abspath(os.path.dirname(__file__))


from os.path import basename, join, splitext

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("../config.ini")

CHNmapping=pd.read_pickle(os.path.join(_ROOT, "mapping.pkl")) #mapping['ISO2']['TWN']
CHNmapping=CHNmapping.set_index("geocode")
fn_output=os.path.join(_ROOT,"size.pkl")
CHNp=pd.read_pickle(fn_output)
fn_output=os.path.join(_ROOT,"meta.pkl")
CHNmeta=pd.read_pickle(fn_output)

CHNyearl={}  #year last for avialable data
CHNsize={} #size for last year
import numpy as np
for i in CHNp.items:
    #i='GDP'
    years_available=[x for x in CHNp[i].columns if type(x)==np.int64]
    years_available.sort(reverse=True)
    for y in years_available:
        #y=2013
        if len(CHNp[i][y])==len(CHNp[i][y].dropna()):
            break;
    CHNyearl[i]=y
    CHNsize[i]=CHNp[i][y]
    
CHNsize=pd.DataFrame(CHNsize)

''''


>>> pd.DataFrame(CHNsize)
              GDP  IPop     LP  broadband_accounts  broadband_ports  \
geocode                                                               
CN-11    19500.56  1556   2115               480.4           1186.8   
CN-12    14370.16   866   1472               188.4            353.9   
CN-13    28301.41  3389   7333              1031.6           2049.3   


#sizec=sizep.loc[["IPop","LP","PPPGDP"],:,2013].join(sizep.loc[["IH"],:,2012]).join(sizep.loc[["IPv4"],:,2015])

LP=sizec['LP']#or sizep['LP'][2013] or  sizep.loc['LP',:,2013]
PPPGDP=sizec['PPPGDP']#or sizep['PPPGDP'][2013]
IPop=sizec['IPop']#or sizep['IPop'][2013]
IH=sizec['IH']#or sizep['IH'][2012]
IPv4=sizec['IPv4']#or sizep['IPv4'][2015]

'''
