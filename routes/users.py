from fastapi import Depends,HTTPException,APIRouter,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from schema import users as user_schema
from models.users import User,Todo
from database.connection import get_db
from crud.crud_user import get_user_by_email,create_user,get_all_users,get_user_by_id,authenticate_user
from core.security import create_access_token,verify_access_token,get_current_user

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
async def get_user_route(db: Session = Depends(get_db),user_data:dict=Depends(get_current_user)):
    users=get_all_users(db=db)
    return users

#user delete
@router.delete("/user/{user_id}")
async def delete_user(user_id: int,db: Session = Depends(get_db),status_code=status.HTTP_204_NO_CONTENT,user_data:dict=Depends(get_current_user)):
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


#create todo
@router.post("/todo",response_model=user_schema.TodoSchema,status_code=201) 
async def create_todo_route(todo: user_schema.TodoCreate, db: Session = Depends(get_db),user_data:dict=Depends(get_current_user)):
    todo_data=todo.dict()
    user_id=user_data.get('user_id')
    todo=Todo(title=todo_data.get('title'),description=todo_data.get('description'),owner_id=user_id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo
    
# get all todos 
@router.get("/todo",response_model=List[user_schema.TodoList]) 
async def get_todo_route(db: Session = Depends(get_db),user_data:dict=Depends(get_current_user)):
    user_id=user_data.get('user_id')
    todos = db.query(Todo).filter(Todo.owner_id == user_id).all()
    return todos

#delete todo
@router.delete("/todo/{todo_id}/")
async def delete_post(todo_id: int, user_data:dict=Depends(get_current_user), db: Session = Depends(get_db)):
    user_id=user_data.get('user_id')
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    if not todo.owner_id==user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

#update todo
@router.patch("/todo/{todo_id}/")
async def update_post(todo_id: int, todo_data: user_schema.TodoUpdate, user_data: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id=user_data.get('user_id')
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    if not todo.owner_id==user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    if todo_data.title:
        todo.title = todo_data.title
    if todo_data.description:
        todo.description = todo_data.description
    if todo_data.is_completed:
        todo.is_completed = todo_data.is_completed

    db.commit()
    db.refresh(todo)
    return todo

