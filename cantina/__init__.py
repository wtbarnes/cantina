from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()
app.config['WTF_CSRF_ENABLED'] = True
from cantina import views
