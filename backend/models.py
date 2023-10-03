"""
models.py
- Data classes for the application
"""

from email.policy import default
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

    
## STAFF ##
class Staff(db.Model):
    __tablename__ = 'staff'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(50), nullable=False)
    Staff_LName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(50), nullable=False)
    Role_ID = db.Column(db.Integer, db.ForeignKey('role.Role_ID'), nullable=False)
    Access_Rights = db.Column(db.Integer, nullable=False)
    
    
    def __init__(self, Staff_FName, Staff_LName, Email, Password, Access_Rights, Role_ID): 
        self.Staff_FName = Staff_FName
        self.Staff_LName = Staff_LName
        self.Email = Email
        self.Password = Password
        self.Access_Rights = Access_Rights
        self.Role_ID = Role_ID

    def to_json(self):
        return {
            "Staff_ID": self.Staff_ID,
            "Staff_FName": self.Staff_FName,
            "Staff_LName": self.Staff_LName,
            "Email": self.Email,
            "Password": self.Password,
            "Access_Rights": self.Access_Rights,
            "Role_ID": self.Role_ID
        }

## STAFF_SKILL ##
class Staff_Skill(db.Model):
    __tablename__ = 'staffskill'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Staff_ID = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID', ondelete='CASCADE'), primary_key=True)
    Skill_ID = db.Column(db.Integer, db.ForeignKey('skill.Skill_ID', ondelete='CASCADE'), primary_key=True)

    def __init__(self, Staff_ID, Skill_ID):
        self.Staff_ID = Staff_ID
        self.Skill_ID = Skill_ID

    # skill = db.relationship('Skill', backref='staff_skill')

    # specify how to represent our Staff_Skill object as a JSON string
    def json(self):
        return {
                "Staff_ID": self.Staff_ID, 
                "Skill_ID": self.Skill_ID,
            }
       
## SKILL ##
class Skill(db.Model):
    __tablename__ = 'skill'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Skill_ID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Skill_Name = db.Column(db.String(20), nullable=False)
    Skill_Status = db.Column(db.String(15), nullable=False, default = 'Active')

    def __init__(self, Skill_Name, Skill_Status):
        self.Skill_Name = Skill_Name
        self.Skill_Status = Skill_Status


    # specify how to represent our book object as a JSON string
    def json(self):
        return {
                "Skill_ID": self.Skill_ID,
                "Skill_Name": self.Skill_Name,
                "Skill_Status": self.Skill_Status
            }
            
    

## ROLE ##
class Role(db.Model):
    __tablename__ = 'role'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Role_ID = db.Column(db.Integer, primary_key=True)
    Role_Name = db.Column(db.String(20), nullable=False)
    Role_Responsibilities = db.Column(db.String(1000), nullable=False)
    Role_Requirements = db.Column(db.String(1000), nullable=False)
    Salary = db.Column(db.String(20), nullable=False)
    Dept = db.Column(db.String(50), nullable=False)
    
    

    def __init__(self, Role_Name, Role_Responsibilities, Role_Requirements, Salary, Dept):
        self.Role_Name = Role_Name
        self.Role_Responsibilities = Role_Responsibilities
        self.Role_Requirements = Role_Requirements
        self.Salary = Salary
        self.Dept = Dept
        

    def to_json(self):
        return {
            "Role_ID": self.Role_ID,
            "Role_Name": self.Role_Name,
            "Role_Responsibilties": self.Role_Responsibilities,
            "Role_Requirements": self.Role_Requirements,
            "Salary": self.Salary,
            "Dept": self.Dept
        }

## Role_skill_mapping #
class RoleSkillMapping(db.Model):
    __tablename__ = 'role_skill_mapping'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Skill_ID = db.Column(db.Integer, db.ForeignKey('skill.Skill_ID', ondelete='CASCADE'), primary_key=True)
    Role_ID = db.Column(db.Integer, db.ForeignKey('role.Role_ID', ondelete='CASCADE'), primary_key=True)

    def __init__(self, Skill_ID, Role_ID):
        self.Role_ID = Role_ID
        self.Skill_ID = Skill_ID

    # specify how to represent our book object as a JSON string
    def json(self):
        return {
                "Role_ID": self.Role_ID,
                "Skill_ID": self.Skill_ID
            }
    
## Application ##
class Application(db.Model):
    __tablename__ = 'application'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Application_ID = db.Column(db.Integer, primary_key=True)
    Application_Date = db.Column(db.Date, nullable=False)
    Application_Status = db.Column(db.String(20), nullable=False)
    Staff_ID = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID', ondelete='CASCADE'))
    Listing_ID = db.Column(db.Integer, db.ForeignKey('role_listing.Listing_ID', ondelete='CASCADE'))

    #staff = db.relationship('Staff', backref='applications')
    #role = db.relationship('Role', backref='applications')
    
    def __init__(self, Application_Date, Application_Status, Staff_ID, Listing_ID):
        self.Application_Date = Application_Date
        self.Application_Status = Application_Status
        self.Staff_ID = Staff_ID
        self.Listing_ID = Listing_ID

    # specify how to represent our book object as a JSON string
    def json(self):
        return {
                    "Application_ID": self.Application_ID, 
                    "Application_Date": self.Application_Date,
                    "Application_Status": self.Application_Status,
                    "Staff_ID": self.Staff_ID,
                    "Listing_ID": self.Listing_ID
                }

## Role_Listing ##
class RoleListing(db.Model):
    __tablename__ = 'role_listing'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Listing_ID = db.Column(db.Integer, primary_key=True)
    Deadline = db.Column(db.Date, nullable=False)
    Date_Posted = db.Column(db.Date, nullable=False)
    Hiring_Manager = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID', ondelete='CASCADE'), nullable=False)
    Role_ID = db.Column(db.Integer, db.ForeignKey('role.Role_ID', ondelete='CASCADE'), nullable=False)

    #staff = db.relationship('Staff', backref='applications')
    #role = db.relationship("Role", back_populates="role_listing")
    
    def __init__(self, Deadline, Date_Posted, Hiring_Manager, Role_ID):
        self.Deadline = Deadline
        self.Date_Posted = Date_Posted
        self.Hiring_Manager = Hiring_Manager
        self.Role_ID = Role_ID

    def to_json(self):
        return {
            "Listing_ID": self.Listing_ID,
            "Deadline": self.Deadline, 
            "Date_Posted": self.Date_Posted,
            "Hiring_Manager": self.Hiring_Manager,
            "Role_ID": self.Role_ID
        }