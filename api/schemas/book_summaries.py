from pydantic import BaseModel
from typing import Optional


class BookSummaryBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    summary: Optional[str] = None


class BookSummaryUpdate(BookSummaryBase):
    pass


class BookSummaryInDB(BaseModel):
    summary_id: int
    title: str
    author: str
    genre: Optional[str] = None
    summary: Optional[str] = None
    file_url: Optional[str] = None
    uploaded_by: Optional[int] = None

    class Config:
        from_attributes = True
