from sqlalchemy.orm import Session
import models, schemas

def get_todos(db: Session):
    return db.query(models.Todo).all()

def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(title=todo.title, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()
    return todo

def update_todo(db: Session, todo_id: int, todo_data: schemas.TodoCreate):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.title = todo_data.title
    todo.completed = todo_data.completed
    db.commit()
    return todo
