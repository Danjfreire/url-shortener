from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel,HttpUrl 
from shortener import generate_random_code
from url_repo import save_shortened_url, find_short_url

app = FastAPI()

class UrlDTO(BaseModel):
    url: HttpUrl


@app.post("/shorten", status_code=status.HTTP_201_CREATED)
def shorten_url(dto: UrlDTO):
    short_url = find_short_url(dto.url)

    if short_url:
        return short_url

    code = generate_random_code()
    if code is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="could not generate short code")

    short_url = save_shortened_url(dto.url, code)
    return short_url

