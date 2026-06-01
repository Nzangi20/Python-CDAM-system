import os
import shutil
import time
from pathlib import Path

# 1. Paths
mysql_data = Path(r"C:\xampp\mysql\data")
mysql_backup = Path(r"C:\xampp\mysql\backup")

# 2. Stop mysqld
print("Stopping any active mysqld processes...")
os.system("taskkill /f /im mysqld.exe")
time.sleep(2)

# 3. Backup and clean corrupted mysql folder
target_mysql = mysql_data / "mysql"
old_corrupted = mysql_data / "mysql_corrupted_old"

if target_mysql.exists():
    if old_corrupted.exists():
        shutil.rmtree(old_corrupted)
    target_mysql.rename(old_corrupted)
    print("Corrupted 'mysql' system folder moved to 'mysql_corrupted_old'.")

# 4. Copy clean mysql folder from backup
shutil.copytree(mysql_backup / "mysql", target_mysql)
print("Copied clean 'mysql' system folder from backup.")

# 5. Clean up Aria transaction log files (they will regenerate automatically on startup)
aria_files = ["aria_log.00000001", "aria_log_control"]
for file_name in aria_files:
    file_path = mysql_data / file_name
    if file_path.exists():
        try:
            file_path.unlink()
            print(f"Removed old Aria log file: {file_name}")
        except Exception as e:
            print(f"Could not remove {file_name}: {e}")

print("System database restoration completed successfully!")
