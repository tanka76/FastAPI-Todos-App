from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String,nullable=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean(), default=False)

    todos = relationship("Todo", backref="user")

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    is_completed = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey('users.id'),nullable=False)


    # user atrr===> related user objects represent..User object associated with each Post

    # This specifies the target entity class, which is the User class. 
    # It tells SQLAlchemy that the relationship is with the User table.

    # This defines the reverse relationship in the User class. It tells SQLAlchemy that the "posts" 
    # attribute in the User class will be used to access the related Post objects. 




