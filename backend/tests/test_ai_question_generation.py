import sys
import json
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

# Ensure backend modules are importable
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app import app, db, User, Session, Exam, Question
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
        
        # Seed an admin user for testing
        from werkzeug.security import generate_password_hash
        admin = User(
            name="Admin User",
            email="admin@cdam.local",
            reg_number="EB3/ADMIN/26",
            password_hash=generate_password_hash("admin123"),
            auth_provider="local",
            is_admin=True
        )
        # Seed a student user
        student = User(
            name="Student User",
            email="student@cdam.local",
            reg_number="EB3/STUDENT/26",
            password_hash=generate_password_hash("student123"),
            auth_provider="local",
            is_admin=False
        )
        db.session.add(admin)
        db.session.add(student)
        db.session.commit()
        
    with app.test_client() as client:
        yield client

def login_admin(client):
    client.post(
        "/login",
        data={"identifier": "admin@cdam.local", "password": "admin123"},
        follow_redirects=True,
    )

def login_student(client):
    client.post(
        "/login",
        data={"identifier": "EB3/STUDENT/26", "password": "student123"},
        follow_redirects=True,
    )

def test_api_admin_ai_generate_questions_requires_admin(client):
    # Try as student -> should be denied
    login_student(client)
    res = client.post("/api/admin/ai/generate-questions", json={"topic": "pandas"})
    assert res.status_code == 302 # redirect because student is not admin

def test_api_admin_ai_generate_questions_success(client):
    login_admin(client)
    
    mock_questions = [
        {
            "questionText": "What is a DataFrame?",
            "questionType": "mcq",
            "options": ["A", "B", "C", "D"],
            "correctAnswer": "0",
            "marks": 1
        }
    ]
    
    with patch("app.get_ai_service") as mock_get_ai:
        mock_ai = MagicMock()
        mock_ai.is_configured = True
        mock_ai.generate_structured_questions.return_value = mock_questions
        mock_get_ai.return_value = mock_ai
        
        res = client.post(
            "/api/admin/ai/generate-questions",
            json={
                "topic": "DataFrame operations",
                "num_questions": 1,
                "question_types": ["mcq"],
                "difficulty": "Intermediate",
                "context_type": "exam"
            }
        )
        assert res.status_code == 200
        data = json.loads(res.data)
        assert "questions" in data
        assert len(data["questions"]) == 1
        assert data["questions"][0]["questionText"] == "What is a DataFrame?"
        
        mock_ai.generate_structured_questions.assert_called_once_with(
            topic="DataFrame operations",
            num_questions=1,
            question_types=["mcq"],
            difficulty="Intermediate",
            context_type="exam"
        )

def test_session_quiz_persistence(client):
    login_admin(client)
    
    quiz_data = [
        {
            "question": "Select True",
            "options": ["True", "False"],
            "correct": 0
        }
    ]
    
    # Test creation
    res_create = client.post(
        "/admin/session/new",
        data={
            "title": "New Session With Quiz",
            "description": "desc",
            "content": "content",
            "objectives": "objectives",
            "expected_outcomes": "outcomes",
            "learning_notes": "notes",
            "instructions": "instructions",
            "code_examples": "print()",
            "quiz_json": json.dumps(quiz_data),
            "duration": "30 min",
            "difficulty": "Beginner",
            "published": "on"
        },
        follow_redirects=True
    )
    assert res_create.status_code == 200
    
    with app.app_context():
        sess = Session.query.filter_by(title="New Session With Quiz").first()
        assert sess is not None
        assert json.loads(sess.quiz_json) == quiz_data
        sess_id = sess.id
        
    # Test editing
    res_edit = client.post(
        f"/admin/session/{sess_id}/edit",
        data={
            "title": "New Session With Quiz (Edited)",
            "description": "desc",
            "content": "content",
            "objectives": "objectives",
            "expected_outcomes": "outcomes",
            "learning_notes": "notes",
            "instructions": "instructions",
            "code_examples": "print()",
            "quiz_json": json.dumps([]),
            "duration": "30 min",
            "difficulty": "Beginner",
            "published": "on"
        },
        follow_redirects=True
    )
    assert res_edit.status_code == 200
    
    with app.app_context():
        sess = db.session.get(Session, sess_id)
        assert sess.title == "New Session With Quiz (Edited)"
        assert json.loads(sess.quiz_json) == []
