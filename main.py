from flask import Flask
from extensions import login_manager, db, ckeditor
from routes import bp
from flask_gravatar import Gravatar
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    flask_app = Flask(__name__)
    flask_app.secret_key = os.environ.get('FLASK_KEY')
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///blog.db')

    db.init_app(flask_app)
    login_manager.init_app(flask_app)
    ckeditor.init_app(flask_app)

    gravatar = Gravatar(flask_app, size=50, rating='g', default='retro')

    flask_app.register_blueprint(bp)

    with flask_app.app_context():
        db.create_all()

    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.run(debug=True)
