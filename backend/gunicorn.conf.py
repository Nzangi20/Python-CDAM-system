import os
import multiprocessing

# Gunicorn configuration file for production concurrency

# Bind to port 8000 (or custom port via env)
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

# Concurrency configurations
# Standard formula: (2 * CPU_cores) + 1
default_workers = (multiprocessing.cpu_count() * 2) + 1
workers = int(os.environ.get("WEB_CONCURRENCY", str(default_workers)))

# Use threads to handle multiple concurrent I/O requests per worker
threads = int(os.environ.get("WEB_THREADS", "4"))
worker_class = "gthread"

# Request timeout limit (in seconds)
timeout = int(os.environ.get("WEB_TIMEOUT", "60"))

# Log configurations
accesslog = "-"
errorlog = "-"
loglevel = "info"
