from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel,HttpUrl 
from shortener import generate_random_code
from url_repo import save_shortened_url, find_by_original_url, find_by_code, update_shortened_url, delete_shortened_url 

app = FastAPI()

class UrlDTO(BaseModel):
    url: HttpUrl


@app.post("/shorten", status_code=status.HTTP_201_CREATED)
def shorten_url(body: UrlDTO):
    short_url = find_by_original_url(body.url)

    if short_url:
        return short_url

    code = generate_random_code()
    if code is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="could not generate short code")

    short_url = save_shortened_url(body.url, code)
    return short_url

@app.get("/shorten/{code}")
def get_original_url(code: str):
    short_url = find_by_code(code)

    if short_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"url not found for code {code}")
    
    return short_url

@app.put("/shorten/{code}")
def update_short_url(code: str, body: UrlDTO):
    short_url = find_by_code(code)

    if short_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"url not found for code {code}")
    
    return update_shortened_url(short_url, body.url)

@app.delete("/shorten/{code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_short_url(code: str):
    short_url = find_by_code(code)

    if short_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"url not found for code {code}")
    
    delete_shortened_url(short_url)
    
