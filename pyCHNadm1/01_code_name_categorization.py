# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("config.ini")
dir_src =   Config.get("Directory",'source')
dir_out =   Config.get("Directory",'outcome')
fn_suffix = Config.get("Filename",'suffix')
fn_mapping =Config.get("Filename",'mapping')
u_mapping = Config.get("URL",'mapping')

dir_db =   Config.get("Directory",'database')

import os
import pandas as pd

try:
    df = pd.read_csv(os.path.join(dir_src,fn_mapping), encoding="utf8", sep=",", na_values='',keep_default_na=False)    
except:
    #downloading from Google Spreadsheet
    import requests
    from StringIO import StringIO 
    r = requests.get(u_mapping)
    data = r.content
    df = pd.read_csv(StringIO(data))
    df.to_csv(os.path.join(dir_src,fn_mapping), encoding="utf8", sep=",")

#e.g.
#df[df['8EZ']=='8EZ_DB']

## Saving to Pickle
df.to_pickle(os.path.join(dir_db,'.'.join([fn_mapping.split('.')[0], fn_suffix])))

