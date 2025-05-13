from flask import Flask
from config import Config
from models import db
from routes.users import user_bp
from routes.projects import project_bp
from routes.tasks import task_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(project_bp, url_prefix='/projects')
app.register_blueprint(task_bp, url_prefix='/tasks')

# ✅ Add this line
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)