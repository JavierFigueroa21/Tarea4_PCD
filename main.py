from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import Union
from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    user_id = Column(Integer, unique=True)
    user_email = Column(String, unique=True)
    age = Column(Integer, nullable=True)
    recommendations = Column(String)
    ZIP = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)


#Endpoint para la creacion de usuarios
@app.post("/create_user/")
def create_user(user: User):
    db = SessionLocal()
    db_user = db.query(User).filter(User.user_email == user.user_email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Usuario creado correctamente"}


# Endpoint para la actualizacion de usuarios
@app.put("/update_user/{user_id}")
def update_user(user_id: int, user: User):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for var, value in vars(user).items():
        if value:
            setattr(db_user, var, value)
    db.commit()
    db.refresh(db_user)
    return {"message": "Usuario actualizado correctamente"}



# Endpoint para optener el usuario
@app.get("/get_user/{user_id}")
def get_user(user_id: int):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Endpoint para eliminar usuario
@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(db_user)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}

#correr el api, cambiando de puerto, en caso de que este siendo usado o no funcione
# uvicorn main:app --reload --port 8001
