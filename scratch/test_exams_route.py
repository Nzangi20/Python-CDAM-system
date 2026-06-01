import traceback
from backend.app import app, User, db
from flask_login import login_user

print("Simulating GET /exams route request...")
with app.test_request_context():
    # Fetch a student user (e.g. id=3 or 4)
    user = db.session.get(User, 3) or db.session.get(User, 4) or db.session.get(User, 2)
    if not user:
        print("No student user found in database!")
    else:
        print(f"Logging in as user: {user.email}")
        
        # Build test client
        with app.test_client() as client:
            # Login the user in the session
            with client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)
                sess['_fresh'] = True
            
            try:
                response = client.get('/exams')
                print(f"Response code: {response.status_code}")
                if response.status_code == 500:
                    print("Error detected! Outputting response data:")
                    print(response.data.decode('utf-8', errors='ignore')[:2000])
                else:
                    print("Request was successful!")
            except Exception as e:
                print("Exception caught during request execution:")
                traceback.print_exc()

print("Simulation finished.")
