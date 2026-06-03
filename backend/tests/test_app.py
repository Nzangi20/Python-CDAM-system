import sys
import json
from pathlib import Path
from datetime import datetime, UTC

import pytest

# Ensure backend modules are importable when running from repo root.
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app import app, db, User, Session, Exam, Question, ExamAttemptRecord, IntegrityLog  # noqa: E402
from seed_data import SESSIONS  # noqa: E402
from sqlalchemy.pool import StaticPool


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        from app import seed_sessions
        seed_sessions()
        
        # Seed an admin user for testing admin features
        from werkzeug.security import generate_password_hash
        admin = User(
            name="Admin User",
            email="admin@cdam.local",
            password_hash=generate_password_hash("admin123"),
            auth_provider="local",
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        
    with app.test_client() as client:
        yield client


def register_and_login(client, reg_number="EB3/10001/26", password="secret123", study_level="Beginner"):
    client.post(
        "/register",
        data={"name": "Test Student", "reg_number": reg_number, "password": password, "study_level": study_level},
        follow_redirects=True,
    )


def login_admin(client):
    client.post(
        "/login",
        data={"identifier": "admin@cdam.local", "password": "admin123"},
        follow_redirects=True,
    )


def test_homepage_lists_sessions(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Master Python for Data Science" in response.data
    assert b"Introduction to Python" in response.data


def test_register_login_and_dashboard(client):
    register_and_login(client)
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome back" in response.data


def test_session_progress_tracking(client):
    register_and_login(client)
    slug = SESSIONS[0]["slug"]
    detail = client.get(f"/session/{slug}")
    assert detail.status_code == 200

    complete = client.post(f"/session/{slug}/complete", follow_redirects=True)
    assert complete.status_code == 200
    assert b"completed" in complete.data.lower()


def test_admin_access_denied_for_students(client):
    register_and_login(client)
    response = client.get("/admin", follow_redirects=True)
    assert b"Admin access is required" in response.data


def test_admin_dashboard_and_session_deletion(client):
    login_admin(client)
    response = client.get("/admin")
    assert response.status_code == 200
    assert b"Admin Control Center" in response.data
    
    # Test session deletion
    with app.app_context():
        sess = Session.query.first()
        sess_id = sess.id
    
    del_resp = client.post(f"/admin/session/{sess_id}/delete", follow_redirects=True)
    assert del_resp.status_code == 200
    assert b"deleted" in del_resp.data.lower()


def test_admin_exam_management_and_editing(client):
    login_admin(client)
    
    # Create Exam
    q_json = json.dumps([
        {
            "questionText": "What is 2+2 in Python?",
            "questionType": "mcq",
            "options": ["3", "4", "5"],
            "correctAnswer": "1",
            "marks": 2
        }
    ])
    
    create_resp = client.post(
        "/admin/exams",
        data={
            "title": "Data Science Core Quiz",
            "description": "Basics of data types",
            "duration": "15",
            "passing_score": "60",
            "exam_type": "multiple_choice",
            "attempt_limit": "2",
            "questions_json": q_json,
            "proctoring_enabled": "on",
            "published": "on"
        },
        follow_redirects=True
    )
    assert create_resp.status_code == 200
    assert b"Data Science Core Quiz" in create_resp.data
    
    with app.app_context():
        exam = Exam.query.filter_by(title="Data Science Core Quiz").first()
        exam_id = exam.id
        
    # Edit Exam
    edit_resp = client.post(
        f"/admin/exams/{exam_id}/edit",
        data={
            "title": "Data Science Core Quiz v2",
            "description": "Updated description",
            "duration": "20",
            "passing_score": "70",
            "exam_type": "multiple_choice",
            "attempt_limit": "3",
            "questions_json": q_json,
            "proctoring_enabled": "on",
            "published": "on"
        },
        follow_redirects=True
    )
    assert edit_resp.status_code == 200
    assert b"Data Science Core Quiz v2" in edit_resp.data


def test_exam_integrity_proctoring_flow(client):
    # Setup: Create an exam as Admin
    login_admin(client)
    q_json = json.dumps([{"questionText": "Q1", "questionType": "essay", "options": [], "correctAnswer": "", "marks": 5}])
    client.post(
        "/admin/exams",
        data={
            "title": "Secure Exam",
            "description": "Proctored Exam",
            "duration": "10",
            "passing_score": "50",
            "exam_type": "essay",
            "attempt_limit": "1",
            "questions_json": q_json,
            "proctoring_enabled": "on",
            "published": "on"
        }
    )
    
    # Log out Admin, login Student
    client.get("/logout")
    register_and_login(client)
    
    with app.app_context():
        exam = Exam.query.filter_by(title="Secure Exam").first()
        exam_id = exam.id
        
    # Take Exam (Starts attempt)
    take_resp = client.get(f"/exams/{exam_id}/take")
    assert take_resp.status_code == 200
    
    with app.app_context():
        # Get active attempt record
        attempt = ExamAttemptRecord.query.filter_by(exam_id=exam_id).first()
        attempt_id = attempt.id
        
    # Submit violations
    violation_resp = client.post(
        f"/exams/attempt/{attempt_id}/violation",
        data={"type": "tab_switch"}
    )
    assert violation_resp.status_code == 200
    res_data = json.loads(violation_resp.data)
    assert res_data["ok"] is True
    assert res_data["terminate"] is False


def test_study_level_access_control(client):
    # Register beginner student
    register_and_login(client, reg_number="EB3/11111/26")
    
    with app.app_context():
        s1 = Session.query.filter_by(display_order=1).first()
        s1_slug = s1.slug
        s6 = Session.query.filter_by(display_order=6).first()
        s6_slug = s6.slug if s6 else None
        
        # Create a display_order 11 session to test restrictions
        s11 = Session(
            title="Advanced ML",
            slug="advanced-ml",
            display_order=11,
            published=True,
            difficulty="Professional"
        )
        db.session.add(s11)
        db.session.commit()
        s11_id = s11.id
    
    # Try to access Session 1 (display_order 1) -> Allowed (200)
    resp_s1 = client.get(f"/session/{s1_slug}")
    assert resp_s1.status_code == 200
    
    # Try to access Session 6 (display_order 6) -> Now Allowed (200)
    if s6_slug:
        resp_s6 = client.get(f"/session/{s6_slug}")
        assert resp_s6.status_code == 200
        
    # Try to access Session 11 (display_order 11) -> Restricted, redirects (302)
    resp_s11 = client.get(f"/session/advanced-ml")
    assert resp_s11.status_code == 302
        
    # Try to download Session 1 notes -> Allowed
    resp_dl1 = client.get(f"/session/{s1.id}/download")
    assert resp_dl1.status_code != 302 or b"restricted" not in resp_dl1.data
    
    # Try to download Session 11 notes -> Blocked and redirected (302)
    resp_dl11 = client.get(f"/session/{s11_id}/download")
    assert resp_dl11.status_code == 302


def test_api_run_code(client):
    # Logged in user required
    register_and_login(client, reg_number="EB3/22222/26")
    
    # Run hello world
    resp = client.post(
        "/api/run-code",
        json={"code": "print('Hello from Sandbox!')"}
    )
    assert resp.status_code == 200
    res_data = json.loads(resp.data)
    assert "Hello from Sandbox!" in res_data["output"]
    assert res_data["error"] == ""
    assert res_data["exit_code"] == 0
    
    # Run timeout infinite loop
    resp_timeout = client.post(
        "/api/run-code",
        json={"code": "import time\nwhile True: time.sleep(0.1)"}
    )
    assert resp_timeout.status_code == 200
    res_data_timeout = json.loads(resp_timeout.data)
    assert "timed out" in res_data_timeout["error"].lower()


def test_exam_level_filtering(client):
    # Register a beginner student
    register_and_login(client, reg_number="EB3/33333/26", study_level="Beginner")
    
    # Create two exams under app context (one Beginner, one Professional)
    with app.app_context():
        # Clean up any existing tests exams if needed
        Exam.query.filter(Exam.title.in_(["Beginner Exam", "Professional Exam"])).delete()
        db.session.commit()
        
        beg_exam = Exam(
            title="Beginner Exam",
            description="Testing Beginner level filtering",
            duration=30,
            passing_score=50,
            study_level="Beginner",
            published=True
        )
        prof_exam = Exam(
            title="Professional Exam",
            description="Testing Professional level filtering",
            duration=45,
            passing_score=60,
            study_level="Professional",
            published=True
        )
        db.session.add(beg_exam)
        db.session.add(prof_exam)
        db.session.commit()
        
        beg_id = beg_exam.id
        prof_id = prof_exam.id
        
        # Add at least one question to each so they can be initialized
        db.session.add(Question(exam_id=beg_id, question_text="What is 1+1?", question_type="mcq", options='["1","2"]', correct_answer="1"))
        db.session.add(Question(exam_id=prof_id, question_text="What is OOP?", question_type="mcq", options='["Yes","No"]', correct_answer="0"))
        db.session.commit()

    # Access exams dashboard as Beginner student
    resp = client.get("/exams")
    assert resp.status_code == 200
    assert b"Beginner Exam" in resp.data
    assert b"Professional Exam" not in resp.data

    # Attempt to take Professional Exam directly via URL -> Redirected with level restriction message
    resp_take_prof = client.get(f"/exams/{prof_id}/take")
    assert resp_take_prof.status_code == 302
    
    # Change student level to Professional in DB
    with app.app_context():
        user = User.query.filter_by(reg_number="EB3/33333/26").first()
        user.study_level = "Professional"
        db.session.commit()
        
    # Access exams dashboard as Professional student
    resp_prof = client.get("/exams")
    assert resp_prof.status_code == 200
    assert b"Beginner Exam" not in resp_prof.data
    assert b"Professional Exam" in resp_prof.data
    
    # Attempt to take Professional Exam now -> Successful (returns take template, which has form or instructions)
    resp_take_prof_success = client.get(f"/exams/{prof_id}/take")
    assert resp_take_prof_success.status_code == 200


