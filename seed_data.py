from app import User, Task, Project, Category
from database import SessionLocal
from datetime import datetime

def seed_data():
    db = SessionLocal()
    try:
        user1 = User(username='Dennis Brown', email='delta@example.com')
        user2 = User(username='Future Fambo', email='falcon@example.com')
        user3 = User(username='Eric Donald', email='eagle@example.com')

        db.add_all([user1, user2, user3])
        db.commit()

        work_category = Category(name='Hobby')
        personal_category = Category(name='Family')

        db.add_all([work_category, personal_category])
        db.commit()

        project1 = Project(name='Task Manager Project', user_id=user1.id)
        project2 = Project(name='Website Development', user_id=user2.id)
        project3 = Project(name='Marketing Campaign', user_id=user3.id)

        db.add_all([project1, project2, project3])
        db.commit()

        task1 = Task(title='Complete CLI Task Manager', description='Build and deploy a CLI-based task manager', 
                     due_date=datetime(2024, 9, 20), project_id=project1.id, category_id=work_category.id, user_id=user1.id)
        task2 = Task(title='Test Task Manager', description='Run tests for the task manager',
                     due_date=datetime(2024, 9, 25), project_id=project1.id, category_id=work_category.id, user_id=user1.id)
        task3 = Task(title='Design Website Layout', description='Create a wireframe and design for portfolio website',
                     due_date=datetime(2024, 10, 1), project_id=project2.id, category_id=personal_category.id, user_id=user2.id)
        task4 = Task(title='Develop Contact Form', description='Implement a functional contact form',
                     due_date=datetime(2024, 10, 10), project_id=project2.id, category_id=work_category.id, user_id=user2.id)
        task5 = Task(title='Create Social Media Plan', description='Outline a plan for social media content',
                     due_date=datetime(2024, 9, 30), project_id=project3.id, category_id=work_category.id, user_id=user3.id)
        task6 = Task(title='Launch Ad Campaign', description='Set up and launch digital ads',
                     due_date=datetime(2024, 10, 5), project_id=project3.id, category_id=work_category.id, user_id=user3.id)

        db.add_all([task1, task2, task3, task4, task5, task6])
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
