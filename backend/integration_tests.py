import unittest
import json
import sqlite3
from flask_testing import TestCase
from models import Staff_Skill, db, Staff, Role, Staff, Staff_Skill, Skill, RoleSkillMapping, RoleListing, Application, Access_Control, Manager, Director, NormalStaff, Application, RoleListing
from application import create_app

'''
To run test cases - the command is:
python -m unittest tests_integration.py 
'''

app = create_app()

class TestApp(TestCase):

    def create_app(self):
        # pass in test configuration
        return app

    def setUp(self):
        # Delete application entry in case it already exists. This is to pass the create application endpoint success case
        application_to_delete = db.session.query(Application).filter_by(
            Staff_ID=140036,
            Listing_ID=1
        ).first()

        # Delete the selected record if it exists
        if application_to_delete:
            db.session.delete(application_to_delete)
            db.session.commit()

    def tearDown(self):
        pass

class TestCreateApplication(TestApp):
    
    def test_create_application(self):
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
        # Prepare data for the POST request with the same Staff_ID and Listing_ID
        data = {
        "Staff_ID": 140879,
        "Listing_ID": 5
        }

        response = self.client.post("/api/applyforopenrole", json=data)

        # Check if the response has a status code of 400 (bad request) indicating duplicate application
        self.assertEqual(response.status_code, 400)

        # Check if the response JSON contains the expected error message
        self.assertEqual(response.json, {"error": "You have already applied for this job role."})
    

