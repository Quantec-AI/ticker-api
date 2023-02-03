from fastapi import FastAPI
from fastapi.responses import JSONResponse
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
    global data
    data = load_data()

# Front API
@app.get('/')
async def welcome():
    content = {'msg':f'Welcome to {title}'}
    headers = {'charset':'utf-8-sig'}
    return JSONResponse(content=content, headers=headers)
    # return {'msg':f'Welcome to {title}'}

# Edge-case (No symbol entered)
@app.get('/tickers/')
async def no_tickers():
    content = {'error':'Enter symbol name'}
    headers = {'charset':'utf-8-sig'}
    return JSONResponse(content=content, headers=headers)

# GET Ticker
@app.get('/tickers/{symbol}')
async def get_tickers(symbol: str):
    if symbol:
        if isinstance(symbol,str):
            symbol = [symbol]
        
        output_data = data.loc[data.symbol.isin(symbol),['region','symbol','name','valid']]
        # print(output_data.to_dict(orient='records'))
        
        if len(output_data)>0:
            content = output_data.to_dict(orient='records')
        
        else:
            content = {'error':f'symbol: {symbol} not found'}
    else:
        content = {'error':f'symbol: {symbol} not found'}

    headers = {'charset':'utf-8-sig'}

    return JSONResponse(content=content, headers=headers)