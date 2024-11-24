# File Sharing System

This project is a file sharing application built with Django and Django Rest Framework. It allows users to upload and download .pptx, .docx, and .xlsx files.

## Features
- Ops User
  can upload files
- Client User
  can view all available files and download them

## Technologies
- Python
- Django
- Django Rest Framework
- SQLite (or other databases)
- HTML/CSS for the frontend

## Setup Instructions

## Install Dependencies:
pip install -r requirements.txt

## Apply Migrations:
python manage.py migrate

## Create a Superuser (Optional):
python manage.py createsuperuser

## To start the development server, run:
python manage.py runserver

You can access the application at http://127.0.0.1:8000/.

## API Endpoints

- User Management (Create User)
  
URL: /users/create/
Method: POST

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "strongpassword123"
}

- Task Management (Create Task)
  
URL: /tasks/create/
Method: POST

{
        "name": "Setup CI/CD Pipeline",
        "description": "Automate deployments using Jenkins and Docker.",
        "task_type": "DevOps",
}

- Assign Task to Users
  
URL: /tasks/<int:task_id>/assign/
Method: POST
{
  "user_ids": [1, 2]
}

- Get Tasks for a User
  
URL: /users/<int:user_id>/tasks/
Method: GET
Response:

{
  "user_id": 1,
  "tasks": [
    {
      "id": 1,
      "title": "Fix API bug",
      "description": "Resolve the issue with the task assignment API.",
      "due_date": "2024-10-25",
      "priority": "High"
    }
  ]
}
