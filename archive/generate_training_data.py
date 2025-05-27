import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from archive.training_data_generator import generate_training_data

if __name__ == "__main__":
    raw = Path("data/raw")
    out = Path("data/training_data.csv")
    df = generate_training_data(raw, out)
    print(f"[OK] Saved {len(df)} rows to {out}")
