from fastapi import FastAPI
from json import loads

app = FastAPI()


@app.get("/settings")
def read_settings():
    with open('settings.json') as f:
        data = ''.join(f.readlines())
        return loads(data)

