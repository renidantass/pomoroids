from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from json import loads
from state import AppStates, GLOBAL_STATE

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/settings")
def read_settings():
    with open('settings.json') as f:
        data = ''.join(f.readlines())
        return loads(data)

@app.get('/status')
def read_status():
    print(GLOBAL_STATE.current_state)

    if GLOBAL_STATE.current_state == AppStates.IN_SESSION.value:
        return JSONResponse(content={ 'status': True })

    return JSONResponse(content={ 'status': False })
