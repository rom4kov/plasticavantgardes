from flask import Flask
from extensions import login_manager, db, ckeditor
from routes import bp
from flask_gravatar import Gravatar
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///blog.db')
print(os.environ.get('DB_URI'))

db.init_app(app)
login_manager.init_app(app)
ckeditor.init_app(app)

gravatar = Gravatar(app, size=50, rating='g', default='retro')

app.register_blueprint(bp)

# with app.app_context():
#     db.create_all()


if __name__ == "__main__":
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.run(debug=True)
