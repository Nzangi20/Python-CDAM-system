import os
from pathlib import Path

templates_dir = Path(r"c:\Users\Administrator\OneDrive\Desktop\Python system\frontend\templates")
for file in templates_dir.glob("*.html"):
    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f, start=1):
            if 'class="tab' in line or 'data-tab=' in line or 'tab-panel' in line:
                print(f"{file.name}:{idx} | {line.strip()}")
