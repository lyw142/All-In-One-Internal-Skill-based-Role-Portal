"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
# from models import db, 
from models import Staff_Skill, db, Staff, Role, Staff, Skill, RoleSkillMapping, RoleListing, Application
from sqlalchemy import and_, desc, func
from flask import Flask
from flask_cors import CORS
# import datetime
api = Blueprint('api', __name__)



@api.route("/createjoblisting", methods=['POST'])
def createListing():
    data = request.get_json()
    
    # Check if the Role_Name already exists in the database
    existing_role = Role.query.filter_by(Role_Name=data['Role_Name']).first()
    
    if existing_role:
        # Create a new RoleListing entry for the existing role
        role_listing = RoleListing(
            Deadline=data['Deadline'],
            Date_Posted=data['Date_Posted'],
            Country=data['Country'],
            Salary=data['Salary'],
            Hiring_Manager=data['Hiring_Manager'],
            Role_ID=existing_role.Role_ID  # Use the existing role's ID
        )
        db.session.add(role_listing)
        db.session.commit()
        
        return jsonify({"message": "Role already exists, new listing created."}), 200  # HTTP 200 OK status code
    else:
        new_role = Role(
            Role_Name=data['Role_Name'],
            Role_Responsibilities=data['Role_Responsibilities']
        )
        
        db.session.add(new_role)
        db.session.commit()

        new_role = Role.query.filter_by(Role_Name=data['Role_Name']).first()
        
        # Query the Skill table to get the Skill_ID for the given Skill_Name
        skill = Skill.query.filter_by(Skill_Name=data['Skill']).first()
        print(skill)

        if skill:
            skill_id = skill.Skill_ID
        else:
            # Create a new Skill object if the Skill_Name does not exist in the database
            new_skill = Skill(
                Skill_Name=data['Skill'],
                Skill_Desc= data['Skill_Desc'],
                Skill_Status = "Active"
            )
            db.session.add(new_skill)
            db.session.commit()

            # Retrieve the new Skill_ID
            skill_id = Skill.query.filter_by(Skill_Name=data['Skill']).first().Skill_ID

        new_role_skill = RoleSkillMapping(
            Skill_ID=skill_id,
            Role_ID=new_role.Role_ID
        )
        db.session.add(new_role_skill)
        db.session.commit()

        # Create a new RoleListing entry
        role_listing = RoleListing(
            Deadline=data['Deadline'],
            Date_Posted=data['Date_Posted'],
            Country = data['Country'],
            Salary = data['Salary'],
            Hiring_Manager=data['Hiring_Manager'],
            Role_ID=new_role.Role_ID
        )
        db.session.add(role_listing)
        db.session.commit()

        
        return jsonify({"message": "Role created successfully, Role_SKill mapped and New Listing created."}), 201  # HTTP 201 Created status code


    #  OLD CODE   
    # ----------------------------------------------
    # try:
    #     # Parse the JSON data from the request
    #     data = request.get_json()

    #     # Extract data from the JSON request
    #     deadline = data['Deadline']
    #     date_posted = data['Date_Posted']
    #     hiring_manager_id = data['Hiring_Manager']
    #     role_id = data['Role_ID']

    #     # Check if the Role and Hiring Manager exist
    #     role = Role.query.get(role_id)
    #     if not role:
    #         return jsonify({"message": "Role not found"}), 404

    #     # Create a new RoleListing object
    #     listing = RoleListing(
    #         Deadline=deadline,
    #         Date_Posted=date_posted,
    #         Hiring_Manager=hiring_manager_id,
    #         Role_ID=role_id
    #     )

    #     # Add the new listing to the database session and commit
    #     db.session.add(listing)
    #     db.session.commit()

    #     # Return a success message
    #     return jsonify({"message": "Role listing created successfully"}), 201

    # except Exception as e:
    #     # Handle any exceptions that may occur during the process
    #     db.session.rollback()  # Rollback the transaction in case of an error
    #     return jsonify({"message": "Error creating role listing", "error": str(e)}), 500



@api.route("/openjoblistings")
def findAllOpenJobListings():
    current_date = datetime.now()

    # Perform joins to retrieve role listings with Hiring Manager and Role Name
    query = (
        db.session.query(RoleListing, Staff.Staff_FName, Staff.Staff_LName, Role.Role_Name, Role.Role_Responsibilities)
        .join(Staff, RoleListing.Hiring_Manager == Staff.Staff_ID)
        .join(Role, RoleListing.Role_ID == Role.Role_ID)
        .filter(RoleListing.Deadline >= current_date)  # Filter by Deadline
        .order_by(desc(RoleListing.Date_Posted))
    )

    # Execute the query and retrieve the results
    results = query.all()

    # Convert the results into a JSON format
    role_listings_json = []
    for role_listing, hiring_manager_fname, hiring_manager_lname, role_name, role_responsibilities in results:
        result1, result2 = retrieveAllSkillsFromRoleListing(role_listing.Role_ID)
        role_listing_data = {
            "Listing_ID": role_listing.Listing_ID,
            "Deadline": str(role_listing.Deadline),
            "Date_Posted": str(role_listing.Date_Posted),
            "Hiring_Manager": hiring_manager_fname + " " + hiring_manager_lname,
            "Role_Name": role_name,
            "Role_Responsibilities": role_responsibilities,
            "Role_Requirements": result2,
            "Salary": role_listing.Salary,
            "Skills": result1
        }
        role_listings_json.append(role_listing_data)

    return jsonify(role_listings_json)

def retrieveAllSkillsFromRoleListing(Role_ID):
    # Perform joins to retrieve role listings with Hiring Manager and Role Name
    query = (
        db.session.query(RoleSkillMapping, Skill.Skill_Name, Skill.Skill_Desc)
        .join(Role, RoleSkillMapping.Role_ID == Role.Role_ID)
        .join(Skill, RoleSkillMapping.Skill_ID == Skill.Skill_ID)
        .filter(Role.Role_ID == Role_ID)
    )

    # Execute the query and retrieve the results
    results = query.all()

    # Convert the results into a JSON format
    skills_json = []
    skills_desc_json = []
    for skills_result in results:
        skills_json.append(skills_result.Skill_Name)
        skills_desc_json.append(skills_result.Skill_Desc)

    return skills_json,skills_desc_json

@api.route("/getRoleListing/<int:listing_id>")
def getRoleListing(listing_id):
    try:
        # Perform joins to retrieve role listings with Hiring Manager and Role Name for the specified Listing_ID
        query = (
            db.session.query(RoleListing, Staff.Staff_FName, Staff.Staff_LName, Role.Role_Name, Role.Role_Responsibilities)
            .join(Staff, RoleListing.Hiring_Manager == Staff.Staff_ID)
            .join(Role, RoleListing.Role_ID == Role.Role_ID)
            .filter(RoleListing.Listing_ID == listing_id)  # Filter by the specified Listing_ID
            .order_by(desc(RoleListing.Date_Posted))
        )

        # Execute the query and retrieve the results
        results = query.all()

        # Convert the results into a JSON format
        role_listings_json = []
        for role_listing, hiring_manager_fname, hiring_manager_lname, role_name, role_responsibilities in results:
            result1, result2 = retrieveAllSkillsFromRoleListing(role_listing.Role_ID)
            role_listing_data = {
                "Listing_ID": role_listing.Listing_ID,
                "Deadline": str(role_listing.Deadline),
                "Date_Posted": str(role_listing.Date_Posted),
                "Hiring_Manager": hiring_manager_fname + " " + hiring_manager_lname,
                "Role_Name": role_name,
                "Role_Responsibilities": role_responsibilities,
                "Role_Requirements": result2,
                "Salary": role_listing.Salary,
                "Skills": result1,
                "Country": role_listing.Country,
            }
            role_listings_json.append(role_listing_data)

        return jsonify(role_listings_json)

    except Exception as e:
        return jsonify({"message": "Error retrieving specific role listing", "error": str(e)}), 500

@api.route("/updateRoleListing/<int:listing_id>", methods=["POST"])
def updateRoleListing(listing_id):
    try:
        # Retrieve the role listing based on listing_id
        role_listing = RoleListing.query.get(listing_id)

        if not role_listing:
            return jsonify({"message": "Role listing not found"}), 404

        # Get the JSON data from the request
        data = request.get_json()

        role_listing.Deadline = data["Deadline"]
        role_listing.Country = data["Country"]
        role_listing.Salary = data["Salary"]
        skill_ids = data["AddedSkills"]
        remove_skill = data["RemovedSkills"] # array of skills id

        role = Role.query.get(role_listing.Role_ID)

        if role:
            role.Role_Responsibilities = data["Role_Responsibilities"]
        else:
            return jsonify({"message": "Role not found"}), 404


        for skill_id in skill_ids:
            role_skill_mapping = RoleSkillMapping(Role_ID=role_listing.Role_ID, Skill_ID=skill_id)

            db.session.add(role_skill_mapping)

        for skill_id in remove_skill:
            role_skill_mapping = RoleSkillMapping.query.filter_by(Role_ID=role_listing.Role_ID, Skill_ID=skill_id).first()
            if role_skill_mapping:
                db.session.delete(role_skill_mapping)

        db.session.commit()

        return jsonify({"message": "Role listing updated successfully"})

    except Exception as e:
        return jsonify({"message": "Error updating role listing", "error": str(e)}), 500

# filter and show closed listings
@api.route("/closedjoblistings")
def findClosedJobListings():
    current_date = datetime.now()

    # Perform joins to retrieve role listings with Hiring Manager and Role Name
    query = (
        db.session.query(RoleListing, Staff.Staff_FName, Staff.Staff_LName, Role.Role_Name, Role.Role_Responsibilities)
        .join(Staff, RoleListing.Hiring_Manager == Staff.Staff_ID)
        .join(Role, RoleListing.Role_ID == Role.Role_ID)
        .filter(RoleListing.Deadline < current_date)  # Filter by Deadline
        .order_by(desc(RoleListing.Date_Posted))
    )

    # Execute the query and retrieve the results
    results = query.all()

    # Convert the results into a JSON format
    role_listings_json = []
    for role_listing, hiring_manager_fname, hiring_manager_lname, role_name, role_responsibilities in results:
        result1, result2 = retrieveAllSkillsFromRoleListing(role_listing.Role_ID)
        role_listing_data = {
            "Listing_ID": role_listing.Listing_ID,
            "Deadline": str(role_listing.Deadline),
            "Date_Posted": str(role_listing.Date_Posted),
            "Hiring_Manager": hiring_manager_fname + " " + hiring_manager_lname,
            "Role_Name": role_name,
            "Role_Responsibilities": role_responsibilities,
            "Role_Requirements": result2,
            "Salary": role_listing.Salary,
            "Skills": result1
        }
        role_listings_json.append(role_listing_data)

    return jsonify(role_listings_json)

#skills api endpoint (clement)
@api.route("/skills", methods=['GET'])  # Define a new endpoint for retrieving skills
def getSkills():
    try:
        # Query the database to retrieve all skills
        skills = Skill.query.all()

        # Convert the skills to a list of dictionaries
        skills_data = [{"Skill_ID": skill.Skill_ID, "Skill_Name": skill.Skill_Name, "Skill_Desc" : skill.Skill_Desc, "Skill_Status": skill.Skill_Status} for skill in skills]

        # Return the skills as JSON response
        return jsonify(skills_data), 200

    except Exception as e:
        return jsonify({"message": "Error retrieving list of skills", "error": str(e)}), 500

#filter by skills

@api.route("/filterRoleListingBySkill/<list_of_skill_id>")
def filterRoleListingBySkill(list_of_skill_id):
    
    selected_skill_ids = list_of_skill_id.split(',')
    
    subquery = (
        db.session.query(RoleSkillMapping.Role_ID)
        .filter(RoleSkillMapping.Skill_ID.in_(selected_skill_ids))
        .group_by(RoleSkillMapping.Role_ID)
        .having(db.func.count(RoleSkillMapping.Skill_ID.distinct()) == len(selected_skill_ids))
        .subquery()
    )

    # Query the RoleListing table to find role listings based on the subquery
    role_listings = (
        db.session.query(
            RoleListing.Listing_ID,
            RoleListing.Deadline,
            RoleListing.Date_Posted,
            RoleListing.Role_ID,
            RoleListing.Salary,
            db.func.concat(Staff.Staff_FName, " ", Staff.Staff_LName).label("Hiring_Manager_Name"),
            Role.Role_Name,
            Role.Role_Responsibilities
        )
        .join(Staff, RoleListing.Hiring_Manager == Staff.Staff_ID)
        .join(Role, RoleListing.Role_ID == Role.Role_ID)
        .join(subquery, RoleListing.Role_ID == subquery.c.Role_ID)
        .order_by(db.desc(RoleListing.Date_Posted))
        .all()
    )


    # Convert the query results into JSON format
    role_listings_json = []

    for role_listing, deadline, date_posted, role_id, salary, hiring_manager_name, role_name, role_responsibilites in role_listings:
        result1, result2 = retrieveAllSkillsFromRoleListing(role_id)
        role_listing_data = {
            "Listing_ID": role_listing,
            "Deadline": str(deadline),
            "Date_Posted": str(date_posted),
            "Hiring_Manager": hiring_manager_name,
            "Role_Name": role_name,
            "Role_Responsibilities": role_responsibilites,
            "Role_Requirements" : result2,
            "Salary": salary,
            "Skills": result1
        }
        role_listings_json.append(role_listing_data)

    # Return the JSON response
    return jsonify(role_listings_json)

# @api.route("/filterRoleListingBySkills", methods=["POST"])
# def filter_role_listing_by_skills():
#     # Get the selected skills from the request
#     selected_skills = request.json.get("selectedSkills", [])

#     # Filter role listings based on selected skills
#     filtered_listings = [listing for listing in role_listings if all(skill in listing["Skills"] for skill in selected_skills)]

#     # Convert the filtered listings into a JSON format
#     role_listings_json = []
#     for listing in filtered_listings:
#         role_listing_data = {
#             "Listing_ID": listing["Listing_ID"],
#             "Deadline": listing["Deadline"].strftime("%Y-%m-%d"),
#             "Date_Posted": listing["Date_Posted"].strftime("%Y-%m-%d"),
#             "Hiring_Manager": listing["Hiring_Manager"],
#             "Role_Name": listing["Role_Name"],
#             "Role_Responsibilities": listing["Role_Responsibilities"],
#             "Role_Requirements": listing["Role_Requirements"],
#             "Salary": listing["Salary"],
#             "Skills": listing["Skills"],
#         }
#         role_listings_json.append(role_listing_data)

#     return jsonify(role_listings_json)

@api.route("/getStaffSkills/<int:staff_id>")
def getStaffSkills(staff_id):
    try:
        query = (
            db.session.query(Staff_Skill, Skill.Skill_Name)
            .join(Skill, Staff_Skill.Skill_ID == Skill.Skill_ID)
            .filter(Staff_Skill.Staff_ID == staff_id) 
        )

        # Execute the query and retrieve the results
        results = query.all()

        # Convert the results into a JSON format
        staff_json = []

        for staff_skill, skill_name in results:
            staff_skill_data = {
                "Skill_ID": staff_skill.Skill_ID,
                "Skill_Name": skill_name,
            }
            staff_json.append(staff_skill_data)

        return jsonify(staff_json)

    except Exception as e:
        return jsonify({"message": "Error retrieving Staff's Skill", "error": str(e)}), 500

#Login
@api.route("/login", methods=['POST'])
def login():
    try:
        data = request.get_json()

        query = (
            db.session.query(Staff)
            .filter(Staff.Email == data["Email"])
            .filter(Staff.Password == data["Password"])
            .all()
        )   

        if query:
            staff = query[0]  # Assuming only one staff member is found

            staff_data = {
                "Access_Rights": staff.Access_Rights,
                "Staff_ID": staff.Staff_ID,
                "Name": staff.Staff_FName + staff.Staff_LName
            }
            
            return jsonify(staff_data), 200
        else :
            return jsonify({
                "data": "Staff not found"
            }), 404

    except Exception as e:
        return jsonify({"message": "Error retrieving Staff information", "error": str(e)}), 500
    
"""
Apply for Open role - Create new application
"""
@api.route("/applyforopenrole", methods=["POST"])
def create_application():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d")

    try:
        # Get the application data from the request
        application_date = formatted_date
        application_status = "Received"
        staff_id = request.json["Staff_ID"]
        listing_id = request.json["Listing_ID"]


        # Check if Staff_ID already exists in the Application table
        existing_application = Application.query.filter_by(Staff_ID=staff_id,Listing_ID=listing_id).first()
        if existing_application:
            error_message = "You have already applied for this job role."
            return jsonify({"error": error_message}), 400
        
        # If its a new applcation, then create a new Application object
        application = Application(application_date, application_status, staff_id, listing_id)

        # Add the Application object to the database
        db.session.add(application)
        db.session.commit()

        # Return a success response
        return jsonify({"message": "Application successfully created"}), 201
    except KeyError as e:
        # Handle the error here
        return jsonify({"error": "Missing required key: " + str(e)}), 400
    except ValueError as e:
        # Handle the error here
        return jsonify({"error": "Invalid value: " + str(e)}), 400

"""
Endpoint to get all applications
"""
@api.route("/getapplications", methods=["GET"])
def get_all_applications():

    try:
        # Get all applications from the database
        applications = Application.query.all()

        # Convert the applications to JSON
        application_json = []
        for application in applications:
            application_json.append(application.json())

        # Return the JSON response
        return jsonify(application_json)
    except Exception as e:
        # Handle the error here
        return jsonify({"error": str(e)}), 500


