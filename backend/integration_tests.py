import unittest
import json
import sqlite3
import random
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

    def test_create_application_missing_key(self):
        # Test when a required key is missing in the JSON data
        data = {
            "Listing_ID": 1  # Missing the "Staff_ID" key
        }
        response = self.client.post("/api/applyforopenrole", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Missing required key: 'Staff_ID'"})
    
    def test_create_application_invalid_value(self):
        # Test when the Staff_ID value is not an integer
        data = {
            "Staff_ID": "invalid_staff_id",
            "Listing_ID": 1
        }
        response = self.client.post("/api/applyforopenrole", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid value: Staff_ID and Listing_ID must be integers"})



class TestCreateJobListing(TestApp):

    def test_create_job_listing(self):
        # Prepare data for the POST request
        data = {
            "Role_ID": random.randint(1, 100000),
            "Role_Name": "Software Engineer",
            "Role_Responsibilities": "Develop and maintain software applications",
            "Deadline": "2023-12-31",
            "Date_Posted": "2023-10-01",
            "Country": "USA",
            "Hiring_Manager": 140036,
            "Skills": ["Python", "JavaScript"]
        }

        response = self.client.post("/api/createjoblisting", json=data)

        # Check if the response has a status code of 201 (created) indicating success
        self.assertEqual(response.status_code, 201)

        # Check if the response JSON contains the expected message
        self.assertEqual(response.json, {"message": "Role created successfully, Role_SKill mapped and New Listing created."})

    def test_create_existing_job_listing(self):
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
    #     # Prepare data for the POST request with an existing Role_Name
        data = {
            "Role_ID": 1,
            "Role_Name": "Engineer",  
            "Role_Responsibilities": "Design and develop software",
            "Deadline": "2023-12-31",
            "Date_Posted": "2023-10-01",
            "Country": "USA",
            "Hiring_Manager": 140036,
            "Skills": "Python"  
        }
        db.session.add_all([ac,staff,staff1, role])
        db.session.commit()
        response = self.client.post("/api/createjoblisting", json=data)

        # Check if the response has a status code of 200 (OK) indicating success
        self.assertEqual(response.status_code, 200)

        # Check if the response JSON contains the expected message
        self.assertEqual(response.json, {"message": "Role already exists, new listing created."})


    def test_create_job_listing_missing_required_field(self):
        # Test when a required field is missing in the JSON data
        data = {
            "Role_ID": random.randint(1, 100000),
            "Role_Responsibilities": "Develop and maintain software applications",
            "Deadline": "2023-12-31",
            "Date_Posted": "2023-10-01",
            "Country": "USA",
            "Hiring_Manager": 140036,
            "Skills": ["Python", "JavaScript"]
        }
        response = self.client.post("/api/createjoblisting", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Role_Name must be a string"})
    
    
    def test_create_job_listing_no_skills(self):
        # Test when no skills are provided in the "Skills" list
        data = {
            "Role_ID": random.randint(1, 100000),
            "Role_Name": "Software Engineer",
            "Role_Responsibilities": "Develop and maintain software applications",
            "Deadline": "2023-12-31",
            "Date_Posted": "2023-10-01",
            "Country": "USA",
            "Hiring_Manager": 140036,
            "Skills": []  # Empty skills list
        }
        response = self.client.post("/api/createjoblisting", json=data)
        self.assertEqual(response.status_code, 201)  # It should succeed even without skills
        self.assertEqual(response.json, {"message": "Role created successfully, Role_SKill mapped and New Listing created."})

class TestUpdateRoleListing(TestApp):

    def setUp(self):
        super().setUp()  # Call the parent class's setUp method
        self.app = self.create_app()

    def test_update_role_listing(self):

        role = Role(
            Role_Name="Consultant",
            Role_Responsibilities="The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings.",
            Role_ID=7
        )
        
        # Creating a RoleListing instance
        role_listing = RoleListing(
            Deadline=date(2023,11,9), 
            Date_Posted=date(2023,10,30),  
            Country="Indonesia",
            Hiring_Manager=180001, 
            Role_ID=7
        )

        role_skill_mapping_entries = [
            RoleSkillMapping(Role_ID=7, Skill_ID=1),
            RoleSkillMapping(Role_ID=7, Skill_ID=4),
            RoleSkillMapping(Role_ID=7, Skill_ID=12)
        ]
        db.session.add_all(role_skill_mapping_entries)
        db.session.add_all([role, role_listing])
        db.session.commit()

        # 
        # Prepare data for the POST request
        data = {
            "Deadline": "2023-12-31",
            "Date_Posted": "2023-10-1",
            "Role_Responsibilities": "The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings.",
            "Salary": 59001,
            "Country": "Indonesia",
            "AddedSkills": [5],
            "RemovedSkills": [1, 12]
        }

        response = self.client.put("/api/updateRoleListing/1", json=data)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json, {"message": "Role listing updated successfully"})

        # Check if skills are correctly added or removed in the role_skill_mapping table
        added_skills = RoleSkillMapping.query.filter(RoleSkillMapping.Role_ID == 7, RoleSkillMapping.Skill_ID == 5).first()
        removed_skills = RoleSkillMapping.query.filter(RoleSkillMapping.Role_ID == 7, RoleSkillMapping.Skill_ID.in_([1, 12])).all()

        # Assert that the skill is added
        self.assertIsNotNone(added_skills)

        # Assert that the skills are removed
        for skill in removed_skills:
            self.assertIsNone(skill)

    def test_invalid_role_id(self):
        
        role = Role(
            Role_Name="Consultant",
            Role_Responsibilities="The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings.",
            Role_ID=7
        )
        
        # Creating a RoleListing instance
        role_listing = RoleListing(
            Deadline=date(2023,11,9), 
            Date_Posted=date(2023,10,30),  
            Country="Indonesia",
            Hiring_Manager=180001, 
            Role_ID=7
        )

        role_skill_mapping_entries = [
            RoleSkillMapping(Role_ID=7, Skill_ID=1),
            RoleSkillMapping(Role_ID=7, Skill_ID=4),
            RoleSkillMapping(Role_ID=7, Skill_ID=12)
        ]
        db.session.add_all(role_skill_mapping_entries)
        db.session.add_all([role, role_listing])
        db.session.commit()

        data = {
            "Deadline": "2023-12-31",
            "Date_Posted": "2023-10-1",
            "Role_Responsibilities": "Updated responsibilities",
            "Salary": 59001,
            "Country": "Indonesia",
            "AddedSkills": [5],
            "RemovedSkills": [1, 12]
        }

        response = self.client.put("/api/updateRoleListing/999", json=data)
        self.assertEqual(response.status_code, 404)

    def test_empty_role_responsibilities(self):
        role = Role(
            Role_Name="Consultant",
            Role_Responsibilities="The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings.",
            Role_ID=7
        )
        
        # Creating a RoleListing instance
        role_listing = RoleListing(
            Deadline=date(2023,11,9), 
            Date_Posted=date(2023,10,30),  
            Country="Indonesia",
            Hiring_Manager=180001, 
            Role_ID=7
        )

        role_skill_mapping_entries = [
            RoleSkillMapping(Role_ID=7, Skill_ID=1),
            RoleSkillMapping(Role_ID=7, Skill_ID=4),
            RoleSkillMapping(Role_ID=7, Skill_ID=12)
        ]
        db.session.add_all(role_skill_mapping_entries)
        db.session.add_all([role, role_listing])
        db.session.commit()

        data = {
            "Deadline": "2023-12-31",
            "Date_Posted": "2023-10-1",
            "Role_Responsibilities": "", 
            "Salary": 59001,
            "Country": "Indonesia",
            "AddedSkills": [5],
            "RemovedSkills": [1, 12]
        }

        response = self.client.put("/api/updateRoleListing/1", json=data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_role_listing_id(self):
        role = Role(
            Role_Name="Consultant",
            Role_Responsibilities="The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings.",
            Role_ID=7
        )
        
        # Creating a RoleListing instance
        role_listing = RoleListing(
            Deadline=date(2023,11,9), 
            Date_Posted=date(2023,10,30),  
            Country="Indonesia",
            Hiring_Manager=180001, 
            Role_ID=7
        )

        role_skill_mapping_entries = [
            RoleSkillMapping(Role_ID=7, Skill_ID=1),
            RoleSkillMapping(Role_ID=7, Skill_ID=4),
            RoleSkillMapping(Role_ID=7, Skill_ID=12)
        ]
        db.session.add_all(role_skill_mapping_entries)
        db.session.add_all([role, role_listing])
        db.session.commit()

        invalid_id = 100 
        data = {
            "Deadline": "2023-11-9",
            "Date_Posted": "2023-10-30",
            "Role_Responsibilities": "Updated responsibilities",
            "Salary": 59001,
            "Country": "Indonesia",
            "AddedSkills": [5],
            "RemovedSkills": [1, 12]
        }
        response = self.client.put(f"/api/updateRoleListing/{invalid_id}", json=data)

        self.assertEqual(response.status_code, 404)

        self.assertEqual(response.json, {"message": "Role listing not found"})

    def test_empty_added_skills(self):

        role = Role(
            Role_Name="Consultant",
            Role_Responsibilities="The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings.",
            Role_ID=7
        )
        
        # Creating a RoleListing instance
        role_listing = RoleListing(
            Deadline=date(2023,11,9), 
            Date_Posted=date(2023,10,30),  
            Country="Indonesia",
            Hiring_Manager=180001, 
            Role_ID=7
        )

        role_skill_mapping_entries = [
            RoleSkillMapping(Role_ID=7, Skill_ID=1),
            RoleSkillMapping(Role_ID=7, Skill_ID=4),
            RoleSkillMapping(Role_ID=7, Skill_ID=12)
        ]

        db.session.add_all(role_skill_mapping_entries)
        db.session.add_all([role, role_listing])
        db.session.commit()

        data = {
            "Deadline": "2023-12-31",
            "Date_Posted": "2023-10-1",
            "Role_Responsibilities": "Updated responsibilities",
            "Salary": 59001,
            "Country": "Indonesia",
            "AddedSkills": [],  # Empty "AddedSkills" list
            "RemovedSkills": [1, 12]
        }

        response = self.client.put("/api/updateRoleListing/1", json=data)
        self.assertEqual(response.status_code, 200)

    def test_empty_removed_skills(self):

        role = Role(
            Role_Name="Consultant",
            Role_Responsibilities="The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings.",
            Role_ID=7
        )
        
        # Creating a RoleListing instance
        role_listing = RoleListing(
            Deadline=date(2023,11,9), 
            Date_Posted=date(2023,10,30),  
            Country="Indonesia",
            Hiring_Manager=180001, 
            Role_ID=7
        )

        role_skill_mapping_entries = [
            RoleSkillMapping(Role_ID=7, Skill_ID=1),
            RoleSkillMapping(Role_ID=7, Skill_ID=4),
            RoleSkillMapping(Role_ID=7, Skill_ID=12)
        ]
        
        db.session.add_all(role_skill_mapping_entries)
        db.session.add_all([role, role_listing])
        db.session.commit()

        data = {
            "Deadline": "2023-12-31",
            "Date_Posted": "2023-10-1",
            "Role_Responsibilities": "Updated responsibilities",
            "Salary": 59001,
            "Country": "Indonesia",
            "AddedSkills": [5], 
            "RemovedSkills": []
        }

        response = self.client.put("/api/updateRoleListing/1", json=data)
        self.assertEqual(response.status_code, 200)

    def test_get_unique_country(self):
        # Insert some sample data into the Staff table
        staff_entries = [
            Staff(
            Staff_ID = 140036,
            Staff_FName="John",
            Staff_LName="Doe",
            Dept="IT",
            Email="john@example.com",
            Country="USA",
            Password="password",
            Role_ID=1,  
            Access_Rights=1  
        ),
            Staff(
            Staff_ID = 140879,
            Staff_FName="Jane",
            Staff_LName="Doe",
            Dept="IT",
            Email="sdf",
            Country="Singapore",
            Password="password",
            Role_ID=1,
            Access_Rights=1  
        )
        ]

        db.session.add_all(staff_entries)
        db.session.commit()

        # Send a GET request to retrieve unique country values
        response = self.client.get("/api/getUniqueCountry")

        self.assertEqual(response.status_code, 200)

        # Check if the response JSON contains the unique country values
        expected_result = ["Singapore", "USA"]
        self.assertEqual(response.json, expected_result)

    def test_get_unique_dept(self):
        # Insert some sample data into the Staff table
        staff_entries = [
            Staff(
            Staff_ID = 140036,
            Staff_FName="John",
            Staff_LName="Doe",
            Dept="IT",
            Email="john@example.com",
            Country="USA",
            Password="password",
            Role_ID=1,  
            Access_Rights=1  
        ),
            Staff(
            Staff_ID = 140879,
            Staff_FName="Jane",
            Staff_LName="Doe",
            Dept="Finance",
            Email="sdf",
            Country="Singapore",
            Password="password",
            Role_ID=1,
            Access_Rights=1  
        )
        ]

        db.session.add_all(staff_entries)
        db.session.commit()

        # Send a GET request to retrieve unique country values
        response = self.client.get("/api/getUniqueDept")

        self.assertEqual(response.status_code, 200)

        # Check if the response JSON contains the unique country values
        expected_result = ["Finance", "IT"]
        self.assertEqual(response.json, expected_result)

    def test_get_created_role_details(self):
        role = Role(
            Role_Name="Consultant",
            Role_Responsibilities="The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings.",
            Role_ID=7
        )
        
        # Creating a RoleListing instance
        role_listing = RoleListing(
            Deadline=date(2023,11,9), 
            Date_Posted=date(2023,10,30),  
            Country="Indonesia",
            Hiring_Manager=180001, 
            Role_ID=7
        )
        db.session.add_all([role, role_listing])
        db.session.commit()

        response = self.client.get("/api/getCreatedRoleDetails")

        self.assertEqual(response.status_code, 200)

        # Check if the response JSON contains the expected role details
        expected_result = [
            {"Role_ID": 7, "Role_Name": "Consultant"}
        ]
        self.assertEqual(response.json, expected_result)


if __name__ == '__main__':
    unittest.main()