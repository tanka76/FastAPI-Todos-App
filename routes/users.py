from fastapi import Depends,HTTPException,APIRouter,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from schema import users as user_schema
from models.users import User,Todo
from database.connection import get_db
from crud.crud_user import get_user_by_email,create_user,get_all_users,get_user_by_id,authenticate_user
from core.security import create_access_token,verify_access_token

router = APIRouter()



#response_model what we sent back to client .response_model ==> pydantic model with orm_mode=True(Schema ) 
#UserCreate what we want payload as input for user create .Both are pydantic models


#User Create
@router.post("/user", response_model=user_schema.UserSchema,status_code=201) 
async def create_user_route(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    print("User Create",user)
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db,user=user)

#User Get
@router.get("/user",response_model=List[user_schema.UserSchema]) 
async def get_user_route(db: Session = Depends(get_db)):
    users=get_all_users(db=db)
    return users

#user delete
@router.delete("/user/{user_id}")
async def delete_user(user_id: int,db: Session = Depends(get_db),status_code=status.HTTP_204_NO_CONTENT):
    user=get_user_by_id(db=db,user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}


@router.post("/user/token")
async def user_login_route(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    print("User Login")
    email=user.email
    password=user.password
    user=authenticate_user(db=db,email=email,password=password)
    if not user:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    
    user_payload={"user_id":user.id,"email":user.email}
    access_token=create_access_token(data=user_payload)
    return {"access_token": access_token, "token_type": "bearer"}


#create,update,delete todos (protected routes)

@router.post("/todo",response_model=user_schema.TodoSchema,status_code=201) 
async def create_todo_route(todo: user_schema.TodoCreate, db: Session = Depends(get_db)):
    print("Todo Create",todo.dict())
    todo_data=todo.dict()
    todo=Todo(title=todo_data.get('title'),description=todo_data.get('description'),owner_id=3)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo
    