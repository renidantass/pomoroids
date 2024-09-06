from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from json import loads

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

