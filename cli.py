import click
from app import Task, User, Project, Category
from database import SessionLocal, init_db
from datetime import datetime

init_db()

@click.group()
def cli():
    """Task Manager CLI"""
    pass

# Task Commands
@cli.command()
def list_tasks():
    """List all tasks"""
    db = SessionLocal()
    try:
        tasks = db.query(Task).all()
        if not tasks:
            click.echo("No tasks available.")
            return

        for task in tasks:
            click.echo(f"Task {task.id}: {task.title} | Status: {task.status} | Due Date: {task.due_date}")
    finally:
        db.close()

@cli.command()
@click.argument('title')
@click.option('--project_id', default=None, help='The project to which the task belongs')
@click.option('--due_date', default=None, help='Due date for the task (YYYY-MM-DD)')
@click.option('--description', default='', help='Description of the task')
def add_task(title, project_id, due_date, description):
    """Add a new task"""
    db = SessionLocal()
    try:
        if project_id and not db.query(Project).filter(Project.id == project_id).first():
            click.echo(f"No project found with ID {project_id}")
            return

        task_data = {
            'title': title,
            'status': 'Pending',
            'due_date': datetime.strptime(due_date, '%Y-%m-%d') if due_date else None,
            'project_id': project_id,
            'description': description
        }

        new_task = Task(**task_data)
        db.add(new_task)
        db.commit()
        click.echo(f"Task '{title}' added to project '{project_id}' with due date '{due_date}'")
    except Exception as e:
        db.rollback()
        click.echo(f"Error adding task: {e}")
    finally:
        db.close()

@cli.command()
@click.argument('task_id', type=int)
@click.option('--title', help='New title for the task')
@click.option('--due_date', help='New due date for the task (YYYY-MM-DD)')
@click.option('--description', help='New description for the task')
@click.option('--status', help='New status for the task')
def update_task(task_id, title, due_date, description, status):
    """Update an existing task"""
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            click.echo(f"No task found with ID {task_id}")
            return

        if title:
            task.title = title
        if due_date:
            task.due_date = datetime.strptime(due_date, '%Y-%m-%d')
        if description:
            task.description = description
        if status:
            task.status = status

        db.commit()
        click.echo(f"Task {task_id} updated successfully!")
    except Exception as e:
        db.rollback()
        click.echo(f"Error updating task: {e}")
    finally:
        db.close()

@cli.command()
@click.argument('task_id', type=int)
def delete_task(task_id):
    """Delete a task"""
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            click.echo(f"No task found with ID {task_id}")
            return

        db.delete(task)
        db.commit()
        click.echo(f"Task {task_id} deleted successfully!")
    except Exception as e:
        db.rollback()
        click.echo(f"Error deleting task: {e}")
    finally:
        db.close()

# User Commands
@cli.command()
def list_users():
    """List all users"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        if not users:
            click.echo("No users available.")
            return

        for user in users:
            click.echo(f"User {user.id}: {user.username} | Email: {user.email}")
    finally:
        db.close()

@cli.command()
@click.argument('username')
@click.argument('email')
def add_user(username, email):
    """Add a new user"""
    db = SessionLocal()
    try:
        new_user = User(username=username, email=email)
        db.add(new_user)
        db.commit()
        click.echo(f"User '{username}' added.")
    except Exception as e:
        db.rollback()
        click.echo(f"Error adding user: {e}")
    finally:
        db.close()

@cli.command()
@click.argument('user_id', type=int)
@click.option('--username', help='New username for the user')
@click.option('--email', help='New email for the user')
def update_user(user_id, username, email):
    """Update an existing user"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            click.echo(f"No user found with ID {user_id}")
            return

        if username:
            user.username = username
        if email:
            user.email = email

        db.commit()
        click.echo(f"User {user_id} updated successfully!")
    except Exception as e:
        db.rollback()
        click.echo(f"Error updating user: {e}")
    finally:
        db.close()

@cli.command()
@click.argument('user_id', type=int)
def delete_user(user_id):
    """Delete a user"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            click.echo(f"No user found with ID {user_id}")
            return

        db.delete(user)
        db.commit()
        click.echo(f"User {user_id} deleted successfully!")
    except Exception as e:
        db.rollback()
        click.echo(f"Error deleting user: {e}")
    finally:
        db.close()

# Project Commands
@cli.command()
def list_projects():
    """List all projects"""
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
        if not projects:
            click.echo("No projects available.")
            return

        for project in projects:
            click.echo(f"Project {project.id}: {project.name} | User ID: {project.user_id}")
    finally:
        db.close()

@cli.command()
@click.argument('name')
@click.option('--user_id', required=True, help='The user to whom the project belongs')
def add_project(name, user_id):
    """Add a new project"""
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.id == user_id).first():
            click.echo(f"No user found with ID {user_id}")
            return

        new_project = Project(name=name, user_id=user_id)
        db.add(new_project)
        db.commit()
        click.echo(f"Project '{name}' added.")
    except Exception as e:
        db.rollback()
        click.echo(f"Error adding project: {e}")
    finally:
        db.close()

@cli.command()
@click.argument('project_id', type=int)
@click.option('--name', help='New name for the project')
@click.option('--user_id', help='New user ID for the project')
def update_project(project_id, name, user_id):
    """Update an existing project"""
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            click.echo(f"No project found with ID {project_id}")
            return

        if name:
            project.name = name
        if user_id and db.query(User).filter(User.id == user_id).first():
            project.user_id = user_id

        db.commit()
        click.echo(f"Project {project_id} updated successfully!")
    except Exception as e:
        db.rollback()
        click.echo(f"Error updating project: {e}")
    finally:
        db.close()

@cli.command()
@click.argument('project_id', type=int)
def delete_project(project_id):
    """Delete a project"""
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            click.echo(f"No project found with ID {project_id}")
            return

        db.delete(project)
        db.commit()
        click.echo(f"Project {project_id} deleted successfully!")
    except Exception as e:
        db.rollback()
        click.echo(f"Error deleting project: {e}")
    finally:
        db.close()

# Category Commands
@cli.command()
def list_categories():
    """List all categories"""
    db = SessionLocal()
    try:
        categories = db.query(Category).all()
        if not categories:
            click.echo("No categories available.")
            return

        for category in categories:
            click.echo(f"Category {category.id}: {category.name}")
    finally:
        db.close()

@cli.command()
@click.argument('name')
def add_category(name):
    """Add a new category"""
    db = SessionLocal()
    try:
        new_category = Category(name=name)
        db.add(new_category)
        db.commit()
        click.echo(f"Category '{name}' added.")
    except Exception as e:
        db.rollback()
        click.echo(f"Error adding category: {e}")
    finally:
        db.close()

@cli.command()
@click.argument('category_id', type=int)
@click.option('--name', help='New name for the category')
def update_category(category_id, name):
    """Update an existing category"""
    db = SessionLocal()
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            click.echo(f"No category found with ID {category_id}")
            return

        if name:
            category.name = name

        db.commit()
        click.echo(f"Category {category_id} updated successfully!")
    except Exception as e:
        db.rollback()
        click.echo(f"Error updating category: {e}")
    finally:
        db.close()

@cli.command()
@click.argument('category_id', type=int)
def delete_category(category_id):
    """Delete a category"""
    db = SessionLocal()
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            click.echo(f"No category found with ID {category_id}")
            return

        db.delete(category)
        db.commit()
        click.echo(f"Category {category_id} deleted successfully!")
    except Exception as e:
        db.rollback()
        click.echo(f"Error deleting category: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    cli()
