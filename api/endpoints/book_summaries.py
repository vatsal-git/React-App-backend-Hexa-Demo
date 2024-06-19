from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from api.models.book_summary import BookSummary
from api.models.user import User
from api.schemas.book_summaries import BookSummaryBase, BookSummaryInDB, BookSummaryUpdate
from core.database import get_db
from core.security import get_current_user
from typing import Optional

router = APIRouter()


@router.get("/", response_model=list[BookSummaryInDB])
def read_all_book_summaries(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book_summaries = db.query(BookSummary).order_by(desc(BookSummary.created_at)).all()
    return book_summaries


@router.get("/current_user", response_model=list[BookSummaryInDB])
def read_current_user_book_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book_summaries = db.query(BookSummary).filter(BookSummary.uploaded_by == current_user.user_id).order_by(desc(BookSummary.created_at)).all()
    return book_summaries


@router.get("/{summary_id}", response_model=BookSummaryInDB)
def read_book_summary(summary_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book_summary = db.query(BookSummary).filter(BookSummary.summary_id == summary_id).first()
    if book_summary is None:
        raise HTTPException(status_code=404, detail="Book Summary not found")
    return book_summary


@router.post("/", response_model=BookSummaryInDB)
def create_book_summary(book_summary: BookSummaryBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Create new book_summary
    new_book_summary = BookSummary(title=book_summary.title, author=book_summary.author, genre=book_summary.genre, summary=book_summary.summary, uploaded_by=current_user.user_id)
    db.add(new_book_summary)
    db.commit()
    db.refresh(new_book_summary)

    latest_book_summary = db.query(BookSummary).order_by(desc(BookSummary.created_at)).first()
    return latest_book_summary


@router.put("/{summary_id}", response_model=BookSummaryInDB)
def update_user(summary_id: int, book_summary_update: BookSummaryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book_summary = db.query(BookSummary).filter(BookSummary.summary_id == summary_id).first()
    if db_book_summary is None:
        raise HTTPException(status_code=404, detail="Book Summary not found")
    for attr, value in book_summary_update.dict(exclude_unset=True).items():
        setattr(db_book_summary, attr, value)
    db.commit()
    db.refresh(db_book_summary)
    return db_book_summary


@router.delete("/{summary_id}", response_model=dict)
def delete_user(summary_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book_summary = db.query(BookSummary).filter(BookSummary.summary_id == summary_id).first()
    if db_book_summary is None:
        raise HTTPException(status_code=404, detail="Book Summary not found")
    db.delete(db_book_summary)
    db.commit()
    return {"message": "Book Summary deleted successfully"}
