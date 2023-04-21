from flask import Flask, jsonify, request
from flask_cors import CORS
from os import environ
from config import db, SECRET_KEY
from dotenv import load_dotenv
from models.user import User
from models.personalDetails import PersonalDetails
from models.projects import Projects
from models.experiences import Experiences
from models.education import Education
from models.certificates import Certificates
from models.skills import Skills

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    app.config["SQLALCHEMY_ECHO"] = False
    app.secret_key = SECRET_KEY
    db.init_app(app)
    print("DB Initially Successfully")


    with app.app_context():
        # db.drop_all()  # when you make a mistake and want to change it then run the db.dropall()-> "Which delete the all tables" then comment out the db.dropall() and run again -> "Which create all the tables again"

        """ 
            Create an endpoint

            use form data to take the response from the user use username for indexing a user

                -Sign up user
                -add personal details
                -add experiences detsils
                -add projects detsils
                -add education detsils
                -add certificates detsils
                -add skills detsils
                
        """

        # sign up for the user

        @app.route('/sign_up', methods = ['POST'])
        def sign_up():
            data = request.form.to_dict(flat=True)

            new_user = User(
                username = data["username"]
            )
            db.session.add(new_user)
            db.session.commit()

            return "User added successfully"
        

        # Adding personal details

        @app.route('/add_personal_details', methods=['POST'])
        def add_personal_details():
            username = request.args.get('username')
            user = User.query.filter_by(username=username).first()
            """
                {
                    "name":"",
                    "email":"",
                    "phone":"",
                    "address":"",
                    "linkdin_link":""
                }
            """
            personal_details = request.get_json()

            new_personal_details = PersonalDetails(
                name = personal_details["name"],
                email = personal_details["email"],
                phone = personal_details["phone"],
                address = personal_details["address"],
                Linkdin_link = personal_details["Linkdin_link"],
                user_id = user.id
            )

            db.session.add(new_personal_details)
            db.session.commit()
            return "Personal details added successfully"
        # Adding experiences

        @app.route('/add_experience_details', methods=['POST'])
        def add_experience_details():
            username = request.args.get('username')
            user = User.query.filter_by(username=username).first()

            experience_details = request.get_json()

            for experience in experience_details["data"]:
                new_experience_details = Experiences(
                    comapny_name = experience["comapny_name"],
                    role = experience["role"],
                    role_desc = experience["role_desc"],
                    start_date = experience["start_date"],
                    end_date = experience["end_date"],
                    user_id = user.id
                )

                db.session.add(new_experience_details)
            db.session.commit()

            return jsonify(msg="Experience added successfully")

        # Adding projects

        @app.route('/add_projects_details', methods=['POST'])
        def add_projects_details():
            username = request.args.get('username')
            user = User.query.filter_by(username=username).first()
            projects_details = request.get_json()
            
            for project in projects_details["data"]:
                new_project = Projects(
                    name=project["name"],
                    desc=project["desc"],
                    start_date=project["start_date"],
                    end_date=project["end_date"],
                    user_id = user.id
                )
                db.session.add(new_project)
            db.session.commit()

            return jsonify(msg="Projects Added Successfully")
            
        # adding educatin
       
        """
        @app.route('/add_education_details', methods=['POST'])

        def add_education_details():
            username = request.args.get('username')
            user = User.query.filter_by(username=username).first()

            education_details = request.get_json()

        # adding certificates

        @app.route('/add_certificates_details', methods=['POST'])
        def add_certificates_details():
            username = request.args.get('username')
            user = User.query.filter_by(username=username).first()

            certificates_details = request.get_json()
        
        # adding skills

        @app.route('/add_silkks_details', methods=['POST'])
        def add_silkks_details():
            username = request.args.get('username')
            user = User.query.filter_by(username=username).first()

            silkks_details = request.get_json() 
        """
    

        @app.route('/get_resume', methods = ['GET'])
        def get_resume():
            username = request.args.get('username')
            user = User.query.filter_by(username=username).first()
            personalDetails = PersonalDetails.query.filter_by(user_id = user.id).first()
            experiences = Experiences.query.filter_by(user_id = user.id).all()
            projects = Projects.query.filter_by(user_id = user.id).all()

            

            experiences_data =[]
            projects_data =[]

            resume_data={
                "name":personalDetails.name,
                "email":personalDetails.email,
                "phone": personalDetails.phone,
                'address':personalDetails.address,
                "Linkdin_link":personalDetails.Linkdin_link
            }

            #add experience
            for exp in experiences:
                experiences_data.append(
                    {
                        "comapny_name":exp.comapny_name,
                        "role":exp.role,
                        "role_desc":exp.role_desc,
                        "start_date":exp.start_date,
                        "end_date":exp.end_date
                    }
                )
            resume_data["experiences"]=experiences_data

            # add projects

            for proj in projects:
                projects_data.append({
                    "name":proj.name,
                    "desc":proj.desc,
                    "start_date":proj.start_date,
                    "end_date":proj.end_date
                })
            resume_data["projects"]=projects_data

            return resume_data

        db.create_all()
        db.session.commit()
        return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)