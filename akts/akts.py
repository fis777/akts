from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
#app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\fomini\PycharmProjects\akts\test.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SECRET_KEY'] = 'hfdolauifc0qn3rl312jr0f9u3r2no'
#app.config['DEBUG'] = True

db = SQLAlchemy(app)

from akts import views
from akts import models

if __name__ == '__main__':
    app.run()