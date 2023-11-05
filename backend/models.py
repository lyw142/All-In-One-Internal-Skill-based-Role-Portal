"""
models.py
- Data classes for the application
"""
from sqlalchemy import types
import datetime

from email.policy import default
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MyDateTime(types.TypeDecorator):
    impl = types.Date  # Use the Date type for Y-M-D

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            date_parts = value.split('T')[0]  # Split the string and keep only Y-M-D part
            return datetime.datetime.strptime(date_parts, '%Y-%m-%d').date()  # Convert to date
        return value
    
## ACCESS_RIGHTS ##
class Access_Control(db.Model):
    __tablename__ = 'access_control'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Access_ID = db.Column(db.Integer, primary_key=True)
    Access_Control_Name = db.Column(db.String(100), nullable=False)
    
    def __init__(self, Access_ID, Access_Control_Name): 
        self.Access_ID = Access_ID
        self.Access_Control_Name = Access_Control_Name

    def get_access_control_details(self):
        return {
            "Access_ID": self.Access_ID,
            "Access_Control_Name": self.Access_Control_Name,
        }
    
## STAFF ##
class Staff(db.Model):
    __tablename__ = 'staff'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(100), nullable=False)
    Staff_LName = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Country = db.Column(db.String(100), nullable=False)
    Dept = db.Column(db.String(100))
    Password = db.Column(db.String(100), nullable=False)
    Role_ID = db.Column(db.Integer, db.ForeignKey('role.Role_ID'))
    Access_Rights = db.Column(db.Integer, db.ForeignKey('access_control.Access_ID'), nullable=False)

    skills = db.relationship('Staff_Skill', backref='staff')
    
    def __init__(self, Staff_ID,Staff_FName, Staff_LName, Email, Country, Dept, Password, Role_ID, Access_Rights): 
        self.Staff_ID = Staff_ID
        self.Staff_FName = Staff_FName
        self.Staff_LName = Staff_LName
        self.Email = Email
        self.Country = Country
        self.Dept = Dept
        self.Password = Password
        self.Role_ID = Role_ID
        self.Access_Rights = Access_Rights

    def get_staff_details(self):
        return {
            "Staff_ID": self.Staff_ID,
            "Staff_FName": self.Staff_FName,
            "Staff_LName": self.Staff_LName,
            "Email": self.Email,
            "Country" : self.Country,
            "Dept" : self.Dept,
            "Password": self.Password,
            "Role_ID": self.Role_ID,
            "Access_Rights": self.Access_Rights
        }
    
## MANAGER ##
class Manager(Staff):
    __tablename__ = 'Manager'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Staff_ID = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID', ondelete='CASCADE'), primary_key=True)
    Responsible_Team = db.Column(db.String(100), nullable=False)
    Reporting_Manager = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID'))

    #Reporting_Manager = db.relationship('Staff', foreign_keys=[Reporting_Manager], backref='reporting_managers', remote_side=[Staff_ID])

    def __init__(self, Staff_ID, Staff_FName, Staff_LName, Email, Country, Dept, Password, Role_ID, Access_Rights, ResponsibleTeam, Reporting_Manager): 
        super().__init__(Staff_ID, Staff_FName, Staff_LName, Email, Country, Dept, Password, Role_ID, Access_Rights)
        self.ResponsibleTeam = ResponsibleTeam
        self.Reporting_Manager = Reporting_Manager
        self.staff_id = Staff.Staff_ID  # Set the staff_id column to match Staff's Staff_ID
    
    __mapper_args__ = {
        'polymorphic_identity': 'manager',
        "inherit_condition": Staff_ID == Staff.Staff_ID
    }

    def get_manager_details(self):
        return {
            "Staff_ID": self.Staff_ID,
            "Responsible_Team": self.ResponsibleTeam,
            "Reporting_Manager": self.Reporting_Manager,
        }


## Director ##
class Director(Staff):
    __tablename__ = 'Director'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Staff_ID = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID', ondelete='CASCADE'), primary_key=True)
    Responsible_Department = db.Column(db.String(100), nullable=False)
    Reporting_Manager = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID', ondelete='CASCADE'))

    __mapper_args__ = {
        'polymorphic_identity': 'director',
        "inherit_condition": Staff_ID == Staff.Staff_ID
    }
    
    #Reporting_Manager = db.relationship('Staff', foreign_keys=[Reporting_Manager], backref='reporting_managers', remote_side=[Staff_ID])

    def __init__(self, Staff_ID, Staff_FName, Staff_LName, Email, Country, Dept, Password, Role_ID, Access_Rights, ResponsibelDept, Reporting_Manager): 
        super().__init__(Staff_ID,Staff_FName, Staff_LName, Email, Country, Dept, Password, Role_ID, Access_Rights)
        self.ResponsibleDept = ResponsibelDept
        self.Reporting_Manager = Reporting_Manager
        self.staff_id = Staff.Staff_ID  # Set the staff_id column to match Staff's Staff_ID

    def get_director_details(self):
        return {
            "Staff_ID": self.Staff_ID,
            "Responsible_Department": self.ResponsibleDept,
            "Reporting_Manager": self.Reporting_Manager,
        }

## Normal Staff ##
class NormalStaff(Staff):
    __tablename__ = 'NormalStaff'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Staff_ID = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID', ondelete='CASCADE'), primary_key=True)
    Reporting_Manager = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID', ondelete='CASCADE'))

    __mapper_args__ = {
        'polymorphic_identity': 'normal_staff',
        "inherit_condition": Staff_ID == Staff.Staff_ID
    }

    #Reporting_Manager = db.relationship('Staff', foreign_keys=[Reporting_Manager], backref='reporting_managers', remote_side=[Staff_ID])

    def __init__(self, Staff_ID, Staff_FName, Staff_LName, Email, Country, Dept, Password, Role_ID, Access_Rights, Reporting_Manager): 
        super().__init__(Staff_ID,Staff_FName, Staff_LName, Email, Country, Dept, Password, Role_ID, Access_Rights)
        self.Reporting_Manager = Reporting_Manager
        self.staff_id = Staff.Staff_ID  # Set the staff_id column to match Staff's Staff_ID

    def get_normal_staff_details(self):
        return {
            "Staff_ID": self.Staff_ID,
            "Reporting_Manager": self.Reporting_Manager,
        }

## STAFF_SKILL ##
class Staff_Skill(db.Model):
    __tablename__ = 'staffskill'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Staff_ID = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID', ondelete='CASCADE'), primary_key=True)
    Skill_ID = db.Column(db.Integer, db.ForeignKey('skill.Skill_ID', ondelete='CASCADE'), primary_key=True)
    
    skill = db.relationship('Skill', backref='staff_skills')
    def __init__(self, Staff_ID, Skill_ID):
        self.Staff_ID = Staff_ID
        self.Skill_ID = Skill_ID

    # skill = db.relationship('Skill', backref='staff_skill')

    # specify how to represent our Staff_Skill object as a JSON string
    def get_staff_skill_details(self):
        return {
                "Staff_ID": self.Staff_ID, 
                "Skill_ID": self.Skill_ID,
            }
       
## SKILL ##
class Skill(db.Model):
    __tablename__ = 'skill'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Skill_ID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Skill_Name = db.Column(db.String(100), nullable=False)
    Skill_Desc = db.Column(db.String(1000), nullable=False)
    Skill_Status = db.Column(db.String(15), nullable=False, default = 'Active')

    def __init__(self, Skill_Name, Skill_Desc, Skill_Status):
        self.Skill_Name = Skill_Name
        self.Skill_Desc = Skill_Desc
        self.Skill_Status = Skill_Status


    # specify how to represent our book object as a JSON string
    def get_skill_details(self):
        return {
                "Skill_ID": self.Skill_ID,
                "Skill_Name": self.Skill_Name,
                "Skill_Desc" : self.Skill_Desc,
                "Skill_Status": self.Skill_Status
            }
            
    

## ROLE ##
class Role(db.Model):
    __tablename__ = 'role'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Role_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Role_Name = db.Column(db.String(100), nullable=False)
    Role_Responsibilities = db.Column(db.String(2000), nullable=False)

    def __init__(self, Role_ID,Role_Name, Role_Responsibilities):
        self.Role_ID= Role_ID
        self.Role_Name = Role_Name
        self.Role_Responsibilities = Role_Responsibilities
        

    def get_role_details(self):
        return {
            "Role_Name": self.Role_Name,
            "Role_Responsibilities": self.Role_Responsibilities
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
    def get_role_skill_mapping_details(self):
        return {
                "Role_ID": self.Role_ID,
                "Skill_ID": self.Skill_ID
            }
    
## Application ##
class Application(db.Model):
    __tablename__ = 'application'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Application_ID = db.Column(db.Integer, primary_key=True)
    Application_Date = db.Column(MyDateTime, nullable=False)
    Application_Status = db.Column(db.String(50), nullable=False)
    Staff_ID = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID', ondelete='CASCADE'))
    Listing_ID = db.Column(db.Integer, db.ForeignKey('role_listing.Listing_ID', ondelete='CASCADE'))

    staff = db.relationship('Staff', backref='applications')
    

    role_listing = db.relationship('RoleListing', backref='applications')
    #staff = db.relationship('Staff', backref='applications')
    #role = db.relationship('Role', backref='applications')
    
    def __init__(self,Application_Date, Application_Status, Staff_ID, Listing_ID):
        # self.Application_ID = Application_ID
        self.Application_Date = Application_Date
        self.Application_Status = Application_Status
        self.Staff_ID = Staff_ID
        self.Listing_ID = Listing_ID

    def get_application_details(self):
        return {
            "Application_ID": self.Application_ID,
            "Application_Date": self.Application_Date,
            "Application_Status": self.Application_Status,
            "Staff_ID": self.Staff_ID,
            "Listing_ID": self.Listing_ID
        }
    # specify how to represent our book object as a JSON string
    def get_all_application_details(self):
        current_role = Role.query.get(self.staff.Role_ID)
        return {
                    "Application_ID": self.Application_ID, 
                    "Application_Date": self.Application_Date,
                    "Application_Status": self.Application_Status,
                    "Staff_ID": self.Staff_ID,
                    "Listing_ID": self.Listing_ID,
                    "Staff_FName": self.staff.Staff_FName,  # Include Staff_FName
                    "Staff_LName": self.staff.Staff_LName,
                    "Staff_Current_Role": current_role.Role_Name if current_role else None,  # Include Staff_LName
                    
                    # "Skills": [skill.json() for skill in self.staff.skills]  # Include Staff's skills
                    "Skills": [{"Skill_ID": skill.skill.Skill_ID, "Skill_Name": skill.skill.Skill_Name} for skill in self.staff.skills],
                    "Role_Name": self.role_listing.role.Role_Name
                }

## Role_Listing ##
class RoleListing(db.Model):
    __tablename__ = 'role_listing'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Listing_ID = db.Column(db.Integer, primary_key=True)
    Deadline = db.Column(MyDateTime, nullable=False)
    Date_Posted = db.Column(MyDateTime, nullable=False)
    Country = db.Column(db.String(100), nullable=False)
    Hiring_Manager = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID', ondelete='CASCADE'), nullable=False)
    Role_ID = db.Column(db.Integer, db.ForeignKey('role.Role_ID', ondelete='CASCADE'), nullable=False)

    role = db.relationship('Role')
    #staff = db.relationship('Staff', backref='applications')
    #role = db.relationship("Role",back_populates="role_listing")
    
    def __init__(self, Deadline, Date_Posted, Country, Hiring_Manager, Role_ID):
        self.Deadline = Deadline
        self.Date_Posted = Date_Posted
        self.Country = Country
        self.Hiring_Manager = Hiring_Manager
        self.Role_ID = Role_ID

    def get_role_listing_details(self):
        return {
            "Listing_ID": self.Listing_ID,
            "Deadline": self.Deadline, 
            "Date_Posted": self.Date_Posted,
            "Country" : self.Country,
            "Hiring_Manager": self.Hiring_Manager,
            "Role_ID": self.Role_ID
        }