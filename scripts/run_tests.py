"""Paleidžia pytest ir raportuoja testų rezultatus."""

from pathlib import Path

import pytest

# Testuojamo projekto testų direktorija
this_dir = Path(__file__).parent.parent / "tests"
result = pytest.main([str(this_dir)])

# Testai grąžina 0 jei visi praėjo sėkmingai
if result == 0:
    print("Visi testai sėkmingai praėjo.")
else:
    print(f"Rasta klaidų. Pytest grąžino kodą: {result}")
