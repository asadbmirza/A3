import datetime
from flask import Flask, flash, jsonify, redirect, request, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, String, exc, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, aliased
from flask_bcrypt import Bcrypt

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///assignment3.db"
app.config["SECRET_KEY"] = "0903cf207352dcfe9f33a43f39b4c764b5b656266b4555a7276dac7b3dca926b"
db.init_app(app)
bcrypt = Bcrypt(app)

class Users(db.Model):
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    fname: Mapped[str] = mapped_column(nullable=False)
    lname: Mapped[str] = mapped_column(nullable=False)
    account_type: Mapped[str] = mapped_column(nullable=False)

    __table_args__ = (
        CheckConstraint(
            "account_type IN ('Instructor', 'Student')",
            name="check_account_type"
        ),
    )
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "fname": self.fname,
            "lname": self.lname,
            "account_type": self.account_type,
        }

class Courses(db.Model):
    course_id: Mapped[int] = mapped_column(primary_key=True)
    course_name: Mapped[str] = mapped_column(nullable=False, unique=True)
   
    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name
        }

class Coursework(db.Model):
    coursework_id: Mapped[int] = mapped_column(primary_key=True)
    coursework_name: Mapped[str] = mapped_column(nullable=False)
    coursework_type: Mapped[str] = mapped_column(nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.course_id"), nullable=False)
    due_date: Mapped[datetime.date] = mapped_column(Date)

    def to_dict(self):
        return {
            "coursework_id": self.coursework_id,
            "coursework_name": self.coursework_name,
            "coursework_type": self.coursework_type,
            "course_id": self.course_id,
            "due_date": self.due_date
        }

class AssignedCoursework(db.Model):
    coursework_id: Mapped[int] = mapped_column(Integer, ForeignKey("coursework.coursework_id"), primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), primary_key=True)
    instructor_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    submission_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    mark: Mapped[int] = mapped_column(Integer, nullable=True)

    def to_dict(self):
        return {
            "coursework_id": self.coursework_id,
            "student_id": self.student_id,
            "instructor_id": self.instructor_id,
            "submission_date": self.submission_date,
            "mark": self.mark
        }

class RemarkRequest(db.Model):
    remark_request_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    coursework_id: Mapped[int] = mapped_column(Integer, ForeignKey("coursework.coursework_id"), nullable=False)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    reason: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    
    __table_args__ = (
        CheckConstraint(
            "status IN ('Pending', 'Approved', 'Rejected')",
            name="check_status"
        ),
    )

    def to_dict(self):
        return {
            "remark_request_id": self.remark_request_id,
            "coursework_id": self.coursework_id,
            "student_id": self.student_id,
            "reason": self.reason,
            "status": self.status
        }

class Feedback(db.Model):
    feedback_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teaching_likes: Mapped[str] = mapped_column()
    teaching_recommendations: Mapped[str] = mapped_column()
    lab_likes: Mapped[str] = mapped_column()
    lab_recommendations: Mapped[str] = mapped_column()
    instructor_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)

    def to_dict(self):
        return {
            "feedback_id": self.feedback_id,
            "teaching_likes": self.teaching_likes,
            "lab_likes": self.teaching_recommendations,
            "lab_likes": self.reason,
            "lab_recommendations": self.lab_recommendations,
            "instructor_id" : self.instructor_id
        }

users_courses = db.Table(
    "users_courses",
    db.Column("user_id", db.Integer, db.ForeignKey("users.user_id"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("courses.course_id"), primary_key=True)
)

Instructors = aliased(Users)
Students = aliased(Users)

# with app.app_context():
#     db.create_all()


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
        

@app.route("/")
def home():
    return render_template("index.html")


def getAssignedCoursework():
    return db.session.execute(
        select(
            Students,
            Coursework.coursework_name,
            Coursework.coursework_type,
            Coursework.due_date,
            AssignedCoursework.mark,
            AssignedCoursework.submission_date
        )
        .join(AssignedCoursework, Coursework.coursework_id == AssignedCoursework.coursework_id)
        .join(Instructors, Instructors.user_id == AssignedCoursework.instructor_id) 
        .join(Students, Students.user_id == AssignedCoursework.student_id)
    ).all()

def formatCoursework(results):
    grouped = {}

    for student, coursework_name, coursework_type, due_date, mark, submission_date in results:
        sid = student.user_id

        if sid not in grouped:
            grouped[sid] = {
                "student_fname": student.fname,
                "student_lname": student.lname,
                "student_username": student.username,
                "coursework": []
            }

        grouped[sid]["coursework"].append({
            "coursework_name": coursework_name,
            "coursework_type": coursework_type,
            "due_date": due_date.isoformat(),
            "mark": mark,
            "submission_date": submission_date.isoformat() if submission_date else None
        })
    return list(grouped.values())

@app.route("/instructor-marks", methods=["GET", "POST"])
def instructorMarks():
    if session['account_type'] != "Instructor":
        return "forbidden"
    if request.method == "GET":
        results = getAssignedCoursework()
        return jsonify(formatCoursework(results))

if __name__ == "__main__":
    app.run(debug=True)