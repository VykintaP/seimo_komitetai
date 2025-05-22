import pytest
from pathlib import Path

this_dir = Path(__file__).parent
pytest.main([str(this_dir)])
