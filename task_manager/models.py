from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='assigned_user', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    tasks = db.relationship('Task', backref='project', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    dependencies = db.relationship(
        'Task',
        secondary='task_dependencies',
        primaryjoin='Task.id==TaskDependency.task_id',
        secondaryjoin='Task.id==TaskDependency.depends_on_id',
        backref='dependents'
    )

class TaskDependency(db.Model):
    __tablename__ = 'task_dependencies'
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)
    depends_on_id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)