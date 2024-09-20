from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task, Project, User, Category

def display_data():
    db: Session = SessionLocal()

    # Fetch all users
    users = db.query(User).all()
    print("\n--- Users ---")
    for user in users:
        print(f"User: {user.name}, Email: {user.email}")

    # Fetch all projects
    projects = db.query(Project).all()
    print("\n--- Projects ---")
    for project in projects:
        print(f"Project: {project.name}, User: {project.user.name}")

    # Fetch all categories
    categories = db.query(Category).all()
    print("\n--- Categories ---")
    for category in categories:
        print(f"Category: {category.name}")

    # Fetch all tasks
    tasks = db.query(Task).all()
    print("\n--- Tasks ---")
    for task in tasks:
        print(f"Task: {task.title}, Due: {task.due_date}, Project: {task.project.name}, Category: {task.category.name}")

    db.close()

if __name__ == "__main__":
    display_data()
