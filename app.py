import datetime
from flask import Flask, flash, jsonify, redirect, request, render_template, session, url_for
from sqlalchemy import  exc, select
from db import db, bcrypt
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///assignment3.db"
app.config["SECRET_KEY"] = "0903cf207352dcfe9f33a43f39b4c764b5b656266b4555a7276dac7b3dca926b"
db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()

def authenticate(user: Users):
    session["user_id"] = user.user_id
    session["username"] = user.username
    session["fname"] = user.fname
    session["account_type"] = user.account_type
    return redirect(url_for("home"))

@app.before_request
def require_login():
    public_routes = ['signIn', 'register', 'static']
    if request.endpoint not in public_routes and 'user_id' not in session:
        return redirect(url_for('signIn'))
    
@app.route("/")
def home():
    return render_template("index.html")
    
@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "GET":
        if "user_id" in session:
            return redirect(url_for("home"))
        return render_template("authenticate.html", form_action="register")
    else:
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        fname = request.form["fname"]
        lname = request.form["lname"]
        account_type = request.form['accountType']

        user = Users(
                username=username,
                password=hashed_password,
                fname=fname,
                lname=lname,
                account_type=account_type
            )
        try:     
            db.session.add(user)
            db.session.commit()
            return authenticate(user)
        except exc.IntegrityError: 
            db.session.rollback()
            flash("Username already taken", "error")
            return render_template("authenticate.html", 
                                   form_action="register",
                                   username=username,
                                   password=password,
                                   fname=fname,
                                   lname=lname,
                                   account_type=account_type), 400
        except Exception as e:
            db.session.rollback()
            return "An error occurred", 500
    
@app.route('/sign-in', methods=["POST", "GET"])
def signIn():
    if request.method == "GET":
        if "user_id" in session:
            return redirect(url_for("home"))
        return render_template("authenticate.html", form_action="sign-in")
    else:
        username = request.form["username"]
        password = request.form["password"]

        try:     
            user = db.session.execute(select(Users).where(Users.username == username)).scalars().first()

            if user and bcrypt.check_password_hash(user.password, password):
                return authenticate(user)
            else:
                flash("Username or password is invalid", "error")
                return render_template("authenticate.html", 
                                       form_action="sign-in",
                                       username=username,
                                       password=password), 400
        except Exception as e:
            db.session.rollback()

            return str(e), 500

@app.route("/sign-out")
def signOut():
    session.clear()
    return redirect(url_for("signIn"))

@app.route("/syllabus")
def syllabus():
    return render_template("syllabus.html")

@app.route("/assignments")
def assignments():
    return render_template("assignments.html")

@app.route("/labs")
def labs():
    return render_template("labs.html")

@app.route("/notes")
def notes():
    return render_template("notes.html")

@app.route("/tests")
def tests():
    return render_template("tests.html")

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/team")
def team():
    return render_template("team.html")

def getInstructorCoursework():
    return db.session.query(Coursework).filter(
        AssignedCoursework.coursework_id == Coursework.coursework_id, 
        AssignedCoursework.instructor_id == session['user_id']).all()

def getStudentCoursework(coursework_id):
    return db.session.query(Users, AssignedCoursework.mark, AssignedCoursework.submission_date, Coursework.due_date, Coursework.coursework_name).filter(
        AssignedCoursework.coursework_id == coursework_id,
        Coursework.coursework_id == coursework_id, 
        AssignedCoursework.student_id == Users.user_id,
        AssignedCoursework.instructor_id == session["user_id"]).all()

@app.route("/api/instructor/marks")
def assignedCourseworkApi():
    if session.get('account_type') != "Instructor":
        return "forbidden"
    
    rawResults = getInstructorCoursework()
    results = []
    for r in rawResults:
        coursework = r.to_dict()
        coursework.pop("course_id")
        results.append(coursework)
    
    return jsonify({"results": results, "class": "Coursework", "header": "Assigned Coursework"})

@app.route("/api/instructor/marks/<int:coursework_id>", methods=["GET", "POST"])
def instructorMarksApi(coursework_id):
    if session.get('account_type') != "Instructor":
        return "forbidden"
    if request.method == "GET":
        rawResults = getStudentCoursework(coursework_id)
        if len(rawResults) == 0:
            return jsonify({"error": "No results found"}), 404
        results = []
        for student in rawResults:
            student_format = student[0].to_dict()
            student_format.pop("account_type")
            results.append({"user_id": student_format["user_id"],
                            "username": student_format["username"],
                            "fname": student_format["fname"],
                            "lname": student_format["lname"],
                            "primary_key": "user_id",
                            "mark": str(student[1]) + "%" if student[1] is not None else None, 
                            "submission_date": student[2].isoformat() if student[2] is not None else "Not Submitted",
                            "due_date": student[3].isoformat() if student[3] is not None else None})
        return jsonify({"results": results, "class": "Students", "header": student[4]})
    elif request.method == "POST":
        data = request.get_json()
        student_id = data.get("student_id")
        mark = data.get("mark")

        if not student_id or not mark:
            return jsonify({"error": "Invalid input"}), 400 # Did research on the diff types of http errors

        student_coursework  = db.session.query(AssignedCoursework).join(Users, Users.user_id == AssignedCoursework.student_id).filter(
            Users.user_id == student_id,
            AssignedCoursework.coursework_id == coursework_id,
        ).first()
        if student_coursework :
            student_coursework.mark = float(mark)
            db.session.commit()
            return jsonify({"success": True}), 200
        
        return jsonify({"error": "User not found or role mismatch"}), 404
    
@app.route("/instructor/marks")
@app.route("/instructor/marks/<int:coursework_id>")
def instructorMarks(coursework_id = None):
    if session.get('account_type') != "Instructor":
        return "forbidden"
    
    return render_template("instructorTable.html")    

@app.route("/api/instructor/feedback", methods=["GET", "POST"])
def instructorFeedbackApi(feedback_id = None):
    if session.get('account_type') != "Instructor":
        return "forbidden"
    
    if request.method == "GET":
        results = db.session.query(Feedback).filter(
            Feedback.instructor_id == session['user_id'],
        ).all()
        feedbacks = []
        for feedback in results:
            feedback_format = feedback.to_dict()
            if feedback_format["reviewed"] != 1:
                feedbacks.append(feedback_format)
        return jsonify({"results": feedbacks, "class": "Feedback", "header": "Feedback"}) 
    elif request.method == "POST":
        data = request.get_json()
        reviewed = data.get("reviewed")
        feedback_id = data.get("feedback_id")
        
        if not reviewed or not feedback_id:
            return jsonify({"error": "Invalid input"}), 400

        results = db.session.query(Feedback).filter(
            Feedback.instructor_id == session['user_id'],
            Feedback.feedback_id == feedback_id
        ).first()
        if results:
            results.reviewed = reviewed
            db.session.commit()
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Feedback not found"}), 404

@app.route("/instructor/feedback")
def instructorFeedback():
    if session.get('account_type') != "Instructor":
        return "forbidden"
    
    return render_template("instructorTable.html")

@app.route("/api/instructor/remark-requests", methods=["GET", "POST"])
def instructorRemarkRequestsApi(remark_request_id = None):
    if session.get('account_type') != "Instructor":
        return "forbidden"
    
    if request.method == "GET":
        results = db.session.query(RemarkRequest, Users.fname, Users.lname, Coursework.coursework_name, AssignedCoursework.mark).filter(
            RemarkRequest.coursework_id == AssignedCoursework.coursework_id,
            AssignedCoursework.instructor_id == session['user_id'],
            RemarkRequest.student_id == Users.user_id,
            RemarkRequest.coursework_id == Coursework.coursework_id,
            AssignedCoursework.student_id == RemarkRequest.student_id,
        ).distinct().all()
        requests = []
        for result in results:
            print(result)
            request_format = result[0].to_dict()
            request_format["student_name"] = result[1] + " " + result[2]
            request_format["coursework_name"] = result[3]
            request_format["mark"] = result[4]
            requests.append(request_format)
        return jsonify({"results": requests, "class": "RemarkRequest", "header": "Remark Requests"}) 
    elif request.method == "POST":
        data = request.get_json()
        remark_request_id = data.get("remark_request_id")
        status = data.get("status")
        updated_mark = data.get("mark")
        
        if not remark_request_id or not status:
            return jsonify({"error": "Invalid input"}), 400

        remark_request = db.session.query(RemarkRequest).filter(
            RemarkRequest.remark_request_id == remark_request_id
        ).first()

        if not remark_request:
            return jsonify({"error": "Remark Request not found"}), 404
        
        if status == "Approved":
            assignment = db.session.query(AssignedCoursework).filter(
                AssignedCoursework.coursework_id == remark_request.coursework_id,
                AssignedCoursework.student_id == remark_request.student_id,
                AssignedCoursework.instructor_id == session['user_id']
            ).first()

            if not assignment:
                return jsonify({"error": "Assignment not found"}), 404
            assignment.mark = updated_mark
        
        remark_request.status = status
        db.session.commit()
        return jsonify({"success": True}), 200

@app.route("/instructor/remark-requests")
def instructorRemarkRequests():
    if session.get('account_type') != "Instructor":
        return "forbidden"
    
    return render_template("instructorTable.html")



if __name__ == "__main__":
    app.run(debug=True)