import blurhash
import requests
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


class BlurhashModel(BaseModel):
    url: str
    timeout: Optional[int] = 15
    x_comp: Optional[int] = 5
    y_comp: Optional[int] = 4


app = FastAPI()


@app.post("/blurhash")
async def generate_blurhash(request: BlurhashModel):
    try:
        response = requests.get(request.url, stream=True, timeout=request.timeout)
        print('Headers:' + str(response.headers))
        print('Status Code: ' + str(response.status_code))
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
    except Exception as e:
        return {
            'error': True,
            'response': None,
            'log': str(e),

        }
    return {
        'error': True,
        'response': None,
        'log': 'Error: Unknown'
    }


@app.get("/")
def root():
    return {
        'error': None,
        'response': 'Hello, Utils Directory'
    }


# image_response = requests.get('https://cdn.pixabay.com/photo/2014/01/22/19/44/flower-field-250016_960_720.jpg', stream=True)
# hash = blurhash.encode(image_response.raw, x_components=5, y_components=4)
# print(hash)
