"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""
from flask import Blueprint, request, jsonify
# from models import db, 
from models import db, Staff, Role, Staff, Skill, RoleSkillMapping, RoleListing
from sqlalchemy import desc
api = Blueprint('api', __name__)



@api.route("/createjoblisting", methods=['POST'])
def createListing():
    try:
        # Parse the JSON data from the request
        data = request.get_json()

        # Extract data from the JSON request
        deadline = data['Deadline']
        date_posted = data['Date_Posted']
        hiring_manager_id = data['Hiring_Manager']
        role_id = data['Role_ID']

        # Check if the Role and Hiring Manager exist
        role = Role.query.get(role_id)
        if not role:
            return jsonify({"message": "Role not found"}), 404

        # Create a new RoleListing object
        listing = RoleListing(
            Deadline=deadline,
            Date_Posted=date_posted,
            Hiring_Manager=hiring_manager_id,
            Role_ID=role_id
        )

        # Add the new listing to the database session and commit
        db.session.add(listing)
        db.session.commit()

        # Return a success message
        return jsonify({"message": "Role listing created successfully"}), 201

    except Exception as e:
        # Handle any exceptions that may occur during the process
        db.session.rollback()  # Rollback the transaction in case of an error
        return jsonify({"message": "Error creating role listing", "error": str(e)}), 500



@api.route("/joblistings")
def findAllJobListings():
    # Perform joins to retrieve role listings with Hiring Manager and Role Name
    query = (
        db.session.query(RoleListing, Staff.Staff_FName, Staff.Staff_LName, Role.Role_Name, Role.Role_Responsibilities, Role.Role_Requirements, Role.Salary)
        .join(Staff, RoleListing.Hiring_Manager == Staff.Staff_ID)
        .join(Role, RoleListing.Role_ID == Role.Role_ID)
        .order_by(desc(RoleListing.Date_Posted))
    )

    # Execute the query and retrieve the results
    results = query.all()

    # Convert the results into a JSON format
    role_listings_json = []
    for role_listing, hiring_manager_fname, hiring_manager_lname, role_name, role_responsibilities, role_requirements, salary in results:
        role_listing_data = {
            "Listing_ID": role_listing.Listing_ID,
            "Deadline": str(role_listing.Deadline),
            "Date_Posted": str(role_listing.Date_Posted),
            "Hiring_Manager": hiring_manager_fname + " " + hiring_manager_lname,
            "Role_Name": role_name,
            "Role_Responsibilities": role_responsibilities,
            "Role_Requirements": role_requirements,
            "Salary": salary,
            "Skills": retrieveAllSkillsFromRoleListing(role_listing.Role_ID)
        }
        role_listings_json.append(role_listing_data)

    return role_listings_json

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

    return skills_json

@api.route("/getRoleListing/<int:listing_id>")
def getRoleListing(listing_id):
    try:
        # Perform joins to retrieve role listings with Hiring Manager and Role Name for the specified Listing_ID
        query = (
            db.session.query(RoleListing, Staff.Staff_FName, Staff.Staff_LName, Role.Role_Name, Role.Role_Responsibilities, Role.Role_Requirements, Role.Salary)
            .join(Staff, RoleListing.Hiring_Manager == Staff.Staff_ID)
            .join(Role, RoleListing.Role_ID == Role.Role_ID)
            .filter(RoleListing.Listing_ID == listing_id)  # Filter by the specified Listing_ID
            .order_by(desc(RoleListing.Date_Posted))
        )

        # Execute the query and retrieve the results
        results = query.all()

        # Convert the results into a JSON format
        role_listings_json = []
        for role_listing, hiring_manager_fname, hiring_manager_lname, role_name, role_responsibilities, role_requirements, salary in results:
            role_listing_data = {
                "Listing_ID": role_listing.Listing_ID,
                "Deadline": str(role_listing.Deadline),
                "Date_Posted": str(role_listing.Date_Posted),
                "Hiring_Manager": hiring_manager_fname + " " + hiring_manager_lname,
                "Role_Name": role_name,
                "Role_Responsibilities": role_responsibilities,
                "Role_Requirements": role_requirements,
                "Salary": salary,
                "Skills": retrieveAllSkillsFromRoleListing(role_listing.Role_ID)
            }
            role_listings_json.append(role_listing_data)

        return jsonify(role_listings_json)

    except Exception as e:
        return jsonify({"message": "Error retrieving role listings", "error": str(e)}), 500

@api.route("/updateRoleListing/<int:listing_id>", methods=["POST"])
def updateRoleListing(listing_id):
    try:
        # Retrieve the role listing based on listing_id
        role_listing = RoleListing.query.get(listing_id)

        if not role_listing:
            return jsonify({"message": "Role listing not found"}), 404

        # Get the JSON data from the request
        data = request.get_json()

        # Update the role listing attributes
        role_listing.Deadline = data["Deadline"]

        # Fetch the corresponding Role object
        role = Role.query.get(role_listing.Role_ID)

        # Update the Role attributes
        if role:
            role.Role_Responsibilities = data["Role_Responsibilities"]
            role.Role_Requirements = data["Role_Requirements"]
        else:
            # Handle the case where the corresponding Role is not found
            return jsonify({"message": "Role not found"}), 404

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "Role listing updated successfully"})

    except Exception as e:
        return jsonify({"message": "Error updating role listing", "error": str(e)}), 500
