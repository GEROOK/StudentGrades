import sys
from pathlib import Path

# ensure that the 'src' directory is on sys.path so tests can import the application modules
root = Path(__file__).parent.parent
sys.path.insert(0, str(root / "src"))
