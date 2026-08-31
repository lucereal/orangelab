import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from makeconnection import set_preset

if __name__ == "__main__":
    set_preset("daylight")
