from fastapi import FastAPI, status, HTTPException, Request, Depends, Header
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import time
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker, declarative_base, Session
import asyncio
app = FastAPI()

# -----------------------------------------

# CRUD WITH DB
# CREATE 

# -----------------------------------------

@app.post("/todos")
def create_todo(title:str, db:Session = Depends(get_db)):
    todo = Todo(title=title, completed="False")
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return{
        "message":"Todo Created",
        "data":todo
    }

# -----------------------------------------
# READ
# -----------------------------------------

@app.get("/todos")
def get_todos(db:Session = Depends(get_db)):
    todos = db.query(Todo).all()

    return{
        "Total":len(todos),
        "data":todos
    }


@app.get("/todos/{todo_id}")
def get_todo(todo_id:int, db:Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id==todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo
    

# -----------------------------------------
# UPDATE
# -----------------------------------------

@app.put("/todo/{todo_id}")
def update_todo(todo_id:int, title:str, db:Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id==todo_id).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.title = title

    db.commit()
    db.refresh(todo)

    return{
        "message":"Todo Updated",
        "data":todo
    }



# -----------------------------------------
# DELETE
# -----------------------------------------

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int, db:Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id==todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()

    return {
        "message":"Todo Deleted"
    }

