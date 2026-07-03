# Gunicorn configuration file
# Automatically loaded by gunicorn when present in the working directory

timeout = 120          # Allow 120s per request (default 30s is too low for remote DB)
workers = 1            # Match Render's free-tier recommendation
