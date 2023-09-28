from flask import Flask
from flask_cors import CORS
from models import db
# from models import Role, Staff, Course, Registration, JobRole, Skill, JobRoleSkill, CourseSkill, LearningJourney, LearningJourneyItem

def create_app(app_name='api_app'):
  app = Flask(app_name)
  app.config.from_object('config.BaseConfig')
  #CORS(app)
  CORS(app, resources={r"/api/*": {"origins": "*"}})
 

  from api import api
  app.register_blueprint(api, url_prefix="/api")

  
  db.init_app(app)
  return app
