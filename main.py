from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.endpoints import users, auth, book_summaries
from core.database import Base, engine

# Create FastAPI instance
app = FastAPI()

# Add Origins
origins = ["http://localhost:5000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(book_summaries.router, prefix="/api/book_summaries", tags=["book_summaries"])

# Create tables in the database
Base.metadata.create_all(bind=engine)
