from flask import Flask
from extensions import login_manager, db, ckeditor
from routes import bp, login_manager


def create_app():
    flask_app = Flask(__name__)
    flask_app.secret_key = b'94551be546b23efeac0374ea76d056dfe962b1f0e928a2fcdd06d9bf8a717367'
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

    db.init_app(flask_app)
    login_manager.init_app(flask_app)
    ckeditor.init_app(flask_app)

    flask_app.register_blueprint(bp)

    with flask_app.app_context():
        db.create_all()

    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.secret_key = "Q!92;x(t9}u#K9U)#)b.=YtP3}e=o?VX*,j"
    app.run(debug=True)
