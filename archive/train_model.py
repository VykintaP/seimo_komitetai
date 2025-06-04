import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from archive.train_logreg_model import train_model

if __name__ == "__main__":
    train_model()
