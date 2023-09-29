'''
this file is to manage the database config settings 
'''

class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/SPM' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False








