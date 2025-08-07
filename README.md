# Django Task Manager

A comprehensive task management application built with Django that allows users to create, manage, and track their tasks efficiently.

## 🚀 Features

- **User Authentication**: Registration, login, logout functionality
- **Task Management**: Create, read, update, delete tasks
- **Priority Levels**: Set task priorities (Low, Medium, High, Urgent)
- **Due Dates**: Set and track task deadlines
- **Task Status**: Track task progress (Pending, In Progress, Completed)
- **Search & Filter**: Find tasks by title, category, priority, or status
- **Responsive Design**: Mobile-friendly interface
- **User Dashboard**: Overview of tasks and statistics

## 🛠️ Technologies Used

- **Backend**: Django 4.2+
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Authentication**: Django's built-in authentication system
- **Forms**: Django Forms with validation

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8+
- pip (Python package manager)
- Git

## 🔧 Installation

1. Fork the repo (GitHub repository)
1. Clone the forked repo
    ```
    git clone the-link-from-your-forked-repo
    ```
    - You can get the link by clicking the `Clone or download` button in your repo
1. Open the project folder in your IDE
1. Open a terminal in the project folder
1. Create a branch for the solution and switch on it
    ```
    git checkout -b develop
    ```
    - You can use any other name instead of `develop`
1. If you are using PyCharm - it may propose you to automatically create venv for your project 
    and install requirements in it, but if not:
    ```
    python -m venv venv
    venv\Scripts\activate (on Windows)
    source venv/bin/activate (on macOS)
    pip install -r requirements.txt
    ```