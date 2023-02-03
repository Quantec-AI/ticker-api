from fastapi import FastAPI, Response
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

# Edge-case (No symbol entered)
@app.get('/tickers/')
async def no_tickers():
    content_dict = {'error':'Enter symbol name'}
    content = json.dumps(content_dict,ensure_ascii=False)

    return Response(content=content, media_type=content_type)

# GET Ticker
@app.get('/tickers/{symbol}')
async def get_tickers(symbol: str):
    if symbol:
        if isinstance(symbol,str):
            symbol = [symbol]
        
        output_data = data.loc[data.symbol.isin(symbol),['region','symbol','name','valid']]
        # print(output_data.to_dict(orient='records'))
        
        if len(output_data)>0:
            content_dict = output_data.to_dict(orient='records')
        
        else:
            content_dict = {'error':f'symbol: {symbol} not found'}
    else:
        content_dict = {'error':f'symbol: {symbol} not found'}

    content = json.dumps(content_dict,ensure_ascii=False)

    return Response(content=content, media_type=content_type)
