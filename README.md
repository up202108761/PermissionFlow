# PermissionFlow

PermissionFlow is a web application developed with **FastAPI** that allows employees to request access to internal company applications. Application owners can review pending requests, approve or reject them, and leave comments.

---

## Team

- Gonçalo Matos
- Alexandra Torres
- João Chaves

---

## Technologies Used

- Python 3
- FastAPI
- SQLAlchemy
- SQLite
- Jinja2
- Bootstrap 5
- Uvicorn

---

## Features

### Employee

- View available applications
- Submit an access request
- Choose an access profile
- Add a justification
- Select the desired access date
- Track the status of submitted requests
- View comments from the application owner

### Application Owner

- View all pending requests
- Approve requests
- Reject requests
- Add comments to requests

---

## Project Structure

```
PermissionFlow
│
├── app
│   ├── templates
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── seed.py
│
├── requirements.txt
├── permissionflow.db
└── README.md
```

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd PermissionFlow
```

---

## 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

---

## 3. Activate the virtual environment

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Command Prompt:

```cmd
.venv\Scripts\activate
```

Git Bash:

```bash
source .venv/Scripts/activate
```

---

## 4. Install the required libraries

```bash
pip install -r requirements.txt
```

---

## 5. Create the database and insert sample data

```bash
python -m app.seed
```

This command creates:

- Sample users
- Sample applications
- Initial database data

---

## 6. Start the application

```bash
uvicorn app.main:app --reload
```

If everything is correct, the terminal will display:

```
Uvicorn running on http://127.0.0.1:8000
```

---

# How to Use the Application

## Home Page

Open:

```
http://127.0.0.1:8000
```

From the home page you can:

- View available applications
- Request access
- View your requests
- Open the owner dashboard

---

## Request Access

1. Click **Request Access**
2. Select an application
3. Choose the access profile
4. Enter a justification
5. Select the desired date
6. Click **Submit Request**

The request will be stored in the database with the status:

```
Pending
```

---

## My Requests

Click **My Requests** to view:

- Application name
- Description
- Owner
- Access profile
- Justification
- Desired date
- Current status
- Owner comment (if available)

Possible request statuses:

- Pending
- Approved
- Rejected

---

## Owner Dashboard

Click **Owner Dashboard**.

The owner can:

- View all pending requests
- Read the employee justification
- Add a comment
- Approve the request
- Reject the request

After approval or rejection:

- The request disappears from the pending list.
- The employee can see the updated status and the owner's comment in **My Requests**.

---

## Database

The application uses **SQLite**.

The database file is automatically created:

```
permissionflow.db
```

Tables:

- users
- applications
- access_requests

---

## API Documentation

FastAPI automatically generates API documentation.

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Future Improvements

- User authentication
- Login system
- Search and filters
- Email notifications
- Admin dashboard
- Better access profile management
- Better UI/UX

---

## Developed for

Final Project

PermissionFlow - Internal Application Access Management System