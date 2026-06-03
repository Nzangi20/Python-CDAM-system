from __future__ import annotations

import csv
import io
import json
from datetime import UTC, datetime
from functools import wraps
from pathlib import Path

from flask import Flask, flash, jsonify, make_response, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from seed_data import SESSIONS
from utils import chatbot_reply, compute_streak, parse_quiz, render_markdown, slugify

import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
# Load .env file from project root if it exists
load_dotenv(BASE_DIR.parent / ".env")

FRONTEND_DIR = BASE_DIR.parent / "frontend"
DB_PATH = BASE_DIR / "cdam.db"
UPLOADS_DIR = FRONTEND_DIR / "static" / "uploads" / "notes"
ALLOWED_EXTENSIONS = {
    ".pdf", ".doc", ".docx", ".txt", ".md",
    ".csv", ".zip", ".ipynb", ".pptx", ".ppt",
    ".png", ".jpg", ".jpeg", ".gif", ".svg",
    ".mp4", ".webm", ".xlsx", ".xls",
}

app = Flask(
    __name__,
    template_folder=str(FRONTEND_DIR / "templates"),
    static_folder=str(FRONTEND_DIR / "static"),
)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-in-production")
db_url = os.environ.get("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/cdam_lms").strip()
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Automatically apply secure SSL settings when deploying to cloud providers
if "aivencloud.com" in db_url or "railway" in db_url or "supabase" in db_url:
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {
            "ssl": {
                "ssl_mode": "REQUIRED"
            }
        }
    }
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

CDAM_LOGO = "assets/cdam/cdam-logo-clear.png"
CHUKA_LOGO = "assets/cdam/chuka-uni-logo-HD-1.jpg"


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    reg_number = db.Column(db.String(100), unique=True, nullable=True, index=True)
    avatar = db.Column(db.String(500), nullable=True)
    auth_provider = db.Column(db.String(50), default="local")
    study_level = db.Column(db.String(30), default="Beginner")
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_suspended = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

    @property
    def role(self) -> str:
        return "admin" if self.is_admin else "student"


class Session(db.Model):
    __tablename__ = "sessions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    objectives = db.Column(db.Text, nullable=False)
    expected_outcomes = db.Column(db.Text, nullable=True)
    learning_notes = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    code_examples = db.Column(db.Text, nullable=False)
    resources = db.Column(db.Text, nullable=False)
    notes_file_path = db.Column(db.String(500), nullable=True)
    video_url = db.Column(db.String(500), nullable=True)
    quiz_json = db.Column(db.Text, nullable=False, default="[]")
    duration = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    display_order = db.Column(db.Integer, nullable=False)
    published = db.Column(db.Boolean, default=True)


class UserProgress(db.Model):
    __tablename__ = "user_progress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False, index=True)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    progress_percentage = db.Column(db.Integer, default=0)


class QuizResult(db.Model):
    __tablename__ = "quiz_results"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False)
    answers = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))


class Bookmark(db.Model):
    __tablename__ = "bookmarks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))


class LessonView(db.Model):
    __tablename__ = "lesson_views"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False, index=True)
    viewed_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    role = db.Column(db.String(30), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))


class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_by_admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))


class DiscussionComment(db.Model):
    __tablename__ = "discussion_comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    approved = db.Column(db.Boolean, default=True)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))


class ExamAttempt(db.Model):
    __tablename__ = "exam_attempts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False, index=True)
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    submitted_at = db.Column(db.DateTime, nullable=True)
    score = db.Column(db.Integer, default=0)
    passed = db.Column(db.Boolean, default=False)
    answers_json = db.Column(db.Text, nullable=False, default="{}")
    question_order_json = db.Column(db.Text, nullable=False, default="[]")
    integrity_flags_json = db.Column(db.Text, nullable=False, default="{}")
    is_flagged = db.Column(db.Boolean, default=False)


class Exam(db.Model):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Integer, default=30)
    passing_score = db.Column(db.Integer, default=50)
    exam_type = db.Column(db.String(50), default="mixed")
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    attempt_limit = db.Column(db.Integer, default=1)
    randomize_questions = db.Column(db.Boolean, default=True)
    randomize_options = db.Column(db.Boolean, default=True)
    one_device_only = db.Column(db.Boolean, default=True)
    proctoring_enabled = db.Column(db.Boolean, default=False)
    published = db.Column(db.Boolean, default=False)
    study_level = db.Column(db.String(30), default="Beginner", nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))


class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False, index=True)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(30), default="mcq")
    options = db.Column(db.Text, default="[]")
    correct_answer = db.Column(db.Text, nullable=True)
    marks = db.Column(db.Integer, default=1)


class ExamAttemptRecord(db.Model):
    __tablename__ = "exam_attempt_records"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False, index=True)
    score = db.Column(db.Integer, default=0)
    submitted_at = db.Column(db.DateTime, nullable=True)
    answers_json = db.Column(db.Text, default="{}")
    violation_count = db.Column(db.Integer, default=0)
    suspicious_score = db.Column(db.Integer, default=0)
    status = db.Column(db.String(30), default="in_progress")
    ip_address = db.Column(db.String(100), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

    exam = db.relationship("Exam", backref="attempt_records")

    @property
    def completed_at(self):
        return self.submitted_at

    @property
    def attempt_number(self):
        # Dynamically calculate the attempt index for this exam and user
        attempts = ExamAttemptRecord.query.filter_by(
            user_id=self.user_id, exam_id=self.exam_id
        ).order_by(ExamAttemptRecord.created_at.asc()).all()
        try:
            return attempts.index(self) + 1
        except ValueError:
            return 1



class IntegrityLog(db.Model):
    __tablename__ = "integrity_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False, index=True)
    violation_type = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(30), default="warning")
    details = db.Column(db.Text, default="")
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(UTC))


@app.context_processor
def inject_globals():
    sessions = Session.query.filter_by(published=True).order_by(Session.display_order).all()
    return {
        "cdam_logo": url_for("static", filename=CDAM_LOGO),
        "chuka_logo": url_for("static", filename=CHUKA_LOGO),
        "nav_sessions": sessions,
        "render_markdown": render_markdown,
        "check_session_access": check_session_access,
    }


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))


def log_activity(action: str, details: str = "") -> None:
    if current_user.is_authenticated:
        user_id = current_user.id
        role = current_user.role
    else:
        user_id = None
        role = "guest"
    db.session.add(ActivityLog(user_id=user_id, role=role, action=action, details=details))
    db.session.commit()


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Admin access is required.", "error")
            return redirect(url_for("student_dashboard"))
        return view(*args, **kwargs)

    return wrapped


def student_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        if current_user.is_admin:
            flash("Admins should use the admin dashboard.", "error")
            return redirect(url_for("admin_panel"))
        if current_user.is_suspended:
            logout_user()
            flash("Your account has been suspended. Contact support.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def check_session_access(user, display_order):
    if not user or not hasattr(user, "is_authenticated") or not user.is_authenticated:
        return False
    if user.is_admin:
        return True
    level = getattr(user, "study_level", "Beginner")
    if display_order <= 10:
        return True
    else:
        return level in ("Intermediate", "Professional")



def seed_sessions() -> None:
    seeded_slugs = {item["slug"] for item in SESSIONS}
    obsolete_sessions = Session.query.filter(~Session.slug.in_(seeded_slugs)).all()
    for obs in obsolete_sessions:
        UserProgress.query.filter_by(session_id=obs.id).delete()
        QuizResult.query.filter_by(session_id=obs.id).delete()
        Bookmark.query.filter_by(session_id=obs.id).delete()
        LessonView.query.filter_by(session_id=obs.id).delete()
        DiscussionComment.query.filter_by(session_id=obs.id).delete()
        db.session.delete(obs)
    db.session.commit()

    for idx, item in enumerate(SESSIONS, start=1):
        session_obj = Session.query.filter_by(slug=item["slug"]).first()
        if not session_obj:
            session_obj = Session(
                title=item["title"],
                slug=item["slug"],
                description=item["description"],
                content=item["content"],
                objectives=item["objectives"],
                expected_outcomes=item.get("expected_outcomes", ""),
                learning_notes=item.get("learning_notes", ""),
                instructions=item.get("instructions", ""),
                code_examples=item["code_examples"],
                resources=item["resources"],
                quiz_json=json.dumps(item.get("quiz", [])),
                duration=item["duration"],
                difficulty=item["difficulty"],
                display_order=idx,
                published=True,
            )
            db.session.add(session_obj)
        else:
            session_obj.title = item["title"]
            session_obj.description = item["description"]
            session_obj.content = item["content"]
            session_obj.objectives = item["objectives"]
            session_obj.expected_outcomes = item.get("expected_outcomes", "")
            session_obj.learning_notes = item.get("learning_notes", "")
            session_obj.instructions = item.get("instructions", "")
            session_obj.code_examples = item["code_examples"]
            session_obj.resources = item["resources"]
            session_obj.quiz_json = json.dumps(item.get("quiz", []))
            session_obj.duration = item["duration"]
            session_obj.difficulty = item["difficulty"]
            session_obj.display_order = idx
    db.session.commit()


def get_user_progress_map(user_id: int) -> dict[int, UserProgress]:
    rows = UserProgress.query.filter_by(user_id=user_id).all()
    return {row.session_id: row for row in rows}


def track_lesson_view(user_id: int, session_id: int) -> None:
    db.session.add(LessonView(user_id=user_id, session_id=session_id))
    db.session.commit()


def dashboard_context(user_id: int):
    sessions = Session.query.filter_by(published=True).order_by(Session.display_order).all()
    progress_map = get_user_progress_map(user_id)
    
    user = db.session.get(User, user_id)
    study_level = getattr(user, "study_level", "Beginner")
    if study_level == "Beginner":
        total_sessions = 10
    else:
        total_sessions = 20

    sessions = sessions[:total_sessions]

    completed = [s for s in sessions if progress_map.get(s.id) and progress_map[s.id].completed]
    completed_count = min(len(completed), total_sessions)
    progress_pct = int((completed_count / total_sessions) * 100) if total_sessions else 0
    remaining = [s for s in sessions if s.id not in progress_map or not progress_map[s.id].completed]

    next_session = remaining[0] if remaining else None
    completed_dates = [
        progress_map[s.id].completed_at.date()
        for s in completed
        if progress_map[s.id].completed_at
    ]
    streak = compute_streak(completed_dates)

    recent_views = (
        LessonView.query.filter_by(user_id=user_id)
        .order_by(LessonView.viewed_at.desc())
        .limit(8)
        .all()
    )
    recent_session_ids = []
    recent_sessions = []
    for view in recent_views:
        if view.session_id not in recent_session_ids:
            recent_session_ids.append(view.session_id)
            session = db.session.get(Session, view.session_id)
            if session:
                recent_sessions.append(session)

    bookmark_rows = Bookmark.query.filter_by(user_id=user_id).all()
    bookmark_ids = {row.session_id for row in bookmark_rows}
    bookmarked = [s for s in sessions if s.id in bookmark_ids]

    quiz_scores = QuizResult.query.filter_by(user_id=user_id).order_by(QuizResult.created_at.desc()).all()
    chart_labels = [s.title[:18] + "..." if len(s.title) > 18 else s.title for s in sessions]
    chart_values = []
    for session in sessions:
        result = next((q for q in quiz_scores if q.session_id == session.id), None)
        chart_values.append(result.score if result else 0)

    certificate_ready = completed_count == total_sessions and total_sessions > 0
    notifications = Notification.query.filter(
        db.or_(Notification.user_id.is_(None), Notification.user_id == user_id)
    ).order_by(Notification.created_at.desc()).limit(5).all()
    exam_attempts = ExamAttemptRecord.query.filter_by(user_id=user_id).order_by(ExamAttemptRecord.created_at.desc()).all()
    exam_avg = round(
        (sum(attempt.score for attempt in exam_attempts) / len(exam_attempts)) if exam_attempts else 0,
        2,
    )

    return {
        "sessions": sessions,
        "progress_map": progress_map,
        "completed_count": completed_count,
        "total_sessions": total_sessions,
        "progress_pct": progress_pct,
        "remaining_count": len(remaining),
        "next_session": next_session,
        "streak": streak,
        "recent_sessions": recent_sessions[:4],
        "bookmarked": bookmarked,
        "certificate_ready": certificate_ready,
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "notifications": notifications,
        "exam_avg": exam_avg,
        "exam_attempts": exam_attempts[:5],
    }


def admin_dashboard_context():
    users_count = User.query.filter_by(is_admin=False).count()
    active_users = ActivityLog.query.filter(
        ActivityLog.created_at >= datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
    ).with_entities(ActivityLog.user_id).distinct().count()
    completion_count = UserProgress.query.filter_by(completed=True).count()
    avg_quiz_score = db.session.query(db.func.avg(QuizResult.score)).scalar() or 0
    most_viewed = (
        db.session.query(Session.title, db.func.count(LessonView.id).label("views"))
        .join(LessonView, LessonView.session_id == Session.id)
        .group_by(Session.id)
        .order_by(db.desc("views"))
        .limit(5)
        .all()
    )
    recent_activities = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(10).all()
    session_progress = (
        db.session.query(Session.title, db.func.count(UserProgress.id))
        .outerjoin(UserProgress, UserProgress.session_id == Session.id)
        .group_by(Session.id)
        .order_by(Session.display_order)
        .all()
    )
    exam_stats = ExamAttemptRecord.query.order_by(ExamAttemptRecord.created_at.desc()).limit(20).all()
    suspicious_count = IntegrityLog.query.count()
    return {
        "users_count": users_count,
        "active_users": active_users,
        "completion_count": completion_count,
        "avg_quiz_score": round(float(avg_quiz_score), 2),
        "most_viewed": most_viewed,
        "recent_activities": recent_activities,
        "session_progress": session_progress,
        "published_count": Session.query.filter_by(published=True).count(),
        "notifications": Notification.query.order_by(Notification.created_at.desc()).limit(8).all(),
        "comments": DiscussionComment.query.order_by(DiscussionComment.created_at.desc()).limit(12).all(),
        "users": User.query.order_by(User.created_at.desc()).all(),
        "sessions": Session.query.order_by(Session.display_order).all(),
        "exam_attempts": exam_stats,
        "suspicious_count": suspicious_count,
        "exams": Exam.query.order_by(Exam.created_at.desc()).all(),
    }


@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    difficulty = request.args.get("difficulty", "").strip()

    sessions_q = Session.query.filter_by(published=True)
    if query:
        like = f"%{query}%"
        sessions_q = sessions_q.filter(db.or_(Session.title.ilike(like), Session.description.ilike(like)))
    if difficulty:
        sessions_q = sessions_q.filter(Session.difficulty == difficulty)

    sessions = sessions_q.order_by(Session.display_order).all()
    return render_template(
        "index.html",
        sessions=sessions,
        query=query,
        difficulty=difficulty,
        difficulties=["Beginner", "Intermediate", "Advanced"],
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        reg_number = request.form.get("reg_number", "").strip().upper()
        password = request.form.get("password", "")
        study_level = request.form.get("study_level", "Beginner").strip() or "Beginner"
        if not all([name, reg_number, password]):
            flash("All fields are required.", "error")
            return redirect(url_for("register"))
        if User.query.filter_by(reg_number=reg_number).first():
            flash("An account with this registration number already exists.", "error")
            return redirect(url_for("register"))
        user = User(
            name=name,
            email=f"{reg_number.replace('/', '_')}@cdam.local",
            reg_number=reg_number,
            password_hash=generate_password_hash(password),
            avatar=CDAM_LOGO,
            study_level=study_level,
            is_admin=False,
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        log_activity("student.register", f"Reg={reg_number}, level={study_level}")
        flash("Welcome to CDAM! Your learning journey starts now.", "success")
        return redirect(url_for("student_dashboard"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "")
        # Query check for either email or reg_number (case insensitive for email, exact or uppercase match for reg_number)
        user = User.query.filter(
            db.or_(
                User.reg_number == identifier.upper(),
                User.reg_number == identifier,
                User.email == identifier.lower()
            )
        ).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid registration number/email or password.", "error")
            return redirect(url_for("login"))
        if user.is_suspended:
            flash("This account is suspended. Contact administrator.", "error")
            return redirect(url_for("login"))
        login_user(user)
        log_activity("auth.login")
        return redirect(url_for("admin_panel" if user.is_admin else "student_dashboard"))
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    log_activity("auth.logout")
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    return redirect(url_for("admin_panel" if current_user.is_admin else "student_dashboard"))


@app.route("/student/dashboard")
@login_required
@student_required
def student_dashboard():
    ctx = dashboard_context(current_user.id)
    return render_template("dashboard.html", **ctx)


@app.route("/resources")
@login_required
def resources():
    sessions = Session.query.filter_by(published=True).order_by(Session.display_order).all()
    return render_template("resources.html", sessions=sessions)


@app.route("/exams")
@login_required
@student_required
def exams_dashboard():
    now = datetime.now(UTC)
    exams = Exam.query.filter_by(published=True, study_level=current_user.study_level).all()
    upcoming = [e for e in exams if e.start_time and e.start_time > now]
    available = [
        e
        for e in exams
        if (not e.start_time or e.start_time <= now) and (not e.end_time or e.end_time >= now)
    ]
    attempts = ExamAttemptRecord.query.filter_by(user_id=current_user.id).order_by(
        ExamAttemptRecord.created_at.desc()
    ).all()
    return render_template("exams_dashboard.html", upcoming=upcoming, available=available, attempts=attempts)


@app.route("/student/profile", methods=["GET", "POST"])
@login_required
@student_required
def student_profile():
    if request.method == "POST":
        current_user.name = request.form.get("name", current_user.name).strip()
        current_user.avatar = request.form.get("avatar", current_user.avatar).strip() or current_user.avatar
        current_user.study_level = request.form.get("study_level", current_user.study_level)
        new_password = request.form.get("new_password", "").strip()
        if new_password:
            current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        log_activity("student.profile.updated")
        flash("Profile updated.", "success")
        return redirect(url_for("student_profile"))
    return render_template("student_profile.html")


@app.route("/certificate")
@login_required
@student_required
def certificate():
    ctx = dashboard_context(current_user.id)
    if not ctx["certificate_ready"]:
        flash("Complete all sessions to unlock your certificate.", "error")
        return redirect(url_for("student_dashboard"))
    return render_template("certificate.html", user=current_user, completed_at=datetime.now(UTC))


@app.route("/session/<slug>")
@login_required
def session_detail(slug: str):
    session = Session.query.filter_by(slug=slug, published=True).first_or_404()
    if not check_session_access(current_user, session.display_order):
        required_level = "Intermediate" if session.display_order <= 10 else "Professional"
        flash(f"Session '{session.title}' notes and materials are restricted to {required_level} level students. Please upgrade your profile level to access.", "error")
        return redirect(url_for("resources"))
        
    progress = UserProgress.query.filter_by(user_id=current_user.id, session_id=session.id).first()
    completed = bool(progress and progress.completed)
    bookmark = Bookmark.query.filter_by(user_id=current_user.id, session_id=session.id).first()
    quiz = parse_quiz(session.quiz_json)
    quiz_result = QuizResult.query.filter_by(user_id=current_user.id, session_id=session.id).first()
    comments = DiscussionComment.query.filter_by(session_id=session.id, approved=True).order_by(
        DiscussionComment.created_at.desc()
    ).all()
    track_lesson_view(current_user.id, session.id)
    log_activity("student.session.view", session.slug)
    return render_template(
        "session_detail.html",
        session=session,
        completed=completed,
        bookmarked=bool(bookmark),
        quiz=quiz,
        quiz_result=quiz_result,
        comments=comments,
        latest_exam_attempt=None,
        show_quiz=False,
        show_exam=False,
    )


@app.route("/session/<int:session_id>/download")
@login_required
def download_notes(session_id: int):
    from flask import send_from_directory
    session = db.session.get(Session, session_id)
    if not session or not session.notes_file_path:
        flash("Notes file not found.", "error")
        return redirect(request.referrer or url_for("resources"))
    if not check_session_access(current_user, session.display_order):
        flash("Access to this note/revision material is restricted for your experience level.", "error")
        return redirect(request.referrer or url_for("resources"))
    
    filename = session.notes_file_path.split("/")[-1]
    return send_from_directory(UPLOADS_DIR, filename, as_attachment=False)


@app.route("/session/<int:session_id>/view")
@login_required
def view_notes(session_id: int):
    session = db.session.get(Session, session_id)
    if not session or not session.notes_file_path:
        flash("Notes file not found.", "error")
        return redirect(request.referrer or url_for("resources"))
    if not check_session_access(current_user, session.display_order):
        flash("Access to this note/revision material is restricted for your experience level.", "error")
        return redirect(request.referrer or url_for("resources"))
    return render_template("view_notes.html", session=session)


@app.route("/api/run-code", methods=["POST"])
@login_required
def run_code():
    import subprocess
    import sys
    payload = request.get_json(silent=True) or {}
    code = payload.get("code", "")
    if not code.strip():
        return jsonify({"output": "", "error": "No code provided."})
    
    try:
        # Run code in a subprocess using Python with a 5 second timeout
        process = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=5.0
        )
        return jsonify({
            "output": process.stdout,
            "error": process.stderr,
            "exit_code": process.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            "output": "",
            "error": "Execution timed out (5 seconds limit)."
        })
    except Exception as e:
        return jsonify({
            "output": "",
            "error": f"Internal execution error: {str(e)}"
        })


def generate_ai_response(action: str, query: str, code: str, error: str, session: Session) -> str:
    import random
    import re
    title = session.title
    objectives = session.objectives
    outcomes = session.expected_outcomes or ""
    learning_notes = session.learning_notes or ""
    
    if action == "debug":
        if not error:
            return "Your code executed successfully without errors! Great job."
        msg = f"### 🔍 AI Error Debugger\n"
        if "SyntaxError" in error:
            msg += f"It looks like there is a **Syntax Error** in your code.\n\n"
            msg += f"**What this means:** Python couldn't parse your code because of a typo or formatting mistake. Check for:\n"
            msg += f"- Missing closing parentheses `()`, brackets `[]`, or braces `{{}}`.\n"
            msg += f"- Missing colon `:` at the end of `if`, `for`, `def`, or `else` lines.\n"
            msg += f"- Unmatched or unclosed quotes (`'` or `\"`).\n\n"
        elif "NameError" in error:
            match = re.search(r"name '(\w+)' is not defined", error)
            name = f"`{match.group(1)}`" if match else "a variable or function"
            msg += f"It looks like there is a **Name Error** in your code.\n\n"
            msg += f"**What this means:** You are trying to use {name} before defining or importing it. Check if you misspelled it or forgot to assign it a value.\n\n"
        elif "TypeError" in error:
            msg += f"It looks like there is a **Type Error** in your code.\n\n"
            msg += f"**What this means:** You tried to perform an operation on incompatible types (for example, adding a string to an integer, or calling something that isn't a function).\n\n"
        elif "IndexError" in error:
            msg += f"It looks like there is an **Index Error** in your code.\n\n"
            msg += f"**What this means:** You are trying to access an element of a list or array at an index that doesn't exist (e.g. accessing index 5 in a list of size 3).\n\n"
        else:
            msg += f"Python reported the following error:\n`{error}`\n\n"
        
        msg += f"**How to Fix:** Review the instructions and notes under the **Learning Notes** tab to compare your syntax, or ask me *'How do I fix my code?'* in the chat."
        return msg

    elif action == "explain":
        if not code.strip():
            return "Your code editor is currently empty! Write some Python code or select a template to explain."
        
        msg = f"### 💡 Code Explanation\n"
        msg += f"Here is a breakdown of what your code does in the context of **{title}**:\n\n"
        
        lines = code.split("\n")
        msg += f"- It runs a script with {len(lines)} lines of Python code.\n"
        
        if "import pandas" in code or "pd." in code:
            msg += f"- **Data Analysis**: It imports/uses **Pandas** to work with structured datasets (DataFrames).\n"
        if "import numpy" in code or "np." in code:
            msg += f"- **Numerical Operations**: It utilizes **NumPy** arrays for fast vectorized operations.\n"
        if "import matplotlib" in code or "plt." in code or "sns." in code:
            msg += f"- **Visualization**: It utilizes plotting libraries to generate charts/graphs.\n"
        if "for " in code or "while " in code:
            msg += f"- **Looping**: It iterates over a sequence or condition using a loop.\n"
        if "def " in code:
            msg += f"- **Functions**: It defines a custom function to encapsulate reusable logic.\n"
        
        msg += f"\n**Line-by-Line Highlight:**\n"
        for line in lines[:5]:
            if line.strip() and not line.strip().startswith("#"):
                msg += f"- `{line.strip()}`: Executed to initialize, process, or render data.\n"
        if len(lines) > 5:
            msg += f"- *(and {len(lines)-5} more lines)*\n"
            
        msg += f"\n**Reference Concept:**\n"
        msg += f"This aligns with our learning objectives:\n"
        msg += "\n".join(objectives.split("\n")[:3])
        return msg

    elif action == "review":
        if not code.strip():
            return "Write some code first, and I will review it for quality, pep-8 compatibility, and performance!"
        
        suggestions = []
        if len(code) > 10 and "def " not in code and ("for " in code or "import " in code):
            suggestions.append("Consider encapsulating your main code block inside a reusable function (e.g., `def run_analysis():`).")
        if any(len(line) > 79 for line in code.split("\n")):
            suggestions.append("Some lines of code exceed 79 characters. Consider splitting them to comply with PEP 8 readability standards.")
        if "=" in code and not re.search(r"\s=\s", code):
            suggestions.append("Add spacing around operators (e.g., `x = 10` instead of `x=10`) to enhance visual hierarchy.")
        if "import " in code and not code.startswith("import"):
            suggestions.append("Place all your library imports (like `pandas` or `numpy`) at the very top of the script.")
            
        msg = f"### 🛠️ Code Review & Optimization\n"
        if suggestions:
            msg += "I've reviewed your workspace. Here are some suggestions for improvement:\n\n"
            for s in suggestions:
                msg += f"- {s}\n"
        else:
            msg += "Excellent work! Your code is highly readable, PEP 8 compliant, and uses optimal structures for this exercise.\n"
            
        msg += f"\n**Performance Tip:** Keep in mind that for Data Science, vectorized operations (e.g., `df['col'] * 2` in Pandas) are significantly faster than looping through rows with `for` loops."
        return msg

    elif action == "challenge":
        challenges = {
            "introduction-to-python": "Write a Python script that calculates the area of a circle. Define a variable `radius = 7`, compute the area using the formula `area = 3.14159 * (radius ** 2)`, and print the result.",
            "python-data-structures": "Create a list named `temperatures` with values `[22, 25, 19, 31, 28]`. Add a new temperature `24` to the end of the list, compute the average temperature, and print it.",
            "control-flow-and-functions": "Write a function named `is_even(n)` that returns `True` if a number is even, and `False` otherwise. Test the function on the numbers `4` and `7`.",
            "numpy-fundamentals": "Use NumPy to create a 1D array of 20 numbers from 1 to 20. Reshape it into a 4x5 2D matrix, and print the mean of each column.",
            "pandas-dataframes": "Create a Pandas DataFrame from a dictionary containing names and scores. Select only the rows where the score is greater than 80.",
            "data-cleaning-prep": "Write a snippet using Pandas to fill missing values in a DataFrame column named `Salary` with the column's median value, then drop any rows that have missing values in the `Email` column.",
            "matplotlib-seaborn": "Write a Matplotlib script to plot a simple line chart where the X-axis represents years `[2020, 2021, 2022, 2023]` and the Y-axis represents revenue `[500, 750, 1000, 1400]`. Set the title to 'Annual Growth'.",
            "statistical-analysis": "Use scipy or numpy to compute the Pearson correlation coefficient between two lists: `x = [1, 2, 3, 4, 5]` and `y = [2, 4, 5, 4, 5]`. Explain if the correlation is positive or negative.",
            "introduction-to-machine-learning": "Define a Scikit-Learn `DecisionTreeClassifier` with `max_depth=3`. Fit it on your training features `X_train` and labels `y_train`, then predict labels on `X_test`.",
            "model-evaluation": "Write a snippet using Scikit-Learn to compute and print the confusion matrix and classification report for a set of true labels `y_true` and predicted labels `y_pred`."
        }
        challenge = challenges.get(session.slug, "Write a function that accepts a list of numbers and returns a new list containing only the unique numbers.")
        msg = f"### 🏋️ Practice Challenge\n"
        msg += f"Ready to test your skills? Try this challenge for **{title}**:\n\n"
        msg += f"> **Challenge:** {challenge}\n\n"
        msg += "Write your solution in the **Code Simulator** editor in the center panel, then click **Run Code** to test it!"
        return msg

    elif action == "career":
        careers = {
            "introduction-to-python": "Python is the entry point for almost all Data roles. Data Analysts and Engineers use it daily. Highlight your understanding of fundamental syntax and environment management in your resume.",
            "python-data-structures": "Efficient data handling is vital. Interviewers frequently ask about lists vs. tuples vs. dictionaries. Learn when to use which structure to optimize performance.",
            "control-flow-and-functions": "Writing clean, functional code is a key software engineering skill for Data Scientists. Break down complex scripts into modular functions to make them testable.",
            "numpy-fundamentals": "NumPy is the backbone of scientific computing. Machine Learning engineers use it to manipulate matrices (tensors). Make sure you understand array reshaping and slicing.",
            "pandas-dataframes": "Pandas is the absolute #1 library for Data Analysts. 80% of your time on the job will be spent manipulating tables with Pandas. Build portfolio projects showing data exploration with Pandas.",
            "data-cleaning-prep": "Data cleaning is where data professionals spend most of their time. Showing that you can handle missing data, duplicates, and type mismatches makes you stand out in technical interviews.",
            "matplotlib-seaborn": "Visual storytelling is critical for communicating insights to business managers. Data Analysts who can build clear, uncluttered visualizations are highly sought after.",
            "statistical-analysis": "A strong foundation in statistics separates amateur builders from professional data scientists. Focus on understanding hypothesis testing, p-values, and statistical distributions.",
            "introduction-to-machine-learning": "Machine learning is the gateway to Data Science and AI Engineering. Start by understanding standard models like Linear Regression and Decision Trees before moving to Deep Learning.",
            "model-evaluation": "Any model is useless without proper evaluation. Understanding metrics like Precision, Recall, and ROC-AUC is crucial when explaining your model's performance to clients or stakeholders."
        }
        advice = careers.get(session.slug, "Building a strong personal GitHub portfolio is the best way to get noticed by recruiters. Focus on clean code, clear documentation, and solved problems.")
        msg = f"### 💼 Career Mentorship\n"
        msg += f"**How this session applies to your career:**\n\n"
        msg += f"{advice}\n\n"
        msg += "**Action Step:** Build a small script incorporating today's concepts and push it to your GitHub portfolio. It shows recruiters you are actively learning and writing clean code!"
        return msg

    else:
        text = query.lower()
        if "numpy" in text:
            return "NumPy stands for Numerical Python. It provides high-performance multidimensional array objects and tools to work with them. Essential for scientific operations!"
        elif "pandas" in text or "dataframe" in text:
            return "Pandas is the standard data manipulation library. It introduces DataFrames, which are 2D tabular data structures with labeled axes (rows and columns) like an Excel sheet."
        elif "matplotlib" in text or "seaborn" in text or "plot" in text or "chart" in text:
            return "Visualization is key! Matplotlib provides low-level control, while Seaborn offers high-level, beautiful statistic visualizations. Remember to call `plt.show()` or return figures."
        elif "machine learning" in text or "ml" in text:
            return "Machine Learning allows systems to learn from data patterns instead of explicit programming. Today we are focusing on supervised models like decision trees or regressions."
        elif "error" in text or "fail" in text or "debug" in text or "fix" in text:
            if code:
                return "Click the **Review Code** button above, and I will analyze your current code editor contents and help you fix any formatting or logical errors."
            return "If you are getting a syntax error, check for missing colons, parenthesis, or quotes. Paste your code here and I will help you look at it."
        elif "career" in text or "job" in text or "interview" in text:
            return "To prepare for a career in Data Science: 1. Master Pandas/NumPy. 2. Build a project portfolio on GitHub. 3. Learn SQL. 4. Practice coding challenges. Ask me for *Career Mentor* advice using the action pill!"
        elif "how do i" in text or "what is" in text or "explain" in text:
            return f"In the context of **{title}**, this topic deals with key concepts like variables, loops, or arrays. Based on the **Learning Notes**, the main idea is: {learning_notes[:250]}..."
        
        return f"I am your AI Learning assistant for **{title}**. Ask me any question about Python, libraries, or concepts in this lesson! You can also click the quick action pills above for instant code review, explanations, or coding challenges."


@app.route("/api/ai-assistant", methods=["POST"])
@login_required
def ai_assistant_api():
    payload = request.get_json(silent=True) or {}
    session_id = payload.get("session_id")
    code = payload.get("code", "")
    query = payload.get("query", "").strip()
    action = payload.get("action", "chat")
    error = payload.get("error", "")

    session = db.session.get(Session, session_id) if session_id else None
    if not session:
        return jsonify({"reply": "I couldn't load the context for this session. Please refresh the page."})

    reply = generate_ai_response(action, query, code, error, session)
    return jsonify({"reply": reply})



@app.post("/session/<slug>/complete")
@login_required
@student_required
def complete_session(slug: str):
    session = Session.query.filter_by(slug=slug, published=True).first_or_404()
    progress = UserProgress.query.filter_by(user_id=current_user.id, session_id=session.id).first()
    if not progress:
        progress = UserProgress(user_id=current_user.id, session_id=session.id)
    progress.completed = True
    progress.progress_percentage = 100
    progress.completed_at = datetime.now(UTC)
    db.session.add(progress)
    db.session.commit()
    log_activity("student.session.complete", session.slug)
    flash(f"Session '{session.title}' marked as completed.", "success")
    return redirect(url_for("session_detail", slug=slug))


@app.post("/session/<slug>/bookmark")
@login_required
@student_required
def toggle_bookmark(slug: str):
    session = Session.query.filter_by(slug=slug, published=True).first_or_404()
    bookmark = Bookmark.query.filter_by(user_id=current_user.id, session_id=session.id).first()
    if bookmark:
        db.session.delete(bookmark)
        flash("Bookmark removed.", "success")
    else:
        db.session.add(Bookmark(user_id=current_user.id, session_id=session.id))
        flash("Session bookmarked.", "success")
    db.session.commit()
    log_activity("student.session.bookmark", session.slug)
    return redirect(url_for("session_detail", slug=slug))


@app.post("/session/<slug>/quiz")
@login_required
@student_required
def submit_quiz(slug: str):
    flash("Quizzes are now under the Exams & Quizzes module.", "error")
    return redirect(url_for("exams_dashboard"))


@app.post("/session/<slug>/comment")
@login_required
@student_required
def add_comment(slug: str):
    session = Session.query.filter_by(slug=slug, published=True).first_or_404()
    content = request.form.get("content", "").strip()
    if content:
        db.session.add(DiscussionComment(user_id=current_user.id, session_id=session.id, content=content, approved=True))
        db.session.commit()
        log_activity("student.comment.add", session.slug)
        flash("Comment posted.", "success")
    return redirect(url_for("session_detail", slug=slug))


@app.post("/comment/<int:comment_id>/like")
@login_required
@student_required
def like_comment(comment_id: int):
    comment = db.session.get(DiscussionComment, comment_id)
    if not comment:
        flash("Comment not found.", "error")
        return redirect(url_for("student_dashboard"))
    comment.likes += 1
    db.session.commit()
    flash("You liked this answer.", "success")
    return redirect(url_for("session_detail", slug=db.session.get(Session, comment.session_id).slug))


@app.route("/exams/<int:exam_id>/take", methods=["GET", "POST"])
@login_required
@student_required
def exam_take(exam_id: int):
    exam = db.session.get(Exam, exam_id)
    if not exam or not exam.published:
        flash("Exam not available.", "error")
        return redirect(url_for("exams_dashboard"))
    if exam.study_level != current_user.study_level:
        flash("You can only take examinations mapped to your study level.", "error")
        return redirect(url_for("exams_dashboard"))
    now = datetime.now(UTC)
    if exam.start_time and exam.start_time > now:
        flash("Exam has not started yet.", "error")
        return redirect(url_for("exams_dashboard"))
    if exam.end_time and exam.end_time < now:
        flash("Exam window has closed.", "error")
        return redirect(url_for("exams_dashboard"))

    prior_attempts = ExamAttemptRecord.query.filter_by(user_id=current_user.id, exam_id=exam.id).count()
    if prior_attempts >= exam.attempt_limit:
        flash("Attempt limit reached for this exam.", "error")
        return redirect(url_for("exams_dashboard"))

    question_rows = Question.query.filter_by(exam_id=exam.id).all()
    exam_questions = [
        {
            "id": q.id,
            "question": q.question_text,
            "type": q.question_type,
            "options": json.loads(q.options or "[]"),
            "correct": q.correct_answer or "",
            "marks": q.marks,
        }
        for q in question_rows
    ]
    if not exam_questions:
        flash("Exam questions are not configured.", "error")
        return redirect(url_for("exams_dashboard"))

    attempt = ExamAttemptRecord.query.filter_by(user_id=current_user.id, exam_id=exam.id, status="in_progress").order_by(
        ExamAttemptRecord.created_at.desc()
    ).first()

    if request.method == "GET":
        if not attempt:
            order = list(range(len(exam_questions)))
            if exam.randomize_questions:
                order.reverse()
            attempt = ExamAttemptRecord(
                user_id=current_user.id,
                exam_id=exam.id,
                answers_json=json.dumps({"question_order": order}),
                ip_address=request.remote_addr,
                user_agent=request.headers.get("User-Agent", ""),
            )
            db.session.add(attempt)
            db.session.commit()
        saved = json.loads(attempt.answers_json or "{}")
        order = saved.get("question_order", list(range(len(exam_questions))))
        ordered_questions = [exam_questions[i] for i in order]
        return render_template(
            "exam_take.html",
            exam=exam,
            attempt=attempt,
            exam_questions=ordered_questions,
            time_limit=exam.duration,
            pass_mark=exam.passing_score,
        )

    # POST submit
    if not attempt:
        flash("No active exam attempt found.", "error")
        return redirect(url_for("exams_dashboard"))

    elapsed = (datetime.now(UTC) - attempt.created_at).total_seconds() / 60
    if elapsed > exam.duration + 1:
        flash("Exam submission rejected: time limit exceeded.", "error")
        attempt.submitted_at = datetime.now(UTC)
        attempt.status = "terminated"
        db.session.commit()
        return redirect(url_for("exams_dashboard"))

    integrity_flags = {
        "tab_switches": int(request.form.get("tab_switches", "0") or 0),
        "fullscreen_exits": int(request.form.get("fullscreen_exits", "0") or 0),
        "copy_events": int(request.form.get("copy_events", "0") or 0),
        "forced_termination": request.form.get("forced_termination", ""),
    }
    is_flagged = (
        integrity_flags["tab_switches"] > 0
        or integrity_flags["fullscreen_exits"] > 1
        or integrity_flags["copy_events"] > 0
        or bool(integrity_flags["forced_termination"])
    )

    answers = {}
    correct_total = 0
    objective_total = 0
    saved = json.loads(attempt.answers_json or "{}")
    ordered_indices = saved.get("question_order", list(range(len(exam_questions))))
    ordered_questions = [exam_questions[i] for i in ordered_indices]
    for idx, question in enumerate(ordered_questions):
        key = f"q{idx}"
        response = request.form.get(key, "").strip()
        answers[key] = response
        q_type = question.get("type", "mcq")
        if q_type == "mcq":
            objective_total += 1
            if response == str(question.get("correct", "")):
                correct_total += 1

    # Essay questions are stored for instructor review; objective score is auto-scored.
    score = int((correct_total / objective_total) * 100) if objective_total else 0
    passed = score >= exam.passing_score

    attempt.submitted_at = datetime.now(UTC)
    attempt.answers_json = json.dumps({"question_order": ordered_indices, "answers": answers})
    attempt.violation_count = (
        integrity_flags["tab_switches"] + integrity_flags["fullscreen_exits"] + integrity_flags["copy_events"]
    )
    attempt.suspicious_score = min(100, attempt.violation_count * 20)
    attempt.status = "flagged" if is_flagged else ("passed" if passed else "submitted")
    attempt.score = score
    db.session.commit()
    if attempt.violation_count or integrity_flags["forced_termination"]:
        db.session.add(
            IntegrityLog(
                user_id=current_user.id,
                exam_id=exam.id,
                violation_type=integrity_flags["forced_termination"] or "integrity_violation",
                severity="high" if is_flagged else "warning",
                details=json.dumps(integrity_flags),
            )
        )
        db.session.commit()
    log_activity("student.exam.submit", f"exam={exam.id}:{score}:flagged={is_flagged}")
    flash("Exam submitted successfully.", "success")
    return redirect(url_for("exams_dashboard"))


@app.post("/exams/attempt/<int:attempt_id>/violation")
@login_required
@student_required
def exam_violation(attempt_id: int):
    attempt = db.session.get(ExamAttemptRecord, attempt_id)
    if not attempt or attempt.user_id != current_user.id or attempt.status != "in_progress":
        return jsonify({"ok": False}), 404
    violation_type = request.form.get("type", "unknown")
    attempt.violation_count += 1
    attempt.suspicious_score = min(100, attempt.suspicious_score + 20)
    terminate = attempt.violation_count >= 3
    if terminate:
        attempt.status = "terminated"
        attempt.submitted_at = datetime.now(UTC)
    db.session.add(
        IntegrityLog(
            user_id=current_user.id,
            exam_id=attempt.exam_id,
            violation_type=violation_type,
            severity="high" if terminate else "warning",
            details=f"count={attempt.violation_count}",
        )
    )
    db.session.commit()
    return jsonify({"ok": True, "terminate": terminate, "count": attempt.violation_count})


@app.post("/api/chatbot")
def chatbot_api():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "")
    return jsonify({"reply": chatbot_reply(message)})


@app.route("/admin")
@login_required
@admin_required
def admin_panel():
    ctx = admin_dashboard_context()
    return render_template("admin.html", **ctx)


@app.route("/admin/exams", methods=["GET", "POST"])
@login_required
@admin_required
def admin_exams():
    if request.method == "POST":
        start_time_raw = request.form.get("start_time", "").strip()
        end_time_raw = request.form.get("end_time", "").strip()
        start_time = datetime.fromisoformat(start_time_raw) if start_time_raw else None
        end_time = datetime.fromisoformat(end_time_raw) if end_time_raw else None
        
        exam = Exam(
            title=request.form.get("title", "").strip(),
            description=request.form.get("description", "").strip(),
            duration=int(request.form.get("duration", "30") or 30),
            passing_score=int(request.form.get("passing_score", "50") or 50),
            exam_type=request.form.get("exam_type", "mixed"),
            attempt_limit=int(request.form.get("attempt_limit", "1") or 1),
            randomize_questions=request.form.get("randomize_questions") == "on",
            randomize_options=request.form.get("randomize_options") == "on",
            one_device_only=request.form.get("one_device_only") == "on",
            proctoring_enabled=request.form.get("proctoring_enabled") == "on",
            published=request.form.get("published") == "on",
            study_level=request.form.get("study_level", "Beginner").strip(),
            start_time=start_time,
            end_time=end_time,
        )
        db.session.add(exam)
        db.session.commit()
        raw_questions = request.form.get("questions_json", "[]")
        try:
            questions = json.loads(raw_questions)
        except json.JSONDecodeError:
            questions = []
        for q in questions:
            db.session.add(
                Question(
                    exam_id=exam.id,
                    question_text=q.get("questionText", ""),
                    question_type=q.get("questionType", "mcq"),
                    options=json.dumps(q.get("options", [])),
                    correct_answer=str(q.get("correctAnswer", "")),
                    marks=int(q.get("marks", 1)),
                )
            )
        db.session.commit()
        log_activity("admin.exam.create", exam.title)
        flash("Exam created.", "success")
        return redirect(url_for("admin_exams"))
    exams = Exam.query.order_by(Exam.created_at.desc()).all()
    return render_template("admin_exams.html", exams=exams)


@app.route("/admin/session/new", methods=["GET", "POST"])
@login_required
@admin_required
def admin_session_new():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        slug = slugify(request.form.get("slug") or title)
        uploaded_note = request.files.get("notes_file")
        notes_path = None
        if uploaded_note and uploaded_note.filename:
            UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
            safe_name = secure_filename(uploaded_note.filename)
            stored_name = f"{slug}-{int(datetime.now(UTC).timestamp())}-{safe_name}"
            destination = UPLOADS_DIR / stored_name
            uploaded_note.save(destination)
            notes_path = f"uploads/notes/{stored_name}"
        session = Session(
            title=title,
            slug=slug,
            description=request.form.get("description", ""),
            content=request.form.get("content", ""),
            objectives=request.form.get("objectives", ""),
            expected_outcomes=request.form.get("expected_outcomes", ""),
            learning_notes=request.form.get("learning_notes", ""),
            instructions=request.form.get("instructions", ""),
            code_examples=request.form.get("code_examples", ""),
            resources=request.form.get("resources", ""),
            notes_file_path=notes_path,
            video_url=request.form.get("video_url", "").strip() or None,
            duration=request.form.get("duration", "60 min"),
            difficulty=request.form.get("difficulty", "Beginner"),
            display_order=int(request.form.get("display_order", Session.query.count() + 1)),
            published=request.form.get("published") == "on",
        )
        db.session.add(session)
        db.session.commit()
        log_activity("admin.session.create", slug)
        flash("Session created.", "success")
        return redirect(url_for("admin_panel"))
    return render_template("admin_session_form.html", session_obj=None)


@app.route("/admin/session/<int:session_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def admin_session_edit(session_id: int):
    session_obj = db.session.get(Session, session_id)
    if not session_obj:
        flash("Session not found.", "error")
        return redirect(url_for("admin_panel"))

    if request.method == "POST":
        session_obj.title = request.form.get("title", "").strip()
        session_obj.slug = slugify(request.form.get("slug") or session_obj.title)
        session_obj.description = request.form.get("description", "")
        session_obj.content = request.form.get("content", "")
        session_obj.objectives = request.form.get("objectives", "")
        session_obj.expected_outcomes = request.form.get("expected_outcomes", "")
        session_obj.learning_notes = request.form.get("learning_notes", "")
        session_obj.instructions = request.form.get("instructions", "")
        session_obj.code_examples = request.form.get("code_examples", "")
        session_obj.resources = request.form.get("resources", "")
        session_obj.video_url = request.form.get("video_url", "").strip() or None
        uploaded_note = request.files.get("notes_file")
        if uploaded_note and uploaded_note.filename:
            UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
            safe_name = secure_filename(uploaded_note.filename)
            stored_name = f"{session_obj.slug}-{int(datetime.now(UTC).timestamp())}-{safe_name}"
            destination = UPLOADS_DIR / stored_name
            uploaded_note.save(destination)
            session_obj.notes_file_path = f"uploads/notes/{stored_name}"
        session_obj.duration = request.form.get("duration", "60 min")
        session_obj.difficulty = request.form.get("difficulty", "Beginner")
        session_obj.display_order = int(request.form.get("display_order", session_obj.display_order))
        session_obj.published = request.form.get("published") == "on"
        db.session.commit()
        log_activity("admin.session.edit", session_obj.slug)
        flash("Session updated.", "success")
        return redirect(url_for("admin_panel"))

    return render_template("admin_session_form.html", session_obj=session_obj)


@app.post("/admin/session/<int:session_id>/toggle")
@login_required
@admin_required
def admin_toggle_publish(session_id: int):
    session_obj = db.session.get(Session, session_id)
    if not session_obj:
        flash("Session not found.", "error")
        return redirect(url_for("admin_panel"))
    session_obj.published = not session_obj.published
    db.session.commit()
    log_activity("admin.session.publish_toggle", session_obj.slug)
    flash("Session publish status updated.", "success")
    return redirect(url_for("admin_panel"))


@app.post("/admin/session/reorder")
@login_required
@admin_required
def admin_reorder_sessions():
    ordered_ids = request.form.getlist("session_id")
    for idx, sid in enumerate(ordered_ids, start=1):
        session_obj = db.session.get(Session, int(sid))
        if session_obj:
            session_obj.display_order = idx
    db.session.commit()
    log_activity("admin.session.reorder")
    flash("Session order updated.", "success")
    return redirect(url_for("admin_panel"))


@app.post("/admin/users/<int:user_id>/suspend")
@login_required
@admin_required
def admin_toggle_suspend(user_id: int):
    user = db.session.get(User, user_id)
    if not user or user.is_admin:
        flash("User not eligible for suspension.", "error")
        return redirect(url_for("admin_panel"))
    user.is_suspended = not user.is_suspended
    db.session.commit()
    log_activity("admin.user.suspend_toggle", user.email)
    flash("User status updated.", "success")
    return redirect(url_for("admin_panel"))


@app.post("/admin/users/<int:user_id>/reset-progress")
@login_required
@admin_required
def admin_reset_progress(user_id: int):
    UserProgress.query.filter_by(user_id=user_id).delete()
    QuizResult.query.filter_by(user_id=user_id).delete()
    Bookmark.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    log_activity("admin.user.reset_progress", str(user_id))
    flash("Student progress reset.", "success")
    return redirect(url_for("admin_panel"))


@app.post("/admin/comments/<int:comment_id>/toggle")
@login_required
@admin_required
def admin_toggle_comment(comment_id: int):
    comment = db.session.get(DiscussionComment, comment_id)
    if not comment:
        flash("Comment not found.", "error")
        return redirect(url_for("admin_panel"))
    comment.approved = not comment.approved
    db.session.commit()
    log_activity("admin.comment.toggle", str(comment_id))
    flash("Comment moderation updated.", "success")
    return redirect(url_for("admin_panel"))


@app.post("/admin/notifications/send")
@login_required
@admin_required
def admin_send_notification():
    title = request.form.get("title", "").strip()
    message = request.form.get("message", "").strip()
    target = request.form.get("target", "all")
    if not title or not message:
        flash("Title and message are required.", "error")
        return redirect(url_for("admin_panel"))
    if target == "all":
        db.session.add(Notification(user_id=None, title=title, message=message, created_by_admin_id=current_user.id))
    else:
        db.session.add(
            Notification(user_id=int(target), title=title, message=message, created_by_admin_id=current_user.id)
        )
    db.session.commit()
    log_activity("admin.notification.send", title)
    flash("Notification sent.", "success")
    return redirect(url_for("admin_panel"))


@app.get("/admin/reports/export.csv")
@login_required
@admin_required
def admin_export_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Student", "Email", "Study Level", "Suspended", "Completed Sessions", "Avg Quiz Score"])
    students = User.query.filter_by(is_admin=False).all()
    for student in students:
        completed = UserProgress.query.filter_by(user_id=student.id, completed=True).count()
        avg_score = db.session.query(db.func.avg(QuizResult.score)).filter_by(user_id=student.id).scalar() or 0
        writer.writerow([student.name, student.email, student.study_level, student.is_suspended, completed, round(avg_score, 2)])
    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv"
    response.headers["Content-Disposition"] = "attachment; filename=cdam-analytics-report.csv"
    return response


@app.post("/admin/session/<int:session_id>/delete")
@login_required
@admin_required
def admin_session_delete(session_id: int):
    session_obj = db.session.get(Session, session_id)
    if not session_obj:
        flash("Session not found.", "error")
        return redirect(url_for("admin_panel"))
    UserProgress.query.filter_by(session_id=session_id).delete()
    QuizResult.query.filter_by(session_id=session_id).delete()
    Bookmark.query.filter_by(session_id=session_id).delete()
    LessonView.query.filter_by(session_id=session_id).delete()
    DiscussionComment.query.filter_by(session_id=session_id).delete()
    db.session.delete(session_obj)
    db.session.commit()
    log_activity("admin.session.delete", str(session_id))
    flash("Session deleted.", "success")
    return redirect(url_for("admin_panel"))


@app.route("/admin/exams/<int:exam_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def admin_exam_edit(exam_id: int):
    exam = db.session.get(Exam, exam_id)
    if not exam:
        flash("Exam not found.", "error")
        return redirect(url_for("admin_exams"))
    if request.method == "POST":
        exam.title = request.form.get("title", "").strip()
        exam.description = request.form.get("description", "").strip()
        exam.duration = int(request.form.get("duration", "30") or 30)
        exam.passing_score = int(request.form.get("passing_score", "50") or 50)
        exam.exam_type = request.form.get("exam_type", "mixed")
        exam.attempt_limit = int(request.form.get("attempt_limit", "1") or 1)
        exam.randomize_questions = request.form.get("randomize_questions") == "on"
        exam.randomize_options = request.form.get("randomize_options") == "on"
        exam.one_device_only = request.form.get("one_device_only") == "on"
        exam.proctoring_enabled = request.form.get("proctoring_enabled") == "on"
        exam.published = request.form.get("published") == "on"
        exam.study_level = request.form.get("study_level", "Beginner").strip()
        start_time = request.form.get("start_time", "").strip()
        end_time = request.form.get("end_time", "").strip()
        exam.start_time = datetime.fromisoformat(start_time) if start_time else None
        exam.end_time = datetime.fromisoformat(end_time) if end_time else None
        raw_questions = request.form.get("questions_json", "")
        if raw_questions.strip():
            try:
                questions = json.loads(raw_questions)
                Question.query.filter_by(exam_id=exam.id).delete()
                for q in questions:
                    db.session.add(Question(
                        exam_id=exam.id,
                        question_text=q.get("questionText", ""),
                        question_type=q.get("questionType", "mcq"),
                        options=json.dumps(q.get("options", [])),
                        correct_answer=str(q.get("correctAnswer", "")),
                        marks=int(q.get("marks", 1)),
                    ))
            except json.JSONDecodeError:
                pass
        db.session.commit()
        log_activity("admin.exam.edit", exam.title)
        flash("Exam updated.", "success")
        return redirect(url_for("admin_exams"))
    questions = Question.query.filter_by(exam_id=exam.id).all()
    questions_data = [
        {"questionText": q.question_text, "questionType": q.question_type,
         "options": json.loads(q.options or "[]"), "correctAnswer": q.correct_answer,
         "marks": q.marks}
        for q in questions
    ]
    return render_template("admin_exam_edit.html", exam=exam, questions_json=json.dumps(questions_data, indent=2))


@app.post("/admin/exams/<int:exam_id>/delete")
@login_required
@admin_required
def admin_exam_delete(exam_id: int):
    exam = db.session.get(Exam, exam_id)
    if not exam:
        flash("Exam not found.", "error")
        return redirect(url_for("admin_exams"))
    Question.query.filter_by(exam_id=exam_id).delete()
    ExamAttemptRecord.query.filter_by(exam_id=exam_id).delete()
    IntegrityLog.query.filter_by(exam_id=exam_id).delete()
    db.session.delete(exam)
    db.session.commit()
    log_activity("admin.exam.delete", str(exam_id))
    flash("Exam deleted.", "success")
    return redirect(url_for("admin_exams"))


@app.post("/admin/exams/<int:exam_id>/toggle")
@login_required
@admin_required
def admin_exam_toggle(exam_id: int):
    exam = db.session.get(Exam, exam_id)
    if not exam:
        flash("Exam not found.", "error")
        return redirect(url_for("admin_exams"))
    exam.published = not exam.published
    db.session.commit()
    log_activity("admin.exam.toggle", exam.title)
    flash("Exam publish status updated.", "success")
    return redirect(url_for("admin_exams"))


@app.route("/admin/integrity")
@login_required
@admin_required
def admin_integrity():
    logs = IntegrityLog.query.order_by(IntegrityLog.timestamp.desc()).all()
    users_map = {u.id: u for u in User.query.all()}
    exams_map = {e.id: e for e in Exam.query.all()}
    return render_template("admin_integrity.html", logs=logs, users_map=users_map, exams_map=exams_map)



def migrate_schema() -> None:

    from sqlalchemy import inspect, text

    inspector = inspect(db.engine)
    if "sessions" in inspector.get_table_names():
        columns = {col["name"] for col in inspector.get_columns("sessions")}
        if "quiz_json" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE sessions ADD COLUMN quiz_json TEXT DEFAULT '[]'"))
        if "notes_file_path" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE sessions ADD COLUMN notes_file_path VARCHAR(500)"))
        if "video_url" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE sessions ADD COLUMN video_url VARCHAR(500)"))
        if "expected_outcomes" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE sessions ADD COLUMN expected_outcomes TEXT"))
        if "learning_notes" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE sessions ADD COLUMN learning_notes TEXT"))
        if "instructions" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE sessions ADD COLUMN instructions TEXT"))
    if "users" in inspector.get_table_names():
        columns = {col["name"] for col in inspector.get_columns("users")}
        if "study_level" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN study_level VARCHAR(30) DEFAULT 'Beginner'"))
        if "is_suspended" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN is_suspended BOOLEAN DEFAULT 0"))
        if "reg_number" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN reg_number VARCHAR(100)"))
    if "exams" in inspector.get_table_names():
        columns = {col["name"] for col in inspector.get_columns("exams")}
        if "study_level" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE exams ADD COLUMN study_level VARCHAR(30) DEFAULT 'Beginner'"))


def initialize():
    with app.app_context():
        db.create_all()
        migrate_schema()
        seed_sessions()
        admin = User.query.filter_by(email="admin@cdam.local").first()
        if not admin:
            admin = User(
                name="CDAM Admin",
                email="admin@cdam.local",
                reg_number="ADMIN-001",
                password_hash=generate_password_hash("admin123"),
                auth_provider="local",
                avatar=CDAM_LOGO,
                is_admin=True,
                study_level="Professional",
            )
            db.session.add(admin)
            db.session.commit()
        elif not admin.reg_number:
            admin.reg_number = "ADMIN-001"
            db.session.commit()
        stale_demo = User.query.filter_by(email="demo.oauth@cdam.local").first()
        if stale_demo:
            db.session.delete(stale_demo)
            db.session.commit()


# Automatically initialize and seed the database on server startup/import
initialize()

if __name__ == "__main__":
    app.run(debug=False)
