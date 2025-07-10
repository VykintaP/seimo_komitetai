import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def run_pipeline():
    pipeline_path = BASE_DIR / "scripts" / "run_pipeline.py"
    print(f"\n[PIPELINE] Startuoja pipeline iš {pipeline_path}")
    result = subprocess.run([sys.executable, str(pipeline_path)])
    if result.returncode != 0:
        print("[PIPELINE] Įvyko klaida pipeline metu.")
        sys.exit(1)
    print("[PIPELINE] Baigta sėkmingai.")

def run_dashboard():
    dashboard_path = BASE_DIR / "visualize" / "dashboard.py"
    print(f"\n[DASHBOARD] Startuoja Dash serveris iš {dashboard_path}")
    subprocess.run([sys.executable, str(dashboard_path)])

if __name__ == "__main__":
    run_pipeline()
    run_dashboard()
