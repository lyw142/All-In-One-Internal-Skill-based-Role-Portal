'''
this file is to manage the database config settings 
'''

class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost:3306/spm' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False








