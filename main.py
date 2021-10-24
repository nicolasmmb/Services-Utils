import blurhash
import requests
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


class BlurhashModel(BaseModel):
    url: str
    timeout: Optional[int] = 15
    x_comp: Optional[int] = 3
    y_comp: Optional[int] = 2


app = FastAPI()


@app.post("/blurhash")
async def generate_blurhash(request: BlurhashModel):
    try:
        response = requests.get(request.url, stream=True, timeout=request.timeout)
        bh = blurhash.encode(response.raw, x_components=request.x_comp, y_components=request.y_comp)
        print('Blurhash: ' + bh)

        if response.status_code == 200:
            return {
                'error': False,
                'response': bh,
                'log': None
            }
        else:
            return {
                'error': True,
                'response': None,
                'log': f'Error: {response.request}',
            }
    except Exception as excp:
        return {
            'error': True,
            'response': None,
            'log': str(excp),
        }


@app.get("/")
def root():
    return {
        'error': None,
        'response': 'Hello, Utils Directory'
    }
