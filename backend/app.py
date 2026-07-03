from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
# Load .env file from project root if it exists
load_dotenv(BASE_DIR.parent / ".env")

import csv
import io
import json
from datetime import UTC, datetime, timezone, timedelta
from functools import wraps
EAT = timezone(timedelta(hours=3))

def to_naive(dt):
    if dt is None:
        return None
    return dt.replace(tzinfo=None) if dt.tzinfo else dt

def utc_now():
    return datetime.now(EAT).replace(tzinfo=None)

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
from utils import compute_streak, parse_quiz, render_markdown, slugify
from ai_service import get_ai_service

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
if os.environ.get("DISABLE_DB_SSL", "").lower() != "true":
    if "aivencloud.com" in db_url or "railway" in db_url or "supabase" in db_url:
        if db_url.startswith("mysql"):
            # For Aiven MySQL, SSL is required. For Railway MySQL, SSL should not be forced as it causes WRONG_VERSION_NUMBER errors.
            if "aivencloud.com" in db_url:
                app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
                    "connect_args": {
                        "ssl": {}
                    }
                }
        else:
            # PostgreSQL SSL settings
            app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
                "connect_args": {
                    "sslmode": "require"
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
    require_password_change = db.Column(db.Boolean, default=False, nullable=False)
    password_reset_status = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    @property
    def role(self) -> str:
        return "admin" if self.is_admin else "student"


class UserSandboxFile(db.Model):
    __tablename__ = "user_sandbox_files"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    is_global = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    __table_args__ = (
        db.UniqueConstraint("user_id", "filename", name="uq_user_sandbox_filename"),
    )


class AIChatMessage(db.Model):
    __tablename__ = "ai_chat_messages"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False, index=True)
    role = db.Column(db.String(50), nullable=False) # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)


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
    notes_file_name = db.Column(db.String(255), nullable=True)
    notes_file_data = db.Column(db.LargeBinary, nullable=True)
    video_url = db.Column(db.String(500), nullable=True)
    quiz_json = db.Column(db.Text, nullable=False, default="[]")
    duration = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    display_order = db.Column(db.Integer, nullable=False)
    published = db.Column(db.Boolean, default=True)

    @property
    def clean_title(self) -> str:
        import re
        return re.sub(r"^(Session\s+\d+:\s*)+", "", self.title, flags=re.IGNORECASE).strip()


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
    created_at = db.Column(db.DateTime, default=utc_now)


class Bookmark(db.Model):
    __tablename__ = "bookmarks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=utc_now)


class LessonView(db.Model):
    __tablename__ = "lesson_views"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False, index=True)
    viewed_at = db.Column(db.DateTime, default=utc_now)


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    role = db.Column(db.String(30), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)


class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_by_admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)


class DiscussionComment(db.Model):
    __tablename__ = "discussion_comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    approved = db.Column(db.Boolean, default=True)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utc_now)


class ExamAttempt(db.Model):
    __tablename__ = "exam_attempts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False, index=True)
    started_at = db.Column(db.DateTime, default=utc_now)
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
    passing_score = db.Column(db.Integer, default=60)
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
    created_at = db.Column(db.DateTime, default=utc_now)


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
    created_at = db.Column(db.DateTime, default=utc_now)

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
    timestamp = db.Column(db.DateTime, default=utc_now)


class AIUsageLog(db.Model):
    __tablename__ = "ai_usage_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    session_id = db.Column(db.Integer, nullable=True)
    action = db.Column(db.String(50), nullable=False)
    tokens_used = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utc_now)


class PlatformSetting(db.Model):
    __tablename__ = "platform_settings"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)


def to_local_datetime_str(dt):
    if not dt:
        return ''
    try:
        return dt.strftime('%Y-%m-%dT%H:%M')
    except Exception:
        return dt.strftime('%Y-%m-%dT%H:%M')

@app.context_processor
def inject_globals():
    sessions = Session.query.filter_by(published=True).order_by(Session.display_order).all()
    return {
        "cdam_logo": url_for("static", filename=CDAM_LOGO),
        "chuka_logo": url_for("static", filename=CHUKA_LOGO),
        "nav_sessions": sessions,
        "render_markdown": render_markdown,
        "check_session_access": check_session_access,
        "to_local_datetime_str": to_local_datetime_str,
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


def check_session_access_with_reason(user, display_order):
    if not user or not hasattr(user, "is_authenticated") or not user.is_authenticated:
        return False, "not_authenticated"
    if user.is_admin:
        return True, ""
    level = getattr(user, "study_level", "Beginner")
    if display_order > 10 and level != "Professional":
        return False, "restricted_level"
        
    prev_sessions = Session.query.filter(Session.display_order < display_order, Session.published == True).all()
    for s in prev_sessions:
        # Verify the session has been marked as completed
        progress = UserProgress.query.filter_by(user_id=user.id, session_id=s.id).first()
        if not progress or not progress.completed:
            return False, f"locked_session:{s.display_order}:{s.title}"
            
        # Verify the quiz has been passed, if a quiz is configured
        quiz_questions = parse_quiz(s.quiz_json)
        if quiz_questions:
            res = QuizResult.query.filter_by(user_id=user.id, session_id=s.id).first()
            if not res or res.score < 60:
                return False, f"locked_quiz:{s.display_order}:{s.title}"
            
    return True, ""


def check_session_access(user, display_order):
    access, _ = check_session_access_with_reason(user, display_order)
    return access



def seed_sessions() -> None:
    # Explicitly clean Session 2 title to ensure it has no duplicate text
    s2 = Session.query.filter_by(slug="session-2-data-import-eda").first()
    if s2:
        s2.title = "Session 2: Data Import, Cleaning, and Exploratory Data Analysis (EDA)"
        db.session.add(s2)
        db.session.commit()

    # Clean up title repetitions/prefixes in existing database sessions
    import re
    for session_obj in Session.query.all():
        title_changed = False
        if "atory Data Analysis (EDA) atory Data Analysis (EDA)" in session_obj.title:
            session_obj.title = session_obj.title.replace(
                "atory Data Analysis (EDA) atory Data Analysis (EDA)",
                "atory Data Analysis (EDA)"
            )
            title_changed = True
        
        # Strip redundant prefixes like "Session X: Session X:"
        cleaned = re.sub(r"^(Session\s+\d+:\s*)+", "", session_obj.title, flags=re.IGNORECASE).strip()
        new_title = f"Session {session_obj.display_order}: {cleaned}"
        if session_obj.title != new_title:
            session_obj.title = new_title
            title_changed = True
            
        if title_changed:
            db.session.add(session_obj)
    db.session.commit()

    # Only seed initial sessions if they are not already in the database.
    # We do NOT overwrite existing sessions or delete sessions created/edited by admins.
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
                quiz_json="[]",
                duration=item["duration"],
                difficulty=item["difficulty"],
                display_order=idx,
                published=True,
            )
            db.session.add(session_obj)
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
        total_sessions = 18

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
        ActivityLog.created_at >= utc_now().replace(hour=0, minute=0, second=0, microsecond=0)
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

    # --- New analytics ---
    from datetime import timedelta
    seven_days_ago = utc_now() - timedelta(days=7)
    recent_registrations = User.query.filter(
        User.is_admin == False, User.created_at >= seven_days_ago
    ).order_by(User.created_at.desc()).all()

    total_attempts = ExamAttemptRecord.query.count()
    passed_attempts = ExamAttemptRecord.query.filter_by(status="submitted").join(
        Exam, Exam.id == ExamAttemptRecord.exam_id
    ).filter(ExamAttemptRecord.score >= Exam.passing_score).count()
    exam_pass_rate = round((passed_attempts / total_attempts * 100), 1) if total_attempts > 0 else 0.0

    exam_results = (
        db.session.query(ExamAttemptRecord, User.name, User.reg_number, Exam.title, Exam.passing_score)
        .join(User, User.id == ExamAttemptRecord.user_id)
        .join(Exam, Exam.id == ExamAttemptRecord.exam_id)
        .order_by(ExamAttemptRecord.created_at.desc())
        .limit(30)
        .all()
    )

    total_sessions = Session.query.count()

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
        "recent_registrations": recent_registrations,
        "exam_pass_rate": exam_pass_rate,
        "exam_results": exam_results,
        "reset_requests": User.query.filter(User.password_reset_status == "requested").all(),
        "total_sessions": total_sessions,
        "ai_enabled": (PlatformSetting.query.filter_by(key="ai_enabled").first() or PlatformSetting(value="true")).value == "true",
        "ai_total_requests": AIUsageLog.query.count(),
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
        difficulties=["Beginner", "Professional"],
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if not app.config.get("TESTING"):
        flash("Public registration is disabled. Please contact the system administrator to receive your registration credentials.", "error")
        return redirect(url_for("login"))
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
            require_password_change=False
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
                db.func.lower(User.email) == identifier.lower(),
                User.email == identifier
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


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        reg_number = request.form.get("reg_number", "").strip().upper()
        
        user = User.query.filter(db.func.lower(User.email) == email, User.reg_number == reg_number).first()
        if not user:
            flash("No user found with the provided email and registration number.", "error")
            return redirect(url_for("forgot_password"))
            
        action = request.form.get("action", "")
        if action == "reset":
            if user.password_reset_status != "approved":
                flash("Password reset request must be approved by an administrator.", "error")
                return redirect(url_for("forgot_password"))
            new_password = request.form.get("new_password", "").strip()
            if not new_password:
                flash("Please enter a new password.", "error")
                return render_template("forgot_password.html", user=user, status="approved")
            user.password_hash = generate_password_hash(new_password)
            user.password_reset_status = None
            db.session.commit()
            log_activity("auth.password_reset_complete", f"User={user.email}")
            flash("Password updated successfully. You can now sign in.", "success")
            return redirect(url_for("login"))
            
        # Default action: check status / submit request
        if not user.password_reset_status:
            user.password_reset_status = "requested"
            db.session.commit()
            log_activity("auth.password_reset_request", f"User={user.email}")
            flash("Password reset request submitted successfully.", "success")
            return render_template("forgot_password.html", user=user, status="requested")
        elif user.password_reset_status == "requested":
            return render_template("forgot_password.html", user=user, status="requested")
        elif user.password_reset_status == "approved":
            return render_template("forgot_password.html", user=user, status="approved")
            
    return render_template("forgot_password.html", user=None, status=None)


@app.route("/logout")
@login_required
def logout():
    log_activity("auth.logout")
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


@app.before_request
def enforce_password_change():
    if current_user.is_authenticated and not current_user.is_admin:
        if getattr(current_user, "require_password_change", False):
            allowed = ["student_profile", "logout", "static"]
            if request.endpoint and request.endpoint not in allowed:
                flash("You are required to change your password before proceeding.", "warning")
                return redirect(url_for("student_profile"))


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
    now = utc_now()
    exams = Exam.query.filter_by(published=True, study_level=current_user.study_level).all()
    upcoming = [e for e in exams if e.start_time and to_naive(e.start_time) > now]
    available = [
        e
        for e in exams
        if (not e.start_time or to_naive(e.start_time) <= now) and (not e.end_time or to_naive(e.end_time) >= now)
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
        new_password = request.form.get("new_password", "").strip()
        if current_user.require_password_change and not new_password:
            flash("You must enter a new password to proceed.", "error")
            return redirect(url_for("student_profile"))

        current_user.name = request.form.get("name", current_user.name).strip()
        current_user.avatar = request.form.get("avatar", current_user.avatar).strip() or current_user.avatar
        current_user.study_level = request.form.get("study_level", current_user.study_level)
        if new_password:
            if not current_user.require_password_change:
                flash("Password change must be approved by an administrator.", "error")
                return redirect(url_for("student_profile"))
            current_user.password_hash = generate_password_hash(new_password)
            current_user.require_password_change = False
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
    return render_template("certificate.html", user=current_user, completed_at=utc_now())


@app.route("/transcript")
@login_required
@student_required
def transcript():
    ctx = dashboard_context(current_user.id)
    if not ctx["certificate_ready"]:
        flash("Complete all sessions to unlock your academic transcript.", "error")
        return redirect(url_for("student_dashboard"))
        
    sessions = ctx["sessions"]
    progress_map = ctx["progress_map"]
    
    quiz_results = QuizResult.query.filter_by(user_id=current_user.id).all()
    quiz_map = {q.session_id: q for q in quiz_results}
    
    exams = Exam.query.filter_by(published=True, study_level=current_user.study_level).all()
    exam_attempts = ExamAttemptRecord.query.filter_by(user_id=current_user.id).all()
    
    return render_template(
        "transcript.html",
        user=current_user,
        sessions=sessions,
        progress_map=progress_map,
        quiz_map=quiz_map,
        exams=exams,
        exam_attempts=exam_attempts,
        completed_at=utc_now()
    )


def ensure_notes_file_exists(session) -> bool:
    """Ensure session's note file exists on disk, auto-restoring from DB BLOB if missing."""
    if not session or not session.notes_file_path:
        return False
    filename = session.notes_file_path.split("/")[-1]
    filepath = UPLOADS_DIR / filename
    if filepath.exists() and filepath.is_file():
        return True
    if session.notes_file_data:
        try:
            UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
            with open(filepath, "wb") as f:
                f.write(session.notes_file_data)
            return True
        except Exception as e:
            app.logger.error(f"Failed to auto-restore session note file: {e}")
    return False


@app.route("/session/<slug>")
@login_required
def session_detail(slug: str):
    session = Session.query.filter_by(slug=slug, published=True).first_or_404()
    access, reason = check_session_access_with_reason(current_user, session.display_order)
    if not access:
        if reason == "restricted_level":
            flash(f"Session '{session.title}' notes and materials are restricted to Professional level students. Please upgrade your profile level to access.", "error")
        elif reason.startswith("locked_session:"):
            _, prev_order, prev_title = reason.split(":", 2)
            flash(f"You must complete Session {prev_order} ('{prev_title}') to unlock Session {session.display_order}.", "error")
        elif reason.startswith("locked_quiz:"):
            _, prev_order, prev_title = reason.split(":", 2)
            flash(f"You must take and pass the quiz for Session {prev_order} ('{prev_title}') with at least 60% to unlock Session {session.display_order}.", "error")
        else:
            flash("You do not have access to this session.", "error")
        return redirect(url_for("student_dashboard"))
        
    progress = UserProgress.query.filter_by(user_id=current_user.id, session_id=session.id).first()
    completed = bool(progress and progress.completed)
    bookmark = Bookmark.query.filter_by(user_id=current_user.id, session_id=session.id).first()
    quiz = parse_quiz(session.quiz_json)
    quiz_result = QuizResult.query.filter_by(user_id=current_user.id, session_id=session.id).first()
    
    quiz_answers = {}
    if quiz_result and quiz_result.answers:
        try:
            quiz_answers = json.loads(quiz_result.answers)
        except Exception:
            pass
            
    comments = DiscussionComment.query.filter_by(session_id=session.id, approved=True).order_by(
        DiscussionComment.created_at.desc()
    ).all()
    track_lesson_view(current_user.id, session.id)
    log_activity("student.session.view", session.slug)
    
    notes_exist = False
    is_viewable = False
    notes_filename = ""
    if ensure_notes_file_exists(session):
        filename = session.notes_file_path.split("/")[-1]
        notes_exist = True
        notes_filename = filename.split("-", 2)[-1] if len(filename.split("-", 2)) > 2 else filename
        import os
        ext = os.path.splitext(filename)[1].lower()
        if ext in {".pdf", ".txt", ".md", ".png", ".jpg", ".jpeg", ".gif", ".svg"}:
            is_viewable = True
            
    now = utc_now()
    exams = Exam.query.filter_by(published=True, study_level=current_user.study_level).all()
    upcoming = [e for e in exams if e.start_time and to_naive(e.start_time) > now]
    available = [
        e
        for e in exams
        if (not e.start_time or to_naive(e.start_time) <= now) and (not e.end_time or to_naive(e.end_time) >= now)
    ]
    exam_attempts = ExamAttemptRecord.query.filter_by(user_id=current_user.id).order_by(
        ExamAttemptRecord.created_at.desc()
    ).all()

    return render_template(
        "session_detail.html",
        session=session,
        completed=completed,
        bookmarked=bool(bookmark),
        quiz=quiz,
        quiz_result=quiz_result,
        quiz_answers=quiz_answers,
        comments=comments,
        latest_exam_attempt=None,
        show_quiz=False,
        show_exam=False,
        notes_exist=notes_exist,
        is_viewable=is_viewable,
        notes_filename=notes_filename,
        upcoming=upcoming,
        available=available,
        exam_attempts=exam_attempts,
    )


@app.route("/session/<int:session_id>/download")
@login_required
def download_notes(session_id: int):
    from flask import send_from_directory
    session = db.session.get(Session, session_id)
    if not session or not ensure_notes_file_exists(session):
        flash("Notes file not found.", "error")
        return redirect(request.referrer or url_for("student_dashboard"))
    if not check_session_access(current_user, session.display_order):
        flash("Access to this note/revision material is restricted for your experience level.", "error")
        return redirect(request.referrer or url_for("student_dashboard"))
    
    filename = session.notes_file_path.split("/")[-1]
    return send_from_directory(UPLOADS_DIR, filename, as_attachment=False)


@app.route("/session/<int:session_id>/view")
@login_required
def view_notes(session_id: int):
    session = db.session.get(Session, session_id)
    if not session or not ensure_notes_file_exists(session):
        flash("Notes file not found.", "error")
        return redirect(request.referrer or url_for("student_dashboard"))
    if not check_session_access(current_user, session.display_order):
        flash("Access to this note/revision material is restricted for your experience level.", "error")
        return redirect(request.referrer or url_for("student_dashboard"))
    return render_template("view_notes.html", session=session)


@app.route("/api/run-code", methods=["POST"])
@login_required
def run_code():
    import subprocess
    import sys
    import os
    payload = request.get_json(silent=True) or {}
    code = payload.get("code", "")
    if not code.strip():
        return jsonify({"output": "", "error": "No code provided."})
    
    # Establish user-specific sandbox workspace directory
    workspace_dir = os.path.join(app.root_path, "sandbox_workspace", f"user_{current_user.id}")
    os.makedirs(workspace_dir, exist_ok=True)
    
    # Dynamically restore missing sandbox files from database
    try:
        from sqlalchemy.orm import defer
        global_files = UserSandboxFile.query.options(defer(UserSandboxFile.file_data)).filter_by(is_global=True).all()
        private_files = UserSandboxFile.query.options(defer(UserSandboxFile.file_data)).filter_by(user_id=current_user.id, is_global=False).all()
        
        for db_file in global_files:
            local_path = os.path.join(workspace_dir, db_file.filename)
            if not os.path.exists(local_path):
                full_file = UserSandboxFile.query.filter_by(id=db_file.id).first()
                if full_file:
                    with open(local_path, "wb") as lf:
                        lf.write(full_file.file_data)
                        
        for db_file in private_files:
            local_path = os.path.join(workspace_dir, db_file.filename)
            if not os.path.exists(local_path):
                full_file = UserSandboxFile.query.filter_by(id=db_file.id).first()
                if full_file:
                    with open(local_path, "wb") as lf:
                        lf.write(full_file.file_data)
    except Exception:
        pass
    
    try:
        # Run code in a subprocess inside the user's workspace directory
        process = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=15.0,
            cwd=workspace_dir
        )
        return jsonify({
            "output": process.stdout,
            "error": process.stderr,
            "exit_code": process.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            "output": "",
            "error": "Execution timed out (15 seconds limit)."
        })
    except Exception as e:
        return jsonify({
            "output": "",
            "error": f"Internal execution error: {str(e)}"
        })


@app.route("/api/sandbox/upload", methods=["POST"])
@login_required
def sandbox_upload():
    import os
    from werkzeug.utils import secure_filename
    
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
        
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
        
    # Check file size (limit to 15MB)
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > 15 * 1024 * 1024:
        return jsonify({"error": "File size exceeds 15MB limit."}), 400

    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({"error": "Invalid filename."}), 400
        
    workspace_dir = os.path.join(app.root_path, "sandbox_workspace", f"user_{current_user.id}")
    os.makedirs(workspace_dir, exist_ok=True)
    
    # Save to disk first
    file_bytes = file.read()
    local_path = os.path.join(workspace_dir, filename)
    with open(local_path, "wb") as f:
        f.write(file_bytes)
        
    # Save to database to ensure durability/persistence
    try:
        is_global = current_user.is_admin
        if is_global:
            sandbox_file = UserSandboxFile.query.filter_by(filename=filename, is_global=True).first()
            if not sandbox_file:
                sandbox_file = UserSandboxFile(user_id=current_user.id, filename=filename, is_global=True)
                db.session.add(sandbox_file)
            else:
                sandbox_file.user_id = current_user.id
        else:
            sandbox_file = UserSandboxFile.query.filter_by(user_id=current_user.id, filename=filename, is_global=False).first()
            if not sandbox_file:
                sandbox_file = UserSandboxFile(user_id=current_user.id, filename=filename, is_global=False)
                db.session.add(sandbox_file)
        sandbox_file.file_data = file_bytes
        sandbox_file.file_size = size
        db.session.commit()
    except Exception as e:
        return jsonify({"error": f"Database storage failed: {str(e)}"}), 500
        
    return jsonify({"success": True, "filename": filename, "size": size})


@app.route("/api/sandbox/files", methods=["GET"])
@login_required
def sandbox_list_files():
    import os
    workspace_dir = os.path.join(app.root_path, "sandbox_workspace", f"user_{current_user.id}")
    os.makedirs(workspace_dir, exist_ok=True)
    
    try:
        # Load from database to ensure durability
        private_files = UserSandboxFile.query.filter_by(user_id=current_user.id, is_global=False).all()
        global_files = UserSandboxFile.query.filter_by(is_global=True).all()
        
        # Restore files that are missing on disk
        for db_file in global_files:
            local_path = os.path.join(workspace_dir, db_file.filename)
            if not os.path.exists(local_path):
                with open(local_path, "wb") as lf:
                    lf.write(db_file.file_data)
                    
        for db_file in private_files:
            local_path = os.path.join(workspace_dir, db_file.filename)
            if not os.path.exists(local_path):
                with open(local_path, "wb") as lf:
                    lf.write(db_file.file_data)
                    
        files = []
        # Add global files
        for db_file in global_files:
            files.append({
                "name": db_file.filename,
                "size": db_file.file_size,
                "is_global": True,
                "can_delete": current_user.is_admin
            })
        # Add private files (filter out duplicates)
        global_names = {f.filename for f in global_files}
        for db_file in private_files:
            if db_file.filename not in global_names:
                files.append({
                    "name": db_file.filename,
                    "size": db_file.file_size,
                    "is_global": False,
                    "can_delete": True
                })
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": f"Failed to load files: {str(e)}"}), 500


@app.route("/api/sandbox/files/<filename>", methods=["DELETE"])
@login_required
def sandbox_delete_file(filename):
    import os
    from werkzeug.utils import secure_filename
    filename = secure_filename(filename)
    
    # Delete from database first
    try:
        if current_user.is_admin:
            # Admins can delete global files AND their own private files
            sandbox_file = UserSandboxFile.query.filter_by(filename=filename).first()
        else:
            # Students can only delete their own private files
            sandbox_file = UserSandboxFile.query.filter_by(user_id=current_user.id, filename=filename, is_global=False).first()
            
        if sandbox_file:
            db.session.delete(sandbox_file)
            db.session.commit()
        else:
            return jsonify({"error": "File not found or permission denied"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to delete record: {str(e)}"}), 500
        
    # Delete from local disk
    workspace_dir = os.path.join(app.root_path, "sandbox_workspace", f"user_{current_user.id}")
    file_path = os.path.join(workspace_dir, filename)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            os.remove(file_path)
        except Exception:
            pass
            
    return jsonify({"success": True})


def _ai_check_access():
    """Common checks for AI endpoints. Returns (error_response, session) tuple."""
    # Check if AI is enabled platform-wide
    setting = PlatformSetting.query.filter_by(key="ai_enabled").first()
    if setting and setting.value == "false":
        return jsonify({"reply": "AI assistance has been disabled by the administrator."}), None

    # Check if student has an active exam in progress
    active_exam = ExamAttemptRecord.query.filter_by(
        user_id=current_user.id, status="in_progress"
    ).first()
    if active_exam:
        return jsonify({"reply": "⚠️ AI assistance is unavailable during assessments. Complete your exam first."}), None

    # Rate limit check
    ai = get_ai_service()
    if not ai.check_rate_limit(current_user.id):
        return jsonify({"reply": "You've reached the AI request limit (10/minute). Please wait a moment before trying again."}), None

    return None, ai


def _log_ai_usage(action: str, session_id=None):
    """Log an AI usage event for admin analytics."""
    db.session.add(AIUsageLog(
        user_id=current_user.id,
        session_id=session_id,
        action=action,
    ))
    db.session.commit()


@app.route("/api/ai/explain-topic", methods=["POST"])
@login_required
@student_required
def ai_explain_topic():
    err, ai = _ai_check_access()
    if err:
        return err
    payload = request.get_json(silent=True) or {}
    session_obj = db.session.get(Session, payload.get("session_id"))
    if not session_obj:
        return jsonify({"reply": "Session not found. Please refresh the page."})
    _log_ai_usage("explain_topic", session_obj.id)
    reply = ai.explain_topic(session_obj)
    return jsonify({"reply": reply})


@app.route("/api/ai/explain-error", methods=["POST"])
@login_required
@student_required
def ai_explain_error():
    err, ai = _ai_check_access()
    if err:
        return err
    payload = request.get_json(silent=True) or {}
    session_obj = db.session.get(Session, payload.get("session_id"))
    if not session_obj:
        return jsonify({"reply": "Session not found. Please refresh the page."})
    code = payload.get("code", "")
    error_text = payload.get("error", "")
    if not error_text:
        return jsonify({"reply": "No error message provided. Run your code first to see if there are errors."})
    _log_ai_usage("explain_error", session_obj.id)
    reply = ai.explain_error(error_text, code, session_obj)
    return jsonify({"reply": reply})


@app.route("/api/ai/review-code", methods=["POST"])
@login_required
@student_required
def ai_review_code():
    err, ai = _ai_check_access()
    if err:
        return err
    payload = request.get_json(silent=True) or {}
    session_obj = db.session.get(Session, payload.get("session_id"))
    if not session_obj:
        return jsonify({"reply": "Session not found. Please refresh the page."})
    code = payload.get("code", "")
    if not code.strip():
        return jsonify({"reply": "Write some code first, and I will review it for quality and best practices!"})
    _log_ai_usage("review_code", session_obj.id)
    reply = ai.review_code(code, session_obj)
    return jsonify({"reply": reply})


@app.route("/api/ai/generate-questions", methods=["POST"])
@login_required
@student_required
def ai_generate_questions():
    err, ai = _ai_check_access()
    if err:
        return err
    payload = request.get_json(silent=True) or {}
    session_obj = db.session.get(Session, payload.get("session_id"))
    if not session_obj:
        return jsonify({"reply": "Session not found. Please refresh the page."})
    _log_ai_usage("generate_questions", session_obj.id)
    reply = ai.generate_questions(session_obj)
    return jsonify({"reply": reply})


@app.route("/api/admin/ai/generate-questions", methods=["POST"])
@login_required
@admin_required
def admin_ai_generate_questions():
    ai = get_ai_service()
    if not ai.is_configured:
        return jsonify({"error": "AI service is not configured. Please check your environment variables."}), 503

    payload = request.get_json(silent=True) or {}
    topic = payload.get("topic", "").strip()
    num_questions = int(payload.get("num_questions", 5))
    question_types = payload.get("question_types", ["mcq"])
    difficulty = payload.get("difficulty", "Professional")
    context_type = payload.get("context_type", "exam")

    if not topic:
        return jsonify({"error": "Topic is required."}), 400

    try:
        questions = ai.generate_structured_questions(
            topic=topic,
            num_questions=num_questions,
            question_types=question_types,
            difficulty=difficulty,
            context_type=context_type
        )
        return jsonify({"questions": questions})
    except Exception as e:
        return jsonify({"error": f"Failed to generate questions: {str(e)}"}), 500



@app.route("/api/ai/generate-project", methods=["POST"])
@login_required
@student_required
def ai_generate_project():
    err, ai = _ai_check_access()
    if err:
        return err
    payload = request.get_json(silent=True) or {}
    session_obj = db.session.get(Session, payload.get("session_id"))
    if not session_obj:
        return jsonify({"reply": "Session not found. Please refresh the page."})
    _log_ai_usage("generate_project", session_obj.id)
    reply = ai.generate_project(session_obj)
    return jsonify({"reply": reply})


@app.route("/api/ai/summarize", methods=["POST"])
@login_required
@student_required
def ai_summarize():
    err, ai = _ai_check_access()
    if err:
        return err
    payload = request.get_json(silent=True) or {}
    session_obj = db.session.get(Session, payload.get("session_id"))
    if not session_obj:
        return jsonify({"reply": "Session not found. Please refresh the page."})
    _log_ai_usage("summarize", session_obj.id)
    reply = ai.summarize_session(session_obj)
    return jsonify({"reply": reply})


@app.route("/api/ai/career-coach", methods=["POST"])
@login_required
@student_required
def ai_career_coach():
    err, ai = _ai_check_access()
    if err:
        return err
    payload = request.get_json(silent=True) or {}
    session_obj = db.session.get(Session, payload.get("session_id"))
    if not session_obj:
        return jsonify({"reply": "Session not found. Please refresh the page."})
    _log_ai_usage("career_coach", session_obj.id)
    reply = ai.career_guidance(session_obj)
    return jsonify({"reply": reply})


@app.route("/api/ai/analyze-dataset", methods=["POST"])
@login_required
@student_required
def ai_analyze_dataset():
    err, ai = _ai_check_access()
    if err:
        return err
    session_id = request.form.get("session_id")
    session_obj = db.session.get(Session, session_id) if session_id else None
    if not session_obj:
        return jsonify({"reply": "Session not found. Please refresh the page."})
    uploaded = request.files.get("dataset")
    if not uploaded or not uploaded.filename:
        return jsonify({"reply": "Please upload a CSV, Excel, or JSON file to analyze."})
    filename = secure_filename(uploaded.filename)
    ext = os.path.splitext(filename)[1].lower()
    if ext not in {".csv", ".xlsx", ".xls", ".json"}:
        return jsonify({"reply": "Unsupported file format. Please upload CSV, Excel (.xlsx/.xls), or JSON files."})
    try:
        raw = uploaded.read(2 * 1024 * 1024)  # Max 2MB
        content = raw.decode("utf-8", errors="replace")
    except Exception:
        return jsonify({"reply": "Could not read the uploaded file. Please check the file format."})
    _log_ai_usage("analyze_dataset", session_obj.id)
    reply = ai.analyze_dataset(content, filename, session_obj)
    return jsonify({"reply": reply})


@app.route("/api/ai/chat", methods=["POST"])
@login_required
@student_required
def ai_chat():
    err, ai = _ai_check_access()
    if err:
        return err
    payload = request.get_json(silent=True) or {}
    session_obj = db.session.get(Session, payload.get("session_id"))
    if not session_obj:
        return jsonify({"reply": "Session not found. Please refresh the page."})
    query = payload.get("query", "").strip()
    code = payload.get("code", "")
    if not query:
        return jsonify({"reply": "Please type a question and I will help you!"})
    
    # Save student message to chat history
    try:
        user_msg = AIChatMessage(
            user_id=current_user.id,
            session_id=session_obj.id,
            role="user",
            content=query
        )
        db.session.add(user_msg)
        db.session.commit()
    except Exception:
        pass

    # Retrieve recent chat history (e.g. last 10 messages) for conversational context
    history_list = []
    try:
        past_msgs = AIChatMessage.query.filter_by(
            user_id=current_user.id,
            session_id=session_obj.id
        ).order_by(AIChatMessage.created_at.asc()).all()
        # Exclude the message we just added so it's not duplicated
        history_list = [{
            "role": msg.role,
            "content": msg.content
        } for msg in past_msgs[:-1]]
    except Exception:
        pass

    _log_ai_usage("chat", session_obj.id)
    
    # Generate contextual reply
    reply = ai.chat(query, code, session_obj, history=history_list)
    
    # Save AI response to chat history
    try:
        ai_msg = AIChatMessage(
            user_id=current_user.id,
            session_id=session_obj.id,
            role="assistant",
            content=reply
        )
        db.session.add(ai_msg)
        db.session.commit()
    except Exception:
        pass

    return jsonify({"reply": reply})


@app.route("/api/ai/chat/history", methods=["GET"])
@login_required
@student_required
def get_ai_chat_history():
    session_id = request.args.get("session_id", type=int)
    if not session_id:
        return jsonify([])
    messages = AIChatMessage.query.filter_by(
        user_id=current_user.id,
        session_id=session_id
    ).order_by(AIChatMessage.created_at.asc()).all()
    
    return jsonify([{
        "role": msg.role,
        "content": msg.content
    } for msg in messages])


@app.route("/api/ai/chat/clear", methods=["POST"])
@login_required
@student_required
def clear_ai_chat_history():
    payload = request.get_json(silent=True) or {}
    session_id = payload.get("session_id")
    if not session_id:
        return jsonify({"error": "No session ID provided."}), 400
    AIChatMessage.query.filter_by(
        user_id=current_user.id,
        session_id=session_id
    ).delete()
    db.session.commit()
    return jsonify({"success": True})


# --- Admin AI Management ---

@app.route("/admin/ai/toggle", methods=["POST"])
@login_required
@admin_required
def admin_ai_toggle():
    setting = PlatformSetting.query.filter_by(key="ai_enabled").first()
    if not setting:
        setting = PlatformSetting(key="ai_enabled", value="true")
        db.session.add(setting)
    setting.value = "false" if setting.value == "true" else "true"
    db.session.commit()
    status = "enabled" if setting.value == "true" else "disabled"
    log_activity("admin.ai.toggle", status)
    flash(f"AI assistance has been {status} platform-wide.", "success")
    return redirect(url_for("admin_panel"))


@app.route("/admin/ai/stats")
@login_required
@admin_required
def admin_ai_stats():
    from sqlalchemy import func
    total = AIUsageLog.query.count()
    today_start = utc_now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_count = AIUsageLog.query.filter(AIUsageLog.created_at >= today_start).count()
    unique_users = db.session.query(func.count(func.distinct(AIUsageLog.user_id))).scalar() or 0
    popular = db.session.query(
        AIUsageLog.action, func.count(AIUsageLog.id).label("cnt")
    ).group_by(AIUsageLog.action).order_by(func.count(AIUsageLog.id).desc()).first()
    popular_action = popular[0] if popular else "N/A"
    recent = AIUsageLog.query.order_by(AIUsageLog.created_at.desc()).limit(20).all()
    recent_list = []
    for log_entry in recent:
        user = db.session.get(User, log_entry.user_id)
        recent_list.append({
            "user": user.name if user else "Unknown",
            "action": log_entry.action,
            "session_id": log_entry.session_id,
            "timestamp": log_entry.created_at.strftime("%Y-%m-%d %H:%M") if log_entry.created_at else "",
        })
    return jsonify({
        "total": total,
        "today": today_count,
        "unique_users": unique_users,
        "popular_action": popular_action,
        "recent": recent_list,
    })



@app.post("/session/<slug>/complete")
@login_required
@student_required
def complete_session(slug: str):
    session = Session.query.filter_by(slug=slug, published=True).first_or_404()
    
    quiz_questions = parse_quiz(session.quiz_json)
    if quiz_questions:
        res = QuizResult.query.filter_by(user_id=current_user.id, session_id=session.id).first()
        if not res or res.score < 60:
            flash("You must take and pass the quiz for this session with at least 60% before marking it as completed.", "error")
            return redirect(url_for("session_detail", slug=slug) + "?tab=quiz-tab")
            
    progress = UserProgress.query.filter_by(user_id=current_user.id, session_id=session.id).first()
    if not progress:
        progress = UserProgress(user_id=current_user.id, session_id=session.id)
    progress.completed = True
    progress.progress_percentage = 100
    progress.completed_at = utc_now()
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
    session = Session.query.filter_by(slug=slug, published=True).first_or_404()
    quiz_questions = parse_quiz(session.quiz_json)
    if not quiz_questions:
        flash("This session does not have a quiz configured.", "error")
        return redirect(url_for("session_detail", slug=slug))
        
    user_answers = {}
    correct_count = 0
    total_questions = len(quiz_questions)
    
    for idx, q in enumerate(quiz_questions):
        key = f"q_{idx}"
        val = request.form.get(key)
        user_answers[key] = val
        if val is not None:
            try:
                val_int = int(val)
                correct_idx = q.get("correct")
                if val_int == correct_idx:
                    correct_count += 1
            except (ValueError, TypeError):
                pass
                
    score = int((correct_count / total_questions) * 100) if total_questions else 0
    
    quiz_result = QuizResult.query.filter_by(user_id=current_user.id, session_id=session.id).first()
    if not quiz_result:
        quiz_result = QuizResult(user_id=current_user.id, session_id=session.id)
    quiz_result.score = score
    quiz_result.answers = json.dumps(user_answers)
    quiz_result.created_at = utc_now()
    db.session.add(quiz_result)
    db.session.commit()
    
    log_activity("student.session.quiz_submit", session.slug)
    
    if score >= 60:
        flash(f"You passed the quiz with a score of {score}%! You can now mark the session as completed and proceed.", "success")
    else:
        flash(f"You scored {score}%. You need at least 60% to pass and unlock the next session. Please try again.", "error")
        
    return redirect(url_for("session_detail", slug=slug) + "?tab=quiz-tab")


@app.post("/session/<slug>/quiz/reset")
@login_required
@student_required
def reset_quiz(slug: str):
    session = Session.query.filter_by(slug=slug, published=True).first_or_404()
    QuizResult.query.filter_by(user_id=current_user.id, session_id=session.id).delete()
    db.session.commit()
    flash("Quiz reset successfully. You can now retake the quiz.", "success")
    return redirect(url_for("session_detail", slug=slug) + "?tab=quiz-tab")


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
        flash("You do not have access to this exam.", "error")
        return redirect(url_for("exams_dashboard"))
    now = utc_now()
    if exam.start_time and to_naive(exam.start_time) > now:
        flash("Exam has not started yet.", "error")
        return redirect(url_for("exams_dashboard"))
    if exam.end_time and to_naive(exam.end_time) < now:
        flash("Exam window has closed.", "error")
        return redirect(url_for("exams_dashboard"))

    # Check if student has already passed this exam
    passed_attempt = ExamAttemptRecord.query.filter_by(
        user_id=current_user.id, 
        exam_id=exam.id,
        status="submitted"
    ).filter(ExamAttemptRecord.score >= exam.passing_score).first()
    if passed_attempt:
        flash("You have already passed this exam.", "success")
        return redirect(url_for("exams_dashboard"))

    prior_attempts = ExamAttemptRecord.query.filter_by(user_id=current_user.id, exam_id=exam.id).count()
    if prior_attempts >= 3:
        flash("Attempt limit reached. You are only allowed 2 other trials after failing.", "error")
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
            server_time_ms=int(utc_now().timestamp() * 1000),
            started_at_ms=int(to_naive(attempt.created_at).timestamp() * 1000),
        )

    # POST submit
    if not attempt:
        flash("No active exam attempt found.", "error")
        return redirect(url_for("exams_dashboard"))

    elapsed = (utc_now() - to_naive(attempt.created_at)).total_seconds() / 60
    if elapsed > exam.duration + 1:
        flash("Exam submission rejected: time limit exceeded.", "error")
        attempt.submitted_at = utc_now()
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

    attempt.submitted_at = utc_now()
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
        attempt.submitted_at = utc_now()
    db.session.add(
        IntegrityLog(
            user_id=current_user.id,
            exam_id=attempt.exam_id,
            violation_type=violation_type,
            severity="high" if terminate else "warning",
            details=f"count={attempt.violation_count}",
        )
    )
    return jsonify({"ok": True, "terminate": terminate, "count": attempt.violation_count})


@app.post("/exams/check-answer")
@login_required
@student_required
def check_exam_question_answer():
    question_id = request.form.get("question_id", type=int)
    selected_option = request.form.get("selected_option", "").strip()

    question = db.session.get(Question, question_id)
    if not question:
        return jsonify({"ok": False, "error": "Question not found"}), 404

    options = json.loads(question.options or "[]")
    correct_idx_str = str(question.correct_answer or "")

    is_correct = (selected_option == correct_idx_str)

    # Get the option texts
    correct_option_text = ""
    try:
        correct_idx = int(correct_idx_str)
        if 0 <= correct_idx < len(options):
            correct_option_text = options[correct_idx]
    except ValueError:
        correct_option_text = correct_idx_str

    selected_option_text = ""
    try:
        selected_idx = int(selected_option)
        if 0 <= selected_idx < len(options):
            selected_option_text = options[selected_idx]
    except ValueError:
        selected_option_text = selected_option

    # Generate short explanation using AI
    ai_service = get_ai_service()

    prompt = f"""You are a Python for Data Science tutor. A student is taking a quiz/exam.
Question: {question.question_text}
Options:
{chr(10).join([f'- Index {i}: {opt}' for i, opt in enumerate(options)])}
Correct Option Index: {correct_idx_str} ({correct_option_text})
Student Selected Option Index: {selected_option} ({selected_option_text})

Please provide a short explanation (1-3 sentences) explaining why the student's answer is {"correct" if is_correct else "incorrect"}, and explain the correct choice clearly. Keep it very concise (under 80 words) and helpful."""

    explanation = "AI explanation is not configured."
    if ai_service.is_configured:
        if ai_service.check_rate_limit(current_user.id):
            explanation = ai_service._call(prompt, max_tokens=150)
            db.session.add(AIUsageLog(user_id=current_user.id, action="exam_check_answer"))
            db.session.commit()
        else:
            explanation = "You are sending requests too quickly. Please wait a moment."
    else:
        if is_correct:
            explanation = f"Correct! '{correct_option_text}' is the right answer."
        else:
            explanation = f"Incorrect. The correct answer is '{correct_option_text}'."

    return jsonify({
        "ok": True,
        "correct": is_correct,
        "correct_option_index": correct_idx_str,
        "correct_option_text": correct_option_text,
        "explanation": explanation
    })





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
        
        start_time = None
        if start_time_raw:
            try:
                start_time = datetime.fromisoformat(start_time_raw)
            except Exception:
                pass
                
        end_time = None
        if end_time_raw:
            try:
                end_time = datetime.fromisoformat(end_time_raw)
            except Exception:
                pass
        
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
            published=True,
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
        notes_name = None
        notes_data = None
        if uploaded_note and uploaded_note.filename:
            UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
            safe_name = secure_filename(uploaded_note.filename)
            stored_name = f"{slug}-{int(utc_now().timestamp())}-{safe_name}"
            destination = UPLOADS_DIR / stored_name
            notes_data = uploaded_note.read()
            uploaded_note.seek(0)
            uploaded_note.save(destination)
            notes_path = f"uploads/notes/{stored_name}"
            notes_name = safe_name
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
            notes_file_name=notes_name,
            notes_file_data=notes_data,
            video_url=request.form.get("video_url", "").strip() or None,
            duration=request.form.get("duration", "60 min"),
            difficulty=request.form.get("difficulty", "Beginner"),
            display_order=int(request.form.get("display_order", Session.query.count() + 1)),
            published=request.form.get("published") == "on",
            quiz_json=request.form.get("quiz_json", "[]"),
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
            stored_name = f"{session_obj.slug}-{int(utc_now().timestamp())}-{safe_name}"
            destination = UPLOADS_DIR / stored_name
            session_obj.notes_file_data = uploaded_note.read()
            uploaded_note.seek(0)
            uploaded_note.save(destination)
            session_obj.notes_file_path = f"uploads/notes/{stored_name}"
            session_obj.notes_file_name = safe_name
        session_obj.duration = request.form.get("duration", "60 min")
        session_obj.difficulty = request.form.get("difficulty", "Beginner")
        session_obj.display_order = int(request.form.get("display_order", session_obj.display_order))
        session_obj.published = request.form.get("published") == "on"
        session_obj.quiz_json = request.form.get("quiz_json", "[]")
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


@app.route("/admin/users/new", methods=["GET", "POST"])
@login_required
@admin_required
def admin_register_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        reg_number = request.form.get("reg_number", "").strip().upper()
        password = request.form.get("password", "")
        study_level = request.form.get("study_level", "Beginner").strip() or "Beginner"
        
        if not all([name, reg_number, password]):
            flash("All fields are required.", "error")
            return redirect(url_for("admin_register_student"))
            
        if User.query.filter_by(reg_number=reg_number).first():
            flash("An account with this registration number already exists.", "error")
            return redirect(url_for("admin_register_student"))
            
        user = User(
            name=name,
            email=f"{reg_number.replace('/', '_')}@cdam.local",
            reg_number=reg_number,
            password_hash=generate_password_hash(password),
            avatar=CDAM_LOGO,
            study_level=study_level,
            is_admin=False,
            require_password_change=True,
        )
        db.session.add(user)
        db.session.commit()
        log_activity("admin.user.create", f"Reg={reg_number}, level={study_level}")
        flash(f"Student account created successfully. Email: {user.email}", "success")
        return redirect(url_for("admin_panel"))
        
    return render_template("admin_student_new.html")


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


@app.post("/admin/users/<int:user_id>/require-password-change")
@login_required
@admin_required
def admin_require_password_change(user_id: int):
    user = db.session.get(User, user_id)
    if not user or user.is_admin:
        flash("Cannot require password change for this user.", "error")
        return redirect(url_for("admin_panel"))
    user.require_password_change = not user.require_password_change
    db.session.commit()
    status = "requested" if user.require_password_change else "cancelled"
    log_activity("admin.user.require_password_change", f"user={user.id}:status={status}")
    flash(f"Password change requirement {status} for student.", "success")
    return redirect(url_for("admin_student_detail", user_id=user_id))


@app.post("/admin/users/<int:user_id>/approve-reset")
@login_required
@admin_required
def admin_approve_password_reset(user_id: int):
    user = db.session.get(User, user_id)
    if not user or user.is_admin:
        flash("Cannot approve password reset for this user.", "error")
        return redirect(url_for("admin_panel"))
    user.password_reset_status = "approved"
    db.session.commit()
    log_activity("admin.user.approve_password_reset", f"user={user.id}")
    flash("Password reset request approved. The student can now set their new password.", "success")
    ref = request.referrer or ""
    if "admin/student/" in ref or "user_id=" in ref:
        return redirect(url_for("admin_student_detail", user_id=user_id))
    return redirect(url_for("admin_panel"))


@app.post("/admin/users/<int:user_id>/reject-reset")
@login_required
@admin_required
def admin_reject_password_reset(user_id: int):
    user = db.session.get(User, user_id)
    if not user or user.is_admin:
        flash("Cannot perform this action.", "error")
        return redirect(url_for("admin_panel"))
    user.password_reset_status = None
    db.session.commit()
    log_activity("admin.user.reject_password_reset", f"user={user.id}")
    flash("Password reset request cleared.", "success")
    ref = request.referrer or ""
    if "admin/student/" in ref or "user_id=" in ref:
        return redirect(url_for("admin_student_detail", user_id=user_id))
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
        start_time_raw = request.form.get("start_time", "").strip()
        end_time_raw = request.form.get("end_time", "").strip()
        
        start_time = None
        if start_time_raw:
            try:
                start_time = datetime.fromisoformat(start_time_raw)
            except Exception:
                pass
                
        end_time = None
        if end_time_raw:
            try:
                end_time = datetime.fromisoformat(end_time_raw)
            except Exception:
                pass
                
        exam.start_time = start_time
        exam.end_time = end_time
        raw_questions = request.form.get("questions_json", "")
        if raw_questions.strip():
            try:
                new_questions = json.loads(raw_questions)
                existing_questions = Question.query.filter_by(exam_id=exam.id).order_by(Question.id).all()
                changed = len(new_questions) != len(existing_questions)
                if not changed:
                    for i, eq in enumerate(existing_questions):
                        nq = new_questions[i]
                        nq_text = nq.get("questionText", "")
                        nq_type = nq.get("questionType", "mcq")
                        nq_options = json.dumps(nq.get("options", []))
                        nq_correct = str(nq.get("correctAnswer", ""))
                        nq_marks = int(nq.get("marks", 1))
                        
                        try:
                            eq_options_norm = json.dumps(json.loads(eq.options or "[]"))
                        except Exception:
                            eq_options_norm = "[]"
                        try:
                            nq_options_norm = json.dumps(json.loads(nq_options))
                        except Exception:
                            nq_options_norm = "[]"
                        
                        if (eq.question_text != nq_text or
                            eq.question_type != nq_type or
                            eq_options_norm != nq_options_norm or
                            eq.correct_answer != nq_correct or
                            eq.marks != nq_marks):
                            changed = True
                            break
                if changed:
                    Question.query.filter_by(exam_id=exam.id).delete()
                    for q in new_questions:
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
    # Also pass active/ongoing attempts to the template for monitoring
    attempts = ExamAttemptRecord.query.order_by(ExamAttemptRecord.created_at.desc()).all()
    return render_template("admin_integrity.html", logs=logs, users_map=users_map, exams_map=exams_map, attempts=attempts)


@app.post("/admin/users/<int:user_id>/delete")
@login_required
@admin_required
def admin_delete_user(user_id: int):
    user = db.session.get(User, user_id)
    if not user or user.is_admin:
        flash("User cannot be deleted.", "error")
        return redirect(url_for("admin_panel"))
    # Cascade delete relations:
    UserProgress.query.filter_by(user_id=user.id).delete()
    QuizResult.query.filter_by(user_id=user.id).delete()
    Bookmark.query.filter_by(user_id=user.id).delete()
    LessonView.query.filter_by(user_id=user.id).delete()
    ActivityLog.query.filter_by(user_id=user.id).delete()
    Notification.query.filter_by(user_id=user.id).delete()
    DiscussionComment.query.filter_by(user_id=user.id).delete()
    ExamAttemptRecord.query.filter_by(user_id=user.id).delete()
    IntegrityLog.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    log_activity("admin.user.delete", user.email)
    flash(f"Student account '{user.name}' has been deleted.", "success")
    return redirect(url_for("admin_panel"))


@app.route("/admin/users/<int:user_id>/detail")
@login_required
@admin_required
def admin_student_detail(user_id: int):
    user = db.session.get(User, user_id)
    if not user or user.is_admin:
        flash("User not found.", "error")
        return redirect(url_for("admin_panel"))
    
    # Study analytics
    completed_progress = UserProgress.query.filter_by(user_id=user.id, completed=True).all()
    completed_sessions = [p.session_id for p in completed_progress]
    
    # Quiz results
    quiz_results = QuizResult.query.filter_by(user_id=user.id).all()
    
    # Exam history
    exam_attempts = ExamAttemptRecord.query.filter_by(user_id=user.id).all()
    
    # Activity logs
    activities = ActivityLog.query.filter_by(user_id=user.id).order_by(ActivityLog.created_at.desc()).all()
    
    # Bookmarks
    bookmarks = Bookmark.query.filter_by(user_id=user.id).all()
    
    # Map sessions and exams for easy templates rendering
    sessions_map = {s.id: s for s in Session.query.all()}
    exams_map = {e.id: e for e in Exam.query.all()}
    
    return render_template(
        "admin_student_detail.html",
        student=user,
        completed_sessions=completed_sessions,
        quiz_results=quiz_results,
        exam_attempts=exam_attempts,
        activities=activities,
        bookmarks=bookmarks,
        sessions_map=sessions_map,
        exams_map=exams_map
    )


@app.post("/admin/attempts/<int:attempt_id>/action")
@login_required
@admin_required
def admin_attempt_action(attempt_id: int):
    attempt = db.session.get(ExamAttemptRecord, attempt_id)
    if not attempt:
        flash("Attempt not found.", "error")
        return redirect(url_for("admin_integrity"))
    action = request.form.get("action", "").strip()
    if action == "force_submit":
        attempt.status = "submitted"
        attempt.submitted_at = utc_now()
        flash("Exam attempt force-submitted successfully.", "success")
        log_activity("admin.exam.force_submit", f"attempt={attempt_id}")
    elif action == "terminate":
        attempt.status = "terminated"
        attempt.submitted_at = utc_now()
        flash("Exam attempt terminated.", "success")
        log_activity("admin.exam.terminate", f"attempt={attempt_id}")
    elif action == "flag":
        attempt.status = "flagged"
        flash("Exam attempt flagged for review.", "success")
        log_activity("admin.exam.flag", f"attempt={attempt_id}")
    elif action == "approve":
        attempt.status = "submitted"
        flash("Exam attempt approved / cleared.", "success")
        log_activity("admin.exam.approve", f"attempt={attempt_id}")
    else:
        flash("Invalid action.", "error")
    db.session.commit()
    return redirect(url_for("admin_integrity"))



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
        if "notes_file_name" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE sessions ADD COLUMN notes_file_name VARCHAR(255)"))
        if "notes_file_data" not in columns:
            with db.engine.begin() as conn:
                db_type = "LONGBLOB" if "mysql" in str(db.engine.url) else "BLOB"
                conn.execute(text(f"ALTER TABLE sessions ADD COLUMN notes_file_data {db_type}"))
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
        if "require_password_change" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN require_password_change BOOLEAN DEFAULT 0"))
        if "password_reset_status" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN password_reset_status VARCHAR(30)"))
    if "exams" in inspector.get_table_names():
        columns = {col["name"] for col in inspector.get_columns("exams")}
        if "study_level" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE exams ADD COLUMN study_level VARCHAR(30) DEFAULT 'Beginner'"))
    if "user_sandbox_files" in inspector.get_table_names():
        columns = {col["name"] for col in inspector.get_columns("user_sandbox_files")}
        if "is_global" not in columns:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE user_sandbox_files ADD COLUMN is_global BOOLEAN DEFAULT 0"))


def initialize():
    with app.app_context():
        db.create_all()
        migrate_schema()
        seed_sessions()
        try:
            for e in Exam.query.all():
                if not e.published:
                    e.published = True
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            print(f"Error auto-publishing exams: {ex}")
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
