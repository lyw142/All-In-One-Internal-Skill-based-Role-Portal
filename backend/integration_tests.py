import unittest
import json
import sqlite3
from flask_testing import TestCase
from datetime import datetime, date
from models import Staff_Skill, db, Staff, Role, Staff, Staff_Skill, Skill, RoleSkillMapping, RoleListing, Application, Access_Control, Manager, Director, NormalStaff, Application, RoleListing
# from application import create_app
from flask import Flask
from flask_cors import CORS

'''
To run test cases - the command is:
python -m unittest integration_tests.py 
'''

def create_app(app_name='api_app'):
  app = Flask(app_name)
#   app.config.from_object('config.BaseConfig')
  app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
  app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
  app.config['TESTING'] = True
  #CORS(app)
  CORS(app, resources={r"/api/*": {"origins": "*"}})
 

  from api import api
  app.register_blueprint(api, url_prefix="/api")

  
  db.init_app(app)
  return app

app = create_app()


class TestApp(TestCase):

    # def create_app(self):
    #     # pass in test configuration
    #     return app

    # def setUp(self):
    #     # Delete application entry in case it already exists. This is to pass the create application endpoint success case
    #     application_to_delete = db.session.query(Application).filter_by(
    #         Staff_ID=140036,
    #         Listing_ID=1
    #     ).first()

    #     # Delete the selected record if it exists
    #     if application_to_delete:
    #         db.session.delete(application_to_delete)
    #         db.session.commit()

    # def tearDown(self):
    #     pass

    def create_app(self):
        # pass in test configuration
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestCreateApplication(TestApp):
    
    def test_create_application(self):
        # Creating a Staff instance
        ac = Access_Control(
            Access_ID=1,
            Access_Control_Name="Admin"
        )
        staff = Staff(
            Staff_ID = 140036,
            Staff_FName="John",
            Staff_LName="Doe",
            Dept="IT",
            Email="john@example.com",
            Country="USA",
            Password="password",
            Role_ID=1,  
            Access_Rights=1  
        )
        staff1 = Staff(
            Staff_ID = 140879,
            Staff_FName="Jane",
            Staff_LName="Doe",
            Dept="IT",
            Email="sdf",
            Country="USA",
            Password="password",
            Role_ID=1,
            Access_Rights=1  
        )

        # Creating a Role instance
        role = Role(
            Role_Name="Engineer",
            Role_Responsibilities="Design and develop software",
            Role_ID=1
        )
        
        # Creating a RoleListing instance
        role_listing = RoleListing(
            Deadline=date(2023,12,31), 
            Date_Posted=date(2023,10,1),  
            Country="USA",
            Hiring_Manager=140036, 
            Role_ID=1 
        )
        
        db.session.add_all([ac,staff,staff1, role, role_listing])
        db.session.commit()

        # 
        # Prepare data for the POST request
        data = {
        "Staff_ID": 140036,
        "Listing_ID": 1
        }

        response = self.client.post("/api/applyforopenrole", json=data)

        # Check if the response has a status code of 201 (created) indicating success
        self.assertEqual(response.status_code, 201)

        # Check if the response JSON contains the expected message
        self.assertEqual(response.json, {"message": "Application successfully created"})
    

    def test_create_application_duplicate(self):
        # Creating a Staff instance
        ac = Access_Control(
            Access_ID=1,
            Access_Control_Name="Admin"
        )
        staff = Staff(
            Staff_ID = 140036,
            Staff_FName="John",
            Staff_LName="Doe",
            Dept="IT",
            Email="john@example.com",
            Country="USA",
            Password="password",
            Role_ID=1,  
            Access_Rights=1 
        )
        staff1 = Staff(
            Staff_ID = 140879,
            Staff_FName="Jane",
            Staff_LName="Doe",
            Dept="IT",
            Email="sdf",
            Country="USA",
            Password="password",
            Role_ID=1,  
            Access_Rights=1  
        )

        # Creating a Role instance
        role = Role(
            Role_Name="Engineer",
            Role_Responsibilities="Design and develop software",
            Role_ID=1
        )

        
        # Creating a RoleListing instance
        role_listing = RoleListing(
            # Deadline=datetime(2023,12,31),  # Replace with a valid date
            Deadline= date(2023,12,31),

            # Date_Posted=datetime(2023,10,1),  # Replace with a valid date
            Date_Posted= date(2023,10,1),
            Country="USA",
            Hiring_Manager=140036,  # Replace with a valid Hiring_Manager (Staff_ID) from your database
            Role_ID=1  # Replace with a valid Role_ID from your database
        )
      
        appl = Application(
            
            Application_Date=date(2023,10,31),
            
            Application_Status="Pending",
            Staff_ID=140879,
            Listing_ID=1
        )
        
        db.session.add_all([ac,appl,staff,staff1, role, role_listing])
        db.session.commit()

        # 
        # Prepare data for the POST request
        data = {
        "Staff_ID": 140879,
        # "Staff_ID": 140036, 
        "Listing_ID": 1
        }
        # Prepare data for the POST request 
        response = self.client.post("/api/applyforopenrole", json=data)

        # Check if the response has a status code of 400 (bad request) indicating duplicate application
        self.assertEqual(response.status_code, 400)

        # Check if the response JSON contains the expected error message
        self.assertEqual(response.json, {"error": "You have already applied for this job role."})


if __name__ == '__main__':
    unittest.main()