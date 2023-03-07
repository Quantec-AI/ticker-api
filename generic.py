import pandas as pd
import os
import re
from pydantic import BaseModel
from typing import Optional, Union

# Ticker Data Class Definition
# symbol is required
class TickerData(BaseModel):
    region: Union[list[str], None]           # Region (e.g., US)
    symbol: Union[list[str], None]           # Ticker (e.g., AAPL)
    name: Union[list[str], None]           # Region (e.g., US)
    listed: Union[list[str], None]           # Ticker (e.g., AAPL)
    
    # name: Optional[Union[list[str], None]]   # Name (e.g., Apple Inc.)
    # listed: Optional[Union[list[str], None]] # Exchange (e.g., NASDAQ)


# Load data
def load_data(dir='data',encoding='utf-8-sig'):
    paths = {'csv':map(lambda x:os.path.join(os.path.join('.',dir),x.name),filter(lambda x:x.name.find('csv') != -1,os.scandir(os.path.join('.',dir)))),
    'xlsx':map(lambda x:os.path.join(os.path.join('.',dir),x.name),filter(lambda x:x.name.find('xlsx') != -1,os.scandir(os.path.join('.',dir))))}
    # map(lambda x:os.path.join(os.path.join('.',dir),x.name),os.scandir(os.path.join('.',dir)))
    columns = ['region','symbol','name','listed']
    raw_data = pd.concat(map(lambda x:pd.read_csv(x,encoding=encoding,dtype={'symbol':object}),paths['csv'])).drop_duplicates('symbol').reset_index(drop=True)
    raw_data = raw_data[columns]
    raw_data['symbol'] = raw_data[['region','symbol']].apply(lambda x:str(x[1][1:]) if x[0] == 'KR' else x[1].replace('-','.'),axis=1)

    ref_data = pd.DataFrame()
    for file_name in paths['xlsx']:
        df = pd.read_excel(file_name)
        if re.search(r'^[ㄱ-ㅎ가-힣]',df[df.columns[3]][0]):
            df['region'] = 'KR'
            df['symbol'] = df[df.columns[1]].apply(lambda x:f'{x[3:9]}')
        else:
            df['region'] = 'US'
            df['symbol'] = df[df.columns[3]].apply(lambda x:x[:x.rfind('.')])
        df = df[['region','symbol']]
        ref_data = pd.concat([ref_data,df])

    data = pd.merge(raw_data,ref_data,how='outer',on=['region','symbol'],indicator=True)
    data['valid'] = data['_merge'].apply(lambda x:'OK' if x in ('both','right_only') else 'Not Available')
    data.loc[data['_merge']=='right_only','name'] = 'Placeholder'

    return data