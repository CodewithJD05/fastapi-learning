from fastapi import FastAPI, status, HTTPException, Request, Depends, Header
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import time
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker, declarative_base, Session
import asyncio



app = FastAPI()


# -------------------------------------

# GET request with query parameters

# -------------------------------------


# @app.get("/users")
# def get_users(name : str = None):
#     return {"name": name }

# @app.get("/products")
# def get_products(limit : int = 10):
#     return {"limit": limit} 

# @app.get("/items")
# def get_items(name : str = None, price : int = 0):
#     return {"name": name, "price": price} 

# -------------------------------------

# POST WITH request body 

# -------------------------------------

# class User(BaseModel):
#     name : str
#     age : int
#     email : str

# @app.post("/create-user")
# def create_user(user:User):
#     return{
#         "message":"User Created",
#         "data":user
#     }

# class Address(BaseModel):
#     city:str
#     pincode:int

# class User(BaseModel):
#     name:str
#     age:int
#     address:Address
# @app.post("/create-user")
# def create_user(user:User):
#     return user

# -------------------------------------

#  CRUD API for TODO application

# -------------------------------------



# todos = []

# class ToDo(BaseModel):
#     id:int
#     title:str
#     completed:bool

# @app.post("/todos")
# def create_todo(todo:ToDo):
#     todos.append(todo)
#     return {"message":"TODO added","data":todo}

# @app.get("/todos")
# def get_todos():
#     return todos

# @app.get("/todos/{todo_id}")
# def get_todo(todo_id: int):
#     for todo in todos:
#         if todo.id == todo_id:
#             return todo
#     return {"message": "TODO not found"}

# @app.put("/todos/{todo_id}")
# def update_todo(todo_id: int, updated_todo: ToDo):
#     for index, todo in enumerate(todos):
#         if todo.id == todo_id:
#             todos[index] = updated_todo
#             return {"message": "TODO updated", "data": updated_todo}
#     return {"message": "TODO not found"}

# @app.delete("/todos/{todo_id}")
# def delete_todo(todo_id: int):
#     for index, todo in enumerate(todos):
#         if todo.id == todo_id:
#             deleted_todo = todos.pop(index)
#             return {"message": "TODO deleted", "data": deleted_todo}
#     return {"message": "TODO not found"}




# --------------------------------------

# PATH + QUERY + BODY COMBO

#  --------------------------------------


# users = []

# class User(BaseModel):
#     id:int
#     name:str
#     age:int

# @app.post("/users")
# def create_user(user:User):
#     users.append(user)
#     return{
#         "message":"User Created",
#         "data":user
#     }

# @app.put("/users/{user_id}")
# def update_user(user_id:int, user:User, notify:bool = False):
#     if user_id < len(users):
#         users[user_id]=user

#         return {
#             "message":"User Updated",
#             "data":user,
#             "notify":notify
#             }
#     return {"message": "User not found"}

# # --------------------------------------

# # RESPONCE MODELS

# #  --------------------------------------

# class User(BaseModel):
#     name:str
#     age:int
#     password:str

# class UserResponce(BaseModel):
#     name:str
#     age:int

# @app.get("/user", response_model=UserResponce)
# def get_user():
#     return{
#         "name" : "jay",
#         "age" : 21,
#         "password": "jay123"
#     }



# --------------------------------------

#  STATUS CODE, CUSTOME RESPONCES, ERROR HANDLING BASICS

#  --------------------------------------

# @app.post("/create_user", status_code=status.HTTP_201_CREATED)
# def create_user():
#     return {
#         "message":"User Created"
#     }

# @app.get("/users")
# def get_users():
#     return{
#         "status":"success",
#         "message":"User Fetched",
#         "data":{
#             "name":"mohit"
#         }
#     }

# @app.get("/users/{user_id}")
# def get_user(user_id:int):
#     if user_id != 1:
#         raise HTTPException(
#             status_code=404,
#             detail="User Not Found"
#         )
#     return {
#         "id":1,
#         "name":"Mohit"
#     }

# --------------------------------------

# EXCEPTION HANDLING, HTTPEXCEPTION, 
# CUSTOM EXCEPTION, GLOBAL ERROR HANDLER

#  --------------------------------------

# @app.get("/users/{user_id}")
# def get_user(user_id:int):
#     if user_id!=1:
#         raise HTTPException(
#             status_code=404,
#             detail="User Not Found"
#         )
#     return{
#         "id":1,
#         "name":"Jay"
#     }


# --------------------------------------

# DEPENDENCY INJECTION

#  --------------------------------------


# def common_logoc():
#     return {
#         "message":"Common Logic executed"
#     }

# @app.get("/home")
# def home(data = Depends(common_logoc)):
#     return data

# def get_current_user():
#     return{
#         "user":"jay"
#     }

# @app.get("/profile")
# def profile(user = Depends(get_current_user)):
#     return user

# @app.get("/dashboard")
# def dashboard(user = Depends(get_current_user)):
#     return user

# ------------------------------

# def varify_token(token: str = Header(None)):
#     if token != "my-secrete-token":
#         raise HTTPException(
#             status_code=401,
#             detail="Unauthorized"
#         )
#     return{
#         "user":"Authorized User"
#     }

# @app.get("/secure-data")
# def secure_data(user = Depends(varify_token)):
#     return{
#         "message":"Secure data accessed",
#         "user":user
#     }
        
# --------------------------------------

# MIDDLEWARE

#  --------------------------------------

# @app.middleware("http")
# async def my_middleware(request:Request,call_next):
#     print("Request received")

#     response  = await call_next(request)

#     print("Response Sent")

#     return response

#  --------------------------------------

# LOGGING MIDDLEWARE

#  --------------------------------------

# @app.middleware("http")
# async def log_middleware(request:Request,call_next):
#     start_time = time.time()

#     response = await call_next(request)

#     process_time = time.time()-start_time

#     print(f"Path:{request.url.path} | Time:{process_time}")

#     return response




# -----------------------------------------

# SQLITE DB

# -----------------------------------------

# conn = sqlite3.connect("test.db",check_same_thread=False)
# cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS todos(
#     id INTEGER PRIMARY KEY,
#     title TEXT,
#     completed TEXT 
#     )
# """)

# conn.commit()

# @app.get("/home")
# def home():
#     return{
#         "message":"SQLite connected"
#     }


# -----------------------------------------

# SQLALCHEMY DB

# -----------------------------------------

DATABASE_URL = "sqlite:///test.db"

engine =  create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

sessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


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



# -----------------------------------------

# ASYNCHRONOUS PROGRAMMMING(ASYNC/AWAIT)

# -----------------------------------------

# def task():
#     time.sleep(3)
#     return "Done"

# async def  task():
#     await asyncio.sleep(3)
#     return "done"

@app.get("/")

async def home():
    await asyncio.sleep(3)
    return{
        "message":"Async API"
    }

# -----------------------------------------

# AUTHENTICATION BASICS : JWT INTRO, 
# TOKEN-BASED AUTH, LOGIN API

# -----------------------------------------







