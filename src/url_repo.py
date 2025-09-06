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


def find_short_url(url: str) -> ShortenedUrl | None:
    if url in url_db: 
        return url_db[url]
    
    return None

def save_shortened_url(url: str, code: str) -> ShortenedUrl:
    now = datetime.datetime.now()
    short: ShortenedUrl = ShortenedUrl(url=url, code=code, created_at=now, updated_at=now) 
    url_db[url] = short
    code_db[code] = short
    return short 


def has_shortened_code(code:str) -> bool:
    return code in code_db
