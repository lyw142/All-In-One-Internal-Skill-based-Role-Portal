from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import desc

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + \
                                            'root' + \
                                            '@localhost:3306/SPM'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                               'pool_recycle': 280}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class RoleListing(db.Model):
    __tablename__ = 'role_listing'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # Specify InnoDB engine for this table

    Listing_ID = db.Column(db.Integer, primary_key=True)
    Deadline = db.Column(db.Date, nullable=False)
    Date_Posted = db.Column(db.Date, nullable=False)
    Hiring_Manager = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID', ondelete='CASCADE'), nullable=False)
    Role_ID = db.Column(db.Integer, db.ForeignKey('role.Role_ID', ondelete='CASCADE'), nullable=False)
    
    def __init__(self, Listing_ID, Deadline, Date_Posted, Hiring_Manager, Role_ID):
        self.Listing_ID = Listing_ID
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

@app.route("/joblistings")
def findAllJobListings():
    job_listings = RoleListing.query.order_by(desc(RoleListing.Date_Posted)).all()

     # Check if there are any job listings
    if job_listings:
        # Convert the job listings to a list of dictionaries
        job_listings_list = [listing.to_json() for listing in job_listings]
        return jsonify({
            "data": job_listings_list
        }), 200
    else:
        return jsonify({
            "message": "No job listings found."
        }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
