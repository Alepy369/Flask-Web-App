from flask import Flask, session, request
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, logout_user, current_user
from datetime import datetime, timedelta, timezone

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.secret_key = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    @app.before_first_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime() = timedelta(seconds=15)
        if current_user.is_authenticated:
            last_active = session.get('last_active')
            utc_now = datetime.now(timezone.utc)  # Current aware UTC time
            if last_active:
                duration = (utc_now - last_active).total_seconds()
                print(f"Time since last activity: {duration} seconds")
                if duration > app.permanent_session_lifetime():
                    print("Session expired. Logging out user.")
                    logout_user()

            # Update the last activity time in the session for the current user
            session['last_active'] = utc_now

    return app

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')