from typing import List, Optional

from pydantic import BaseModel

# Schema Response Feature 1: Hasil Ringkasan CV
class CVSummaryResponse(BaseModel):
    name: str
    location: str
    work_experience_summary: str
# Schema Feature 2: News Search
class Article(BaseModel):
    title: str
    summary: str
    url: str
    published_date: Optional[str] = None

class NewsSearchResponse(BaseModel):
    query: str
    articles: List[Article]