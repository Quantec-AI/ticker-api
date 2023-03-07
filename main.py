from fastapi import FastAPI, Response, Query
from functools import reduce
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

# GET by Ticker
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
            query['symbol'] = symbol[:10]
        if name:
            query['name'] = name[:10]
        # output_data = data.loc[(data.symbol.isin(query['symbol'])) | (data.name.isin(query['name'])),['region','symbol','name','valid']]
        output_data = data.loc[(data.symbol.isin(query['symbol']))]

        for group in query['name']:
            df = data.copy()
            dfs = map(lambda q:df.loc[df.name.str.contains(q)],group)
            df = reduce(lambda left,right: pd.merge(left,right), dfs)
            output_data = pd.concat([output_data,df])

        if len(output_data)>0:
            output_data = output_data[['region','symbol','name','valid']]
            content_dict = output_data.to_dict(orient='records')

        else:
            content_dict = {'error':f'symbol: {symbol} not found'}

        content = json.dumps(content_dict,ensure_ascii=False)

        return Response(content=content, media_type=content_type)
    

# # GET by Ticker
# @app.get('/tickers/')
# async def get_by_name(name: Union[list[str], None] = Query(default=None)):
#     # Edge-case (No symbol entered)
#     if not name:
#         content_dict = {'error':'Enter company name'}
#         content = json.dumps(content_dict,ensure_ascii=False)

#         return Response(content=content, media_type=content_type)
    
#     else:
#         name = name[:10]
#         output_data = data.loc[data.name.isin(name),['region','symbol','name','valid']]
#         # print(output_data.to_dict(orient='records'))

#         if len(output_data)>0:
#             content_dict = output_data.to_dict(orient='records')

#         else:
#             content_dict = {'error':f'name: {name} not found'}

#         content = json.dumps(content_dict,ensure_ascii=False)

#         return Response(content=content, media_type=content_type)
    

