from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    book_summaries = relationship("BookSummary", back_populates="users")


class BookSummary(Base):
    __tablename__ = "book_summaries"

    summary_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    genre = Column(String(100))
    summary = Column(Text)
    file_url = Column(String(255))
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    uploaded_by = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    users = relationship("User", back_populates="book_summaries")
