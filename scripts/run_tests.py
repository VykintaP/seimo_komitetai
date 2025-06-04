import pytest
from pathlib import Path

this_dir = Path(__file__).parent.parent / "tests"
result = pytest.main([str(this_dir)])

if result == 0:
    print("Visi testai sėkmingai praėjo.")
else:
    print(f"Rasta klaidų. Pytest grąžino kodą: {result}")
