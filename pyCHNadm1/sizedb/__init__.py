# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import pandas as pd
import os

__all__ = ["LP","PPPGDP","IPop","sizec","sizep", "meta", "description", "mapping"]
__all__ = [str(u) for u in __all__]
_ROOT = os.path.abspath(os.path.dirname(__file__))


from os.path import basename, join, splitext
sizep=pd.read_pickle(os.path.join(_ROOT, "size.pkl"))
sizec=sizep.loc[["IPop","LP","PPPGDP"],:,2013].join(sizep.loc[["IH"],:,2012]).join(sizep.loc[["IPv4"],:,2015])
mapping=pd.read_pickle(os.path.join(_ROOT, "mapping.pkl")) #mapping['ISO2']['TWN']

LP=sizec['LP']#or sizep['LP'][2013] or  sizep.loc['LP',:,2013]
PPPGDP=sizec['PPPGDP']#or sizep['PPPGDP'][2013]
IPop=sizec['IPop']#or sizep['IPop'][2013]
IH=sizec['IH']#or sizep['IH'][2012]
IPv4=sizec['IPv4']#or sizep['IPv4'][2015]

meta={'LP': "Population in 2013 (IMF WEO)",\
      'PPPGDP': "Economy Size in 2013 (IMF WEO)",\
      'IPop': "Internet Population in 2013 (ITU)",\
      'IH': "Internet Hosts in 2012 (CIA)",\
      'IPv4': "Internet Addresses in 2015 (CIPB)", }

description={'LP': "Population in 2013 (in millions) from IMF World Economic Outlook (WEO) database, October 2014",\
      'PPPGDP': "Economy Size in 2013 (in billions) from IMF World Economic Outlook (WEO) database, October 2014",\
      'IPop': "Internet Population in 2013 (in millions) derived from ITU 2014 report and IMF World Economic Outlook (WEO) database, October 2014",\
      'IH': "Internet Hosts in 2012 (in millions) from CIA the World Factbook",\
      'IPv4': "Internet Addresses in 2015 (in millions) from CIPB", }


