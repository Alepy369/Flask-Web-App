from flask import Flask, session, flash
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
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=1200)
    
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
    
    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            last_active = session.get('last_active')
            utc_now = datetime.now(timezone.utc)  # Current aware UTC time
            #print(f"Last active: {last_active}, Current time: {utc_now}")

            if last_active is not None:
                duration = (utc_now - last_active).total_seconds()
                print(f"Time since last activity: {duration} seconds")
                if duration > app.config['PERMANENT_SESSION_LIFETIME'].total_seconds():
                    flash("Session expired. Logging out user.", category="error")
                    logout_user()

            # Update the last activity time in the session for the current user
            if last_active is None:
                session['last_active'] = utc_now
            else:
                session['last_active'] = last_active

    return app

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')