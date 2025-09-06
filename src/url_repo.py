import datetime
from typing import Dict
from pydantic import BaseModel, HttpUrl

class ShortenedUrl(BaseModel):
    url: HttpUrl 
    code: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class ShortnedUrlWithAccess(ShortenedUrl):
    access_count: int

class UrlRepo:
    def __init__(self):
        self.url_db: Dict[str, ShortenedUrl] = {}
        self.code_db: Dict[str, ShortenedUrl] = {}
        self.stats_db: Dict[str, int] = {}

    def find_by_original_url(self, url: str) -> ShortenedUrl | None:
        if url in self.url_db: 
            return self.url_db[url]
        return None

    def find_by_code(self, code : str) -> ShortenedUrl | None:
        if code in self.code_db:
            return self.code_db[code]
        return None

    def save_shortened_url(self, url: str, code: str) -> ShortenedUrl:
        now = datetime.datetime.now()
        short: ShortenedUrl = ShortenedUrl(url=url, code=code, created_at=now, updated_at=now) 
        self.url_db[url] = short
        self.code_db[code] = short
        return short 

    def update_shortened_url(self, shortened_url: ShortenedUrl, new_url: HttpUrl):
        now = datetime.datetime.now()
        old_url = shortened_url.url

        shortened_url.url = new_url
        shortened_url.updated_at = now

        self.url_db.pop(old_url)
        self.url_db[new_url] = shortened_url
        self.code_db[shortened_url.code] = shortened_url

        return shortened_url

    def delete_shortened_url(self,short_url: ShortenedUrl):
        self.url_db.pop(short_url.url)
        self.code_db.pop(short_url.code)

    def increase_stats(self, code: str, increase: int = 1):
        if not code in self.stats_db:
            self.stats_db[code] = 0
        
        self.stats_db[code] += increase

    def find_shortened_url_stats(self,short_url: ShortenedUrl):
        access_count = self.stats_db.get(short_url.code, 0)
        return ShortnedUrlWithAccess(
            url=short_url.url,
            code=short_url.code, 
            created_at=short_url.created_at,
            updated_at=short_url.updated_at, 
            access_count=access_count)



