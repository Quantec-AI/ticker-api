from fastapi import FastAPI, Response, Query
import json
from generic import *

import uvicorn

title = "Ticker Info REST API"

# Initialize FastAPI app
app = FastAPI(
    title = title,
    description= "REST API for Integrated Ticker Info",
    version="0.0.1",
)


# On startup
@app.on_event('startup')
async def startup_event():
    global data, content_type
    data = load_data()
    content_type = f'application/json;charset=utf-8'


# Front API
@app.get('/')
async def welcome():
    content_dict = {'msg':f'Welcome to {title}'}
    content = json.dumps(content_dict,ensure_ascii=False)

    return Response(content=content, media_type=content_type)


## GET by Single Ticker only
# Edge-case (No symbol entered)
@app.get('/symbol/')
async def no_symbol():
    content_dict = {'error':'Enter company ticker'}
    content = json.dumps(content_dict,ensure_ascii=False)

    return Response(content=content, media_type=content_type)
    

# Single symbol entered
@app.get('/symbol/{symbol}')
async def get_ticker(symbol: str):
    if symbol:
        if isinstance(symbol,str):
            symbol = [symbol]
        output_data = data.loc[data.symbol.isin(symbol),['region','symbol','name','valid']][:10]

        if len(output_data)>0:
            content_dict = output_data.to_dict(orient='records')

        else:
            content_dict = {'error':f'symbol: {symbol} not found'}
    else:
        content_dict = {'error':f'symbol: {symbol} not found'}

    content = json.dumps(content_dict,ensure_ascii=False)

    return Response(content=content, media_type=content_type)
    

## GET by Single Name only
# Edge-case (No name entered)
@app.get('/name/')
async def no_name():
    content_dict = {'error':'Enter company name'}
    content = json.dumps(content_dict,ensure_ascii=False)

    return Response(content=content, media_type=content_type)
    

# Single name entered
@app.get('/name/{name}')
async def get_ticker(name: str):
    if name:
        output_data = data.loc[data.name.str.contains(name),['region','symbol','name','valid']][:10]

        if len(output_data)>0:
            content_dict = output_data.to_dict(orient='records')

        else:
            content_dict = {'error':f'name: {name} not found'}
    else:
        content_dict = {'error':f'name: {name} not found'}

    content = json.dumps(content_dict,ensure_ascii=False)

    return Response(content=content, media_type=content_type)


# GET by Ticker / Name Mix
@app.get('/tickers/')
async def get_tickers(symbol: Union[List[str], None] = Query(default=None), name: Union[List[str], None] = Query(default=None)):
    # Edge-case (No symbol entered)
    if not symbol and not name:
        content_dict = {'error':'Enter company ticker or name'}
        content = json.dumps(content_dict,ensure_ascii=False)

        return Response(content=content, media_type=content_type)
    
    else:
        query = {'name':[],'symbol':[]}
        if symbol:
            query['symbol'] = symbol
        if name:
            query['name'] = name

        ## Symbol
        symbol_data = data.loc[(data.symbol.isin(query['symbol']))]

        ## Name
        if len(query['name'])>0:
            name_data = pd.concat([data.loc[data.name.str.contains(group)] for group in query['name']])
        else:
            name_data = pd.DataFrame()

        # All Data 
        output_data = pd.concat([symbol_data,name_data]).drop_duplicates()[:10]

        if len(output_data)>0:
            output_data = output_data[['region','symbol','name','valid']]
            content_dict = output_data.to_dict(orient='records')

        else:
            content_dict = {'error':f': {query} not found'}

        content = json.dumps(content_dict,ensure_ascii=False)

        return Response(content=content, media_type=content_type)