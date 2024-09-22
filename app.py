from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tasks = relationship("Task", back_populates="category")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    projects = relationship("Project", back_populates="user")

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False)
    due_date = Column(Date, nullable=True)
    project_id = Column(Integer, ForeignKey('projects.id'))  # Assuming Task is linked to a Project
    category_id = Column(Integer, ForeignKey('categories.id'))  # Foreign key to Category

    category = relationship("Category", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")