from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy instance globally

db = SQLAlchemy()


def create_app(config_object='backend_codebase.config.TestConfig'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize the app with the global db instance
    db.init_app(app)

    # Register blueprints
    from .views import views_bp
    app.register_blueprint(views_bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
