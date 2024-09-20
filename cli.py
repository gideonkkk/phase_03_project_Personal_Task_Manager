# cli.py
import click
from models import Task, Project
from database import SessionLocal, init_db
from datetime import datetime

init_db()

@click.group()
def cli():
    """Task Manager CLI"""
    pass

@cli.command()
def list_tasks():
    """List all tasks"""
    db = SessionLocal()
    tasks = db.query(Task).all()  

    if not tasks:
        click.echo("No tasks available.")
        return

    for task in tasks:
        click.echo(f"Task {task.id}: {task.title} | Status: {task.status} | Due Date: {task.due_date}")

@cli.command()
@click.argument('title')
@click.option('--project_id', default=None, help='The project to which the task belongs')
@click.option('--due_date', default=None, help='Due date for the task (YYYY-MM-DD)')
def add_task(title, project_id, due_date):
    """Add a new task"""
    db = SessionLocal()

    task_data = {
        'title': title,
        'status': 'Pending',
        'due_date': datetime.strptime(due_date, '%Y-%m-%d') if due_date else None,
        'project_id': project_id
    }

    new_task = Task(**task_data)
    db.add(new_task)
    db.commit()

    click.echo(f"Task '{title}' added to project '{project_id}' with due date '{due_date}'")

@cli.command()
def add_multiple_tasks():
    """Add multiple tasks using tuples"""
    db = SessionLocal()

    
    tasks_to_add = [
        ('Task 1', '2024-01-01', 1),  
        ('Task 2', '2024-02-01', 2),
        ('Task 3', '2024-03-01', 1)
    ]

    for task_title, task_date, project_id in tasks_to_add:
        new_task = Task(
            title=task_title,
            due_date=datetime.strptime(task_date, '%Y-%m-%d'),
            project_id=project_id
        )
        db.add(new_task)

    db.commit() 
    click.echo(f"{len(tasks_to_add)} tasks added successfully!")

if __name__ == '__main__':
    cli()
