import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///assignment3.db"
db.init_app(app)

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

class Courses(db.Model):
    course_id: Mapped[int] = mapped_column(primary_key=True)
    course_name: Mapped[str] = mapped_column(nullable=False, unique=True)

class Coursework(db.Model):
    coursework_id: Mapped[int] = mapped_column(primary_key=True)
    coursework_name: Mapped[str] = mapped_column(nullable=False)
    coursework_type: Mapped[str] = mapped_column(nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.course_id"), nullable=False)
    due_date: Mapped[datetime.date] = mapped_column(Date)

class AssignedCoursework(db.Model):
    coursework_id: Mapped[int] = mapped_column(Integer, ForeignKey("coursework.coursework_id"), primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), primary_key=True)
    instructor_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    submission_date: Mapped[datetime.date] = mapped_column(Date)
    mark: Mapped[int] = mapped_column(Integer)

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

class Feedback(db.Model):
    feedback_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teaching_likes: Mapped[str] = mapped_column()
    teaching_recommendations: Mapped[str] = mapped_column()
    lab_likes: Mapped[str] = mapped_column()
    lab_recommendations: Mapped[str] = mapped_column()
    instructor_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)

users_courses = db.Table(
    "users_courses",
    db.Column("user_id", db.Integer, db.ForeignKey("users.user_id"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("courses.course_id"), primary_key=True)
)

with app.app_context():
    db.create_all()