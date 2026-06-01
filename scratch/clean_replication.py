import os
import shutil
from pathlib import Path

data_dir = Path(r"C:\xampp\mysql\data")
backup_dir = data_dir / "backup_replication"
backup_dir.mkdir(parents=True, exist_ok=True)

patterns = ["master", "multi-master", "relay-log", "mysql-relay-bin"]

print("Cleaning up corrupted replication files...")
for file in data_dir.glob("*"):
    if file.is_file():
        name = file.name.lower()
        if any(p in name for p in patterns):
            try:
                shutil.move(str(file), str(backup_dir / file.name))
                print(f"Moved: {file.name}")
            except Exception as e:
                print(f"Failed to move {file.name}: {e}")

print("Cleanup completed successfully!")
