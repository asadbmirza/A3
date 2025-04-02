import datetime
from sqlalchemy import CheckConstraint, Date, Float, ForeignKey, Integer, String
from db import db
from sqlalchemy.orm import Mapped, mapped_column, aliased

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
            "primary_key": "user_id",
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
            "primary_key": "course_id",
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
            "primary_key": "coursework_id",
            "coursework_id": self.coursework_id,
            "coursework_name": self.coursework_name,
            "coursework_type": self.coursework_type,
            "course_id": self.course_id,
            "due_date": self.due_date.isoformat()
        }

class AssignedCoursework(db.Model):
    coursework_id: Mapped[int] = mapped_column(Integer, ForeignKey("coursework.coursework_id"), primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), primary_key=True)
    instructor_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    submission_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    mark: Mapped[float] = mapped_column(Float, nullable=True)

    def to_dict(self):
        return {
            "coursework_id": self.coursework_id,
            "student_id": self.student_id,
            "instructor_id": self.instructor_id,
            "submission_date": self.submission_date.isoformat(),
            "mark": self.mark
        }

class RemarkRequest(db.Model):
    remark_request_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    coursework_id: Mapped[int] = mapped_column(Integer, ForeignKey("coursework.coursework_id"), nullable=False)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    reason: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="Pending")
    
    __table_args__ = (
        CheckConstraint(
            "status IN ('Pending', 'Approved', 'Rejected')",
            name="check_status"
        ),
    )

    def to_dict(self):
        return {
            "primary_key": "remark_request_id",
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
    reviewed: Mapped[bool] = mapped_column(default=False)
    instructor_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)

    def to_dict(self):
        return {
            "primary_key": "feedback_id",
            "feedback_id": self.feedback_id,
            "teaching_likes": self.teaching_likes,
            "teaching_recommendations": self.teaching_recommendations,
            "lab_likes": self.lab_likes,
            "lab_recommendations": self.lab_recommendations,
            "reviewed": self.reviewed,
            "instructor_id" : self.instructor_id
        }

users_courses = db.Table(
    "users_courses",
    db.Column("user_id", db.Integer, db.ForeignKey("users.user_id"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("courses.course_id"), primary_key=True)
)

Instructors = aliased(Users)
Students = aliased(Users)