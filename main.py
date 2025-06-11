from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
router = APIRouter(prefix="/api")
@router.get("/todos/", response_model=list[schemas.TodoOut])
def read_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)

@router.post("/todos/", response_model=schemas.TodoOut)
def add_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@router.put("/todos/{todo_id}/", response_model=schemas.TodoOut)
def update_todo(todo_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.update_todo(db, todo_id, todo)

@router.delete("/todos/{todo_id}/")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo(db, todo_id)

app.include_router(router)
