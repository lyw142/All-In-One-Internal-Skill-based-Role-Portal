import unittest
from models import Staff_Skill, db, Staff, Role, Staff, Staff_Skill, Skill, RoleSkillMapping, RoleListing, Application, Access_Control, Manager, Director, NormalStaff, Application, RoleListing
# To run code: 
# python -m unittest tests_unit.py 
'''
This document is a compilation of unit tests for our models.
'''


class TestAccessControl(unittest.TestCase): 
    def test(self): 
        ac1 = Access_Control(Access_ID=1,Access_Control_Name="Admin")
        self.assertEqual(ac1.get_access_control_details(), {"Access_ID":ac1.Access_ID, "Access_Control_Name":ac1.Access_Control_Name})

class TestStaff(unittest.TestCase):
    def test(self):
        s1 = Staff(Staff_ID=1, Staff_FName="John", Staff_LName='Lee', Email="join@gmail.com", Password="1234", Role_ID=1, Country="Singapore", Dept='IT', Access_Rights=1)
        self.assertEqual(s1.get_staff_details(), {"Staff_ID":s1.Staff_ID, "Staff_FName":s1.Staff_FName, "Staff_LName":s1.Staff_LName, "Email":s1.Email, "Password":s1.Password, "Role_ID":s1.Role_ID, "Country":s1.Country, "Dept":s1.Dept, "Access_Rights":s1.Access_Rights})

class TestManager(unittest.TestCase):
    def test(self):
        m1 = Manager(Staff_ID=3,Staff_FName="John", Staff_LName='Lee', Email="join@gmail.com", Password="1234", Role_ID=1, Country="Singapore", Dept='IT', Access_Rights=1,ResponsibleTeam="Dev", Reporting_Manager=1)
        self.assertEqual(m1.get_manager_details(), {"Staff_ID":m1.Staff_ID, "Responsible_Team":m1.ResponsibleTeam, "Reporting_Manager":m1.Reporting_Manager})

class TestDirector(unittest.TestCase):
    def test(self):
        d1 = Director(Staff_ID=2,Staff_FName="John", Staff_LName='Lee', Email="join@gmail.com", Country="Singapore", Dept='IT', Password="1234", Role_ID=1,  Access_Rights=1, ResponsibelDept="IT", Reporting_Manager=1)
        self.assertEqual(d1.get_director_details(), {"Staff_ID":d1.Staff_ID, "Responsible_Department":d1.ResponsibleDept, "Reporting_Manager":d1.Reporting_Manager})

class TestNormalStaff(unittest.TestCase):
    def test(self):
        ns1 = NormalStaff(Staff_ID=5,Staff_FName="John", Staff_LName='Lee', Email="John@gmail.com", Country="Singapore", Dept='IT', Password="1234", Role_ID=1, Access_Rights=1, Reporting_Manager=1)
        self.assertEqual(ns1.get_normal_staff_details(), {"Staff_ID":ns1.Staff_ID, "Reporting_Manager":ns1.Reporting_Manager})

class TestStaffSkill(unittest.TestCase):
    def test(self):
        ss1 = Staff_Skill(Staff_ID=1, Skill_ID=1)
        self.assertEqual(ss1.get_staff_skill_details(), {"Staff_ID":ss1.Staff_ID, "Skill_ID":ss1.Skill_ID})

class TestSkill(unittest.TestCase):
    def test(self):
        s1 = Skill(Skill_Name = "Python", Skill_Desc = "Programming Language",Skill_Status="Active")
        self.assertEqual(s1.get_skill_details(), {"Skill_ID":s1.Skill_ID, "Skill_Name":s1.Skill_Name, "Skill_Desc":s1.Skill_Desc, "Skill_Status":s1.Skill_Status})

class TestRole(unittest.TestCase):
    def test(self): 
        r1 = Role(Role_ID=1,Role_Name="Developer", Role_Responsibilities="Dev")
        self.assertEqual(
            r1.get_role_details(), 
            {"Role_Name": "Developer", "Role_Responsibilities": "Dev"}
        )

class TestRoleSkillMapping(unittest.TestCase):
    def test(self):
        rsm1 = RoleSkillMapping(Role_ID=1, Skill_ID=1)
        self.assertEqual(rsm1.get_role_skill_mapping_details(), {"Role_ID":rsm1.Role_ID, "Skill_ID":rsm1.Skill_ID})

class TestApplication(unittest.TestCase):
    def test(self):
        a1 = Application(Application_Date="2021-01-01", Application_Status="Pending", Staff_ID=1, Listing_ID=1)
        self.assertEqual(a1.get_application_details(), {"Application_ID":a1.Application_ID, "Application_Date":a1.Application_Date, "Application_Status":a1.Application_Status, "Staff_ID":a1.Staff_ID, "Listing_ID":a1.Listing_ID})

class TestRoleListing(unittest.TestCase):
    def test(self):
        rl1 = RoleListing(Deadline="2021-01-01", Date_Posted="2021-01-01", Country="Singapore", Hiring_Manager=1, Role_ID=1)
        self.assertEqual(rl1.get_role_listing_details(), {"Listing_ID":rl1.Listing_ID, "Deadline":rl1.Deadline, "Date_Posted":rl1.Date_Posted, "Country":rl1.Country, "Hiring_Manager":rl1.Hiring_Manager, "Role_ID":rl1.Role_ID})


if __name__ == '__main__':
    unittest.main()