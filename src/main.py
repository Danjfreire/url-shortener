from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel,HttpUrl 
from shortener import generate_random_code
from url_repo import UrlRepo

app = FastAPI()

class UrlDTO(BaseModel):
    url: HttpUrl

url_repo = UrlRepo()


@app.post("/shorten", status_code=status.HTTP_201_CREATED)
def shorten_url(body: UrlDTO):
    short_url = url_repo.find_by_original_url(body.url)

    if short_url:
        return short_url

    code = generate_random_code()
    if code is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="could not generate short code")

    short_url = url_repo.save_shortened_url(body.url, code)
    return short_url

@app.get("/shorten/{code}")
def get_original_url(code: str):
    short_url = url_repo.find_by_code(code)

    if short_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"url not found for code {code}")
    
    url_repo.increase_stats(code)
    return short_url

@app.put("/shorten/{code}")
def update_short_url(code: str, body: UrlDTO):
    short_url = url_repo.find_by_code(code)

    if short_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"url not found for code {code}")
    
    return url_repo.update_shortened_url(short_url, body.url)

@app.delete("/shorten/{code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_short_url(code: str):
    short_url = url_repo.find_by_code(code)

    if short_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"url not found for code {code}")
    
    url_repo.delete_shortened_url(short_url)
    
@app.get("/shorte/{code}/stats")
def get_code_stats(code: str):
    short_url = url_repo.find_by_code(code)

    if short_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"url not found for code {code}")
    
    return url_repo.find_shortened_url_stats(short_url) 
    