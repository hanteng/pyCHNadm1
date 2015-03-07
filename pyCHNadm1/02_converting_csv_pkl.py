# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("config.ini")
dir_src =   Config.get("Directory",'source')
dir_out =   Config.get("Directory",'outcome')
fn_suffix = Config.get("Filename",'suffix')
fn_datasrc= Config.get("Filename",'datasource')
fn_mapping =Config.get("Filename",'mapping')

dir_db =   Config.get("Directory",'database')
fn_db =     Config.get("Filename",'database')
fn_meta =   Config.get("Filename",'meta')
import os
import glob

list_src= glob.glob(os.path.join(dir_src,fn_datasrc))
list_indicators=[x.split("stats.gov.cn_")[1].split(".")[0] for x in list_src]
#>>> list_indicators
#['broadband_accounts', 'broadband_ports', 'domainnames', 'GDP', 'IPop', 'LP', 'webpages', 'websites']

import pandas as pd
dfCN=pd.read_pickle(os.path.join(dir_db,'.'.join([fn_mapping.split('.')[0], fn_suffix])))

dict_zhs_iso=dfCN.set_index("name_zhs")['ISO']

from StringIO import StringIO
import codecs

ldf={}
mdf={}
for i,ind in enumerate(list_indicators):
#i=0
#ind=list_indicators[i]
    fn=list_src[i]
    s = StringIO()
    meta={}
    with codecs.open(fn, 'r', encoding="gb2312") as f:
        read_data = f.readline()
        meta['db']=read_data.strip().split(u"：")[1]
        read_data = f.readline()
        meta['indicator']=read_data.strip().split(u"：")[1]

        read_rest = f.readlines()
        for n,line in enumerate(read_rest[:32]):
            s.write(line.encode("utf8"))
        meta['note'] =u"".join(read_rest[32:]).replace("\r\n", " ")


    mdf[ind]=meta
    s.seek(0)
    df = pd.read_csv(s, encoding="utf8", sep=",", na_values='',keep_default_na=False)    
    s.close()
    ## Cleaning the data and translating the names

    columns=[x.replace(u"\u5e74","") for x in df.columns] #u"\u5e74"  == u"年"
    columns=["geocode",]+[int(x) for x in columns[1:]]
    df.columns=columns

    df['geocode']=[dict_zhs_iso.get(x,None) for x in df.geocode]
    df=df.set_index('geocode')

    ## Saving to Pickle
    fn_output=os.path.join(dir_out,'.'.join([ind, fn_suffix]))
    df.to_pickle(fn_output)
    
    ## Storing together
    ldf[ind]=df
    print fn_output,

CNp   =pd.Panel(ldf)
CNmeta=pd.DataFrame(mdf).transpose()

## Saving to Pickle database

fn_output=os.path.join(dir_db,fn_db)
CNp.to_pickle(fn_output)
fn_output=os.path.join(dir_db,fn_meta)
CNmeta.to_pickle(fn_output)


'''
>>> CNmeta.index
Index([u'GDP', u'IPop', u'LP', u'broadband_accounts', u'broadband_ports', u'domainnames', u'webpages', u'websites'], dtype='object')
>>> CNmeta.columns
Index([u'db', u'indicator', u'note'], dtype='object')


>>> CNp.items
Index([u'GDP', u'IPop', u'LP', u'broadband_accounts', u'broadband_ports', u'domainnames', u'webpages', u'websites'], dtype='object')


>>> CNp['GDP',:,:]

>>> CNp['IPop',:,:2013]
'''
