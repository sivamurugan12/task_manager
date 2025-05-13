# Task Management REST API (Flask + MySQL)

## ✅ Features
- Manage users, projects, and tasks
- Tasks with dependencies
- Prevent circular dependencies
- Status updates with logic checks

---

## 🔧 Requirements

Install the following packages:

```bash
pip install -r requirements.txt
```

---

## 🗃️ MySQL Setup

1. Start MySQL server.
2. Create the database:

```sql
CREATE DATABASE taskdb;
```

3. Update your `config.py` with correct DB credentials:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/taskdb'
```

---

## 🚀 Running the App

### Step 1: Set environment

```bash
export FLASK_APP=app.py       # On Windows use: set FLASK_APP=app.py
```

### Step 2: Initialize database

```bash
python
>>> from app import app
>>> from models import db
>>> with app.app_context():
...     db.create_all()
...     exit()
```

### Step 3: Run the server

```bash
python app.py
```

App runs at: `http://localhost:5000`

---

## 🌱 Seeding Sample Data (Optional)

Create a file `db_seed.py`:
```python
from models import db, User, Project, Task
from app import app

with app.app_context():
    user = User(name="Alice", email="alice@example.com")
    project = Project(name="Project Alpha")
    db.session.add_all([user, project])
    db.session.commit()
```

Then run:
```bash
python db_seed.py
```

---

## ✅ Testing API

Use Postman or curl. Example:

```bash
curl -X POST http://localhost:5000/users/ -H "Content-Type: application/json" -d '{"name": "Bob", "email": "bob@example.com"}'
```---

## 🔁 Flask-Migrate: How to Use Migrations

### 🧩 Step-by-Step Migration Setup

1. **Install Required Packages**:
```bash
pip install Flask-Migrate
```

2. **Update `app.py`** to include migration setup:
```python
from flask_migrate import Migrate
migrate = Migrate(app, db)
```

3. **Initialize Migrations Folder**:
```bash
flask db init
```

4. **Create a Migration Script** (every time you change `models.py`):
```bash
flask db migrate -m "Initial tables"
```

5. **Apply Migrations** to the actual MySQL database:
```bash
flask db upgrade
```

---

### 🔁 Full Run and Migration Flow:

```bash
# Step 1: Create MySQL DB
CREATE DATABASE taskdb;

# Step 2: Set environment
export FLASK_APP=app.py  # Windows: set FLASK_APP=app.py

# Step 3: Initialize migrations folder
flask db init

# Step 4: Generate migration from models
flask db migrate -m "initial"

# Step 5: Apply migration
flask db upgrade

# Step 6: Run server
python app.py
```

---

### 🔄 Common Commands

- Reapply migrations:
```bash
flask db migrate -m "update"
flask db upgrade
```

- Downgrade last migration:
```bash
flask db downgrade
```