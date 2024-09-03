from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Configuración de la base de datos
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_name", String, nullable=False),
    Column("user_email", String, unique=True, nullable=False),
    Column("age", Integer),
    Column("recommendations", String),
    Column("ZIP", String)
)

metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Modelos de Pydantic
class UserCreate(BaseModel):
    user_name: str
    user_id: int = Field(..., alias="id")
    user_email: EmailStr
    age: Optional[int] = None
    recommendations: List[str]
    ZIP: Optional[str] = None


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None
    age: Optional[int] = None
    recommendations: Optional[List[str]] = None
    ZIP: Optional[str] = None


app = FastAPI()


# Crear usuario
@app.post("/users/")
async def create_user(user: UserCreate):
    session = SessionLocal()
    try:
        recommendations_str = ",".join(user.recommendations)
        session.execute(users_table.insert().values(
            id=user.user_id,
            user_name=user.user_name,
            user_email=user.user_email,
            age=user.age,
            recommendations=recommendations_str,
            ZIP=user.ZIP
        ))
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Email already exists.")
    finally:
        session.close()
    return {"message": "User created successfully."}


# Actualizar usuario por id
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    session = SessionLocal()
    query = users_table.select().where(users_table.c.id == user_id)
    existing_user = session.execute(query).fetchone()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found.")

    update_data = {key: value for key, value in user.dict(exclude_unset=True).items()}
    if "recommendations" in update_data:
        update_data["recommendations"] = ",".join(update_data["recommendations"])

    session.execute(users_table.update().where(users_table.c.id == user_id).values(**update_data))
    session.commit()
    session.close()
    return {"message": "User updated successfully."}


# Obtener usuario por id
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    session = SessionLocal()
    query = users_table.select().where(users_table.c.id == user_id)
    user = session.execute(query).fetchone()
    session.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return dict(user)


# Eliminar usuario por id
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    session = SessionLocal()
    query = users_table.select().where(users_table.c.id == user_id)
    user = session.execute(query).fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    session.execute(users_table.delete().where(users_table.c.id == user_id))
    session.commit()
    session.close()
    return {"message": "User deleted successfully."}

