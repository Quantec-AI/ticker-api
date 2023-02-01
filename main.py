from fastapi import FastAPI
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
    return {'msg':f'Welcome to {title}'}

# Edge-case (No symbol entered)
@app.get('/tickers/')
async def no_tickers():
    return {'error':'Enter symbol name'}

# GET Ticker
@app.get('/tickers/{symbol}')
async def get_tickers(symbol: str):
    if symbol:
        if isinstance(symbol,str):
            symbol = [symbol]
        
        output_data = data.loc[data.symbol.isin(symbol),['region','symbol','name','valid']]
        print(output_data.to_dict(orient='records'))
        
        if len(output_data)>0:
            return output_data.to_dict(orient='records')
        
        else:
            return {'error':f'symbol: {symbol} not found'}
    else:
        return {'error':f'symbol: {symbol} not found'}
