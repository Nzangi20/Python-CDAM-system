import sys
import json
from pathlib import Path
from datetime import datetime, UTC

import pytest
from werkzeug.security import generate_password_hash

# Ensure backend modules are importable when running from repo root.
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app import app, db, User, Session, Exam, Question, ExamAttemptRecord, IntegrityLog, UserProgress, UPLOADS_DIR  # noqa: E402
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
        s1_id = s1.id
        s1_slug = s1.slug
        s6 = Session.query.filter_by(display_order=6).first()
        s6_slug = s6.slug if s6 else None
        
        s11 = Session(
            title="Advanced ML",
            slug="advanced-ml",
            description="Learn advanced machine learning models.",
            content="Session content here.",
            objectives="Understand neural networks.",
            expected_outcomes="Able to build models.",
            learning_notes="Learning notes here.",
            instructions="Follow the instructions.",
            code_examples="print('Advanced ML')",
            resources="None",
            duration=45,
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
    resp_dl1 = client.get(f"/session/{s1_id}/download")
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
    
    # Verify sandbox can import key libraries
    resp_imports = client.post(
        "/api/run-code",
        json={"code": "import numpy as np\nimport pandas as pd\nimport sklearn\nimport seaborn as sns\nimport openpyxl\nimport statsmodels\nprint('All libraries loaded!')"}
    )
    assert resp_imports.status_code == 200
    res_data_imports = json.loads(resp_imports.data)
    assert "All libraries loaded!" in res_data_imports["output"]
    assert res_data_imports["error"] == ""
    assert res_data_imports["exit_code"] == 0

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


def test_dashboard_rendering(client):
    # Register and login a student
    register_and_login(client, reg_number="EB3/44444/26")
    
    # 1. Access dashboard with 0% progress
    resp = client.get("/student/dashboard")
    assert resp.status_code == 200
    assert b"Welcome back" in resp.data
    assert b"View Certificate" not in resp.data

    # 2. Access dashboard with 100% progress
    with app.app_context():
        user = User.query.filter_by(reg_number="EB3/44444/26").first()
        sessions = Session.query.all()
        for s in sessions:
            prog = UserProgress(user_id=user.id, session_id=s.id, completed=True, progress_percentage=100)
            db.session.add(prog)
        db.session.commit()
        
    resp_complete = client.get("/student/dashboard")
    assert resp_complete.status_code == 200
    assert b"View Certificate" in resp_complete.data


def test_admin_delete_student(client):
    # Register student
    login_admin(client)
    student_reg = "EB3/99999/26"
    
    with app.app_context():
        # Setup student user
        student = User(
            name="Delete Me Student",
            email="delete.me@cdam.local",
            reg_number=student_reg,
            password_hash=generate_password_hash("password"),
            study_level="Beginner"
        )
        db.session.add(student)
        db.session.commit()
        student_id = student.id
        
        # Add related progress, quiz, and attempt logs
        db.session.add(UserProgress(user_id=student_id, session_id=1, completed=True))
        db.session.commit()

    # Admin deletes the student
    resp = client.post(f"/admin/users/{student_id}/delete", follow_redirects=True)
    assert resp.status_code == 200
    assert b"deleted" in resp.data

    with app.app_context():
        deleted_user = db.session.get(User, student_id)
        assert deleted_user is None
        progress = UserProgress.query.filter_by(user_id=student_id).all()
        assert len(progress) == 0


def test_admin_student_detail(client):
    login_admin(client)
    with app.app_context():
        student = User(
            name="Detail Student",
            email="detail.student@cdam.local",
            reg_number="EB3/88888/26",
            password_hash=generate_password_hash("password"),
            study_level="Beginner"
        )
        db.session.add(student)
        db.session.commit()
        student_id = student.id

    resp = client.get(f"/admin/users/{student_id}/detail")
    assert resp.status_code == 200
    assert b"Detail Student" in resp.data
    assert b"EB3/88888/26" in resp.data


def test_admin_attempt_action(client):
    login_admin(client)
    with app.app_context():
        student = User(
            name="Exam Actions Student",
            email="exam.actions@cdam.local",
            reg_number="EB3/77777/26",
            password_hash=generate_password_hash("password"),
            study_level="Beginner"
        )
        db.session.add(student)
        db.session.commit()
        student_id = student.id

        exam = Exam(
            title="Integrity Exam",
            description="Testing proctor controls",
            duration=30,
            passing_score=50,
            study_level="Beginner",
            published=True
        )
        db.session.add(exam)
        db.session.commit()
        exam_id = exam.id

        attempt = ExamAttemptRecord(
            user_id=student_id,
            exam_id=exam_id,
            status="in_progress"
        )
        db.session.add(attempt)
        db.session.commit()
        attempt_id = attempt.id

    # 1. Flag attempt
    resp_flag = client.post(f"/admin/attempts/{attempt_id}/action", data={"action": "flag"}, follow_redirects=True)
    assert resp_flag.status_code == 200
    with app.app_context():
        updated_attempt = db.session.get(ExamAttemptRecord, attempt_id)
        assert updated_attempt.status == "flagged"

    # 2. Clear flags / Approve attempt
    resp_approve = client.post(f"/admin/attempts/{attempt_id}/action", data={"action": "approve"}, follow_redirects=True)
    assert resp_approve.status_code == 200
    with app.app_context():
        updated_attempt = db.session.get(ExamAttemptRecord, attempt_id)
        assert updated_attempt.status == "submitted"

    # 3. Terminate attempt
    with app.app_context():
        # Set back to in_progress to test terminate
        att = db.session.get(ExamAttemptRecord, attempt_id)
        att.status = "in_progress"
        db.session.commit()

    resp_term = client.post(f"/admin/attempts/{attempt_id}/action", data={"action": "terminate"}, follow_redirects=True)
    assert resp_term.status_code == 200
    with app.app_context():
        updated_attempt = db.session.get(ExamAttemptRecord, attempt_id)
        assert updated_attempt.status == "terminated"


def test_transcript_and_trials_limit(client):
    # 1. Register and login
    register_and_login(client, reg_number="EB3/99999/26", password="mytestpassword", study_level="Beginner")
    
    # 2. Check transcript requires 100% progress (which is currently 0%, so it should redirect)
    resp_tr = client.get("/transcript")
    assert resp_tr.status_code == 302
    
    # 3. Seed student progress to 100% to unlock transcript
    with app.app_context():
        student = User.query.filter_by(reg_number="EB3/99999/26").first()
        student_id = student.id
        
        # Complete all 10 Beginner sessions
        for i in range(1, 11):
            s = Session.query.filter_by(display_order=i).first()
            if s:
                prog = UserProgress(user_id=student_id, session_id=s.id, completed=True)
                db.session.add(prog)
        db.session.commit()
        
    resp_tr_unlocked = client.get("/transcript")
    assert resp_tr_unlocked.status_code == 200
    assert b"Official Academic Transcript" in resp_tr_unlocked.data
    assert b"EB3/99999/26" in resp_tr_unlocked.data
    
    # 4. Check trials limit logic (at most 3 attempts, blocked after passing)
    with app.app_context():
        exam = Exam(
            title="Trial Limit Exam",
            description="Testing max attempts rule",
            duration=30,
            passing_score=60,
            study_level="Beginner",
            published=True
        )
        db.session.add(exam)
        db.session.commit()
        exam_id = exam.id
        
    # Attempt 1: Failed
    with app.app_context():
        att1 = ExamAttemptRecord(user_id=student_id, exam_id=exam_id, score=45, status="submitted")
        db.session.add(att1)
        db.session.commit()
        
    # Attempt 2: Failed
    with app.app_context():
        att2 = ExamAttemptRecord(user_id=student_id, exam_id=exam_id, score=50, status="submitted")
        db.session.add(att2)
        db.session.commit()
        
    # Attempt 3: Failed
    with app.app_context():
        att3 = ExamAttemptRecord(user_id=student_id, exam_id=exam_id, score=55, status="submitted")
        db.session.add(att3)
        db.session.commit()
        
    # Attempt 4: Should be blocked by prior attempts >= 3 limit
    resp_att4 = client.get(f"/exams/{exam_id}/take")
    assert resp_att4.status_code == 302
    
    # Check that if they passed, they are also blocked from retaking
    with app.app_context():
        # Clean up database records for this exam
        ExamAttemptRecord.query.filter_by(exam_id=exam_id).delete()
        # Add a passed attempt
        att_passed = ExamAttemptRecord(user_id=student_id, exam_id=exam_id, score=85, status="submitted")
        db.session.add(att_passed)
        db.session.commit()
        
    resp_att_passed = client.get(f"/exams/{exam_id}/take")
    assert resp_att_passed.status_code == 302


def test_ai_platform_toggle(client):
    from app import PlatformSetting
    register_and_login(client)
    
    with app.app_context():
        sess = Session.query.first()
        sess_id = sess.id
        # Turn off AI
        setting = PlatformSetting.query.filter_by(key="ai_enabled").first()
        if not setting:
            setting = PlatformSetting(key="ai_enabled", value="false")
            db.session.add(setting)
        else:
            setting.value = "false"
        db.session.commit()

    # Request AI assistance while disabled
    resp = client.post("/api/ai/explain-topic", json={"session_id": sess_id})
    assert resp.status_code == 200
    data = json.loads(resp.data.decode("utf-8"))
    assert "disabled" in data["reply"].lower()

    # Re-enable AI
    with app.app_context():
        setting = PlatformSetting.query.filter_by(key="ai_enabled").first()
        setting.value = "true"
        db.session.commit()


def test_ai_exam_lockout(client):
    from app import PlatformSetting, Exam, ExamAttemptRecord, User
    register_and_login(client)
    
    with app.app_context():
        sess = Session.query.first()
        sess_id = sess.id
        # Query the registered student
        user = User.query.filter_by(reg_number="EB3/10001/26").first()
        user_id = user.id
        
        # Ensure AI is enabled
        setting = PlatformSetting.query.filter_by(key="ai_enabled").first()
        if setting:
            setting.value = "true"
            db.session.commit()
            
        # Create an exam and a record in_progress
        exam = Exam(title="ML Exam", description="...", duration=10, passing_score=60)
        db.session.add(exam)
        db.session.commit()
        
        attempt = ExamAttemptRecord(user_id=user_id, exam_id=exam.id, status="in_progress")
        db.session.add(attempt)
        db.session.commit()

    # Request AI assistance during active exam
    resp = client.post("/api/ai/explain-topic", json={"session_id": sess_id})
    assert resp.status_code == 200
    data = json.loads(resp.data.decode("utf-8"))
    assert "assessment" in data["reply"].lower() or "exam" in data["reply"].lower()

    with app.app_context():
        # Clean up the exam attempt
        ExamAttemptRecord.query.filter_by(user_id=user_id).delete()
        db.session.commit()


def test_ai_rate_limiter(client):
    from ai_service import get_ai_service, BaseProvider
    
    class DummyProvider(BaseProvider):
        def generate(self, prompt, system_instruction="", max_tokens=2048):
            return "Mocked AI Response"

    register_and_login(client)
    
    with app.app_context():
        sess = Session.query.first()
        sess_id = sess.id
        
        # Set dummy provider on global AI service
        ai_service = get_ai_service()
        old_provider = ai_service._provider
        ai_service._provider = DummyProvider()
        
        # Reset rate limiter buckets for clean test run
        ai_service._rate_limiter._buckets.clear()

    try:
        # Fire 10 fast requests (they should pass/be accepted)
        for i in range(10):
            resp = client.post("/api/ai/explain-topic", json={"session_id": sess_id})
            assert resp.status_code == 200
            data = json.loads(resp.data.decode("utf-8"))
            assert "mocked" in data["reply"].lower()
            
        # 11th request must trigger the rate limit error response
        resp = client.post("/api/ai/explain-topic", json={"session_id": sess_id})
        assert resp.status_code == 200
        data = json.loads(resp.data.decode("utf-8"))
        assert "limit" in data["reply"].lower() or "rate" in data["reply"].lower() or "reach" in data["reply"].lower()
    finally:
        with app.app_context():
            get_ai_service()._provider = old_provider


def test_session_material_persistence_and_restoration(client):
    import io
    import os
    
    # Login as admin
    login_admin(client)
    
    with app.app_context():
        sess = Session.query.first()
        sess_id = sess.id
        sess_slug = sess.slug
        
    file_content = b"This is a persistent revision note data."
    data = {
        "title": "Updated Session with Note",
        "slug": sess_slug,
        "description": "Short desc",
        "content": "Full markdown content",
        "objectives": "* Obj 1",
        "expected_outcomes": "Outcomes",
        "learning_notes": "Learning Notes",
        "instructions": "Step 1: run code",
        "code_examples": "print('hello')",
        "resources": "http://example.com",
        "video_url": "http://youtube.com/embed/test",
        "notes_file": (io.BytesIO(file_content), "test_revision_notes.txt"),
        "duration": "45 min",
        "difficulty": "Beginner",
        "display_order": "1",
        "published": "on"
    }
    
    resp = client.post(f"/admin/session/{sess_id}/edit", data=data)
    assert resp.status_code == 302
    
    with app.app_context():
        sess_updated = db.session.get(Session, sess_id)
        assert sess_updated.notes_file_name == "test_revision_notes.txt"
        assert sess_updated.notes_file_data == file_content
        notes_path = sess_updated.notes_file_path
        
    filename = notes_path.split("/")[-1]
    filepath = UPLOADS_DIR / filename
    
    if filepath.exists():
        os.remove(filepath)
    assert not filepath.exists()
    
    # Log out admin
    client.get("/logout")
    
    register_and_login(client, reg_number="EB3/11111/11")
    
    resp_detail = client.get(f"/session/{sess_slug}")
    assert resp_detail.status_code == 200
    
    # Check physical file restored
    assert filepath.exists()
    with open(filepath, "rb") as f:
        assert f.read() == file_content
        
    # Check download works
    resp_dl = client.get(f"/session/{sess_id}/download")
    assert resp_dl.status_code == 200
    assert resp_dl.data == file_content
    
    # Close response to release Windows file lock
    resp_dl.close()
    # Cleanup physical file
    try:
        if filepath.exists():
            os.remove(filepath)
    except Exception:
        pass


def test_groq_provider_initialization():
    from ai_service import GroqProvider, get_ai_service
    import os
    
    # Test initializer
    provider = GroqProvider(api_key="mock-groq-key")
    assert provider._api_key == "mock-groq-key"
    assert provider._model_name == "llama-3.3-70b-versatile"
    
    # Test singleton fallback under env variables
    os.environ["GROQ_API_KEY"] = "mock-groq-key-env"
    os.environ.pop("GEMINI_API_KEY", None)
    
    # Re-initialize singleton instance
    import ai_service
    ai_service._ai_service_instance = None
    ai = get_ai_service()
    assert ai.is_configured
    assert isinstance(ai._provider, GroqProvider)
    assert ai._provider._api_key == "mock-groq-key-env"
    
    # Cleanup env
    os.environ.pop("GROQ_API_KEY", None)
    ai_service._ai_service_instance = None







