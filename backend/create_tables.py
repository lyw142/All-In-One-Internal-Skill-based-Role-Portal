from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Role, Staff, Skill, Staff_Skill, RoleSkillMapping, Application, RoleListing
from models import db

app = Flask('api_app')


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/SPM'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                               'pool_recycle': 280}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)


# Define your classes as mentioned in your code here

if __name__ == '__main__':
    # This will create the database tables based on your class definitions
    db.init_app(app)
    with app.app_context():
        db.create_all() 
