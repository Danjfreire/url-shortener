import datetime
from typing import Dict
from pydantic import BaseModel, HttpUrl

class ShortenedUrl(BaseModel):
    url: HttpUrl 
    code: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

url_db: Dict[str, ShortenedUrl ] = {}
code_db: Dict[str, ShortenedUrl] = {}


def find_by_original_url(url: str) -> ShortenedUrl | None:
    if url in url_db: 
        return url_db[url]
    return None

def find_by_code(code : str) -> ShortenedUrl | None:
    if code in code_db:
        return code_db[code]
    return None

def save_shortened_url(url: str, code: str) -> ShortenedUrl:
    now = datetime.datetime.now()
    short: ShortenedUrl = ShortenedUrl(url=url, code=code, created_at=now, updated_at=now) 
    url_db[url] = short
    code_db[code] = short
    return short 

def update_shortened_url(shortened_url: ShortenedUrl, new_url: HttpUrl):
    now = datetime.datetime.now()
    old_url = shortened_url.url

    shortened_url.url = new_url
    shortened_url.updated_at = now

    url_db.pop(old_url)
    url_db[new_url] = shortened_url
    code_db[shortened_url.code] = shortened_url

    return shortened_url

def delete_shortened_url(short_url: ShortenedUrl):
    url_db.pop(short_url.url)
    code_db.pop(short_url.code)


