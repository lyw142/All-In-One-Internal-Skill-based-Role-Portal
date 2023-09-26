from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import desc
from models import RoleListing,Role, Staff, RoleSkillMapping, Skill;

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + \
                                            'root' + \
                                            '@localhost:3306/SPM'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                               'pool_recycle': 280}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)
    
@app.route("/joblistings")
def findAllJobListings():
    # Perform joins to retrieve role listings with Hiring Manager and Role Name
    query = (
        db.session.query(RoleListing, Staff.Staff_FName, Staff.Staff_LName, Role.Role_Name, Role.Role_Description, Role.Salary)
        .join(Staff, RoleListing.Hiring_Manager == Staff.Staff_ID)
        .join(Role, RoleListing.Role_ID == Role.Role_ID)
        .order_by(desc(RoleListing.Date_Posted))
    )

    # Execute the query and retrieve the results
    results = query.all()

    # Convert the results into a JSON format
    role_listings_json = []
    for role_listing, hiring_manager_fname, hiring_manager_lname, role_name, role_description, salary in results:
        role_listing_data = {
            "Listing_ID": role_listing.Listing_ID,
            "Deadline": str(role_listing.Deadline),
            "Date_Posted": str(role_listing.Date_Posted),
            "Hiring_Manager": hiring_manager_fname + " " + hiring_manager_lname,
            "Role_Name": role_name,
            "Role_Description": role_description,
            "Salary": salary,
            "Skills": retrieveAllSkillsFromRoleListing(role_listing.Role_ID)
        }
        role_listings_json.append(role_listing_data)

    return role_listings_json;

def retrieveAllSkillsFromRoleListing(Role_ID):
    # Perform joins to retrieve role listings with Hiring Manager and Role Name
    query = (
        db.session.query(RoleSkillMapping, Skill.Skill_Name)
        .join(Role, RoleSkillMapping.Role_ID == Role.Role_ID)
        .join(Skill, RoleSkillMapping.Skill_ID == Skill.Skill_ID)
        .filter(Role.Role_ID == Role_ID)
    )

    # Execute the query and retrieve the results
    results = query.all()
    print(results)

    # Convert the results into a JSON format
    skills_json = []
    for skills_name in results:
        skills_json.append(skills_name.Skill_Name)

    return skills_json;

# @app.route("/joblistings")
# def findAllJobListings():
#     job_listings = RoleListing.query.order_by(desc(RoleListing.Date_Posted)).all()

#      # Check if there are any job listings
#     if job_listings:
#         # Convert the job listings to a list of dictionaries
#         job_listings_list = [listing.to_json() for listing in job_listings]
#         return jsonify({
#             "data": job_listings_list
#         }), 200
#     else:
#         return jsonify({
#             "message": "No job listings found."
#         }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
