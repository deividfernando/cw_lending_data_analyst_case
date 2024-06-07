import sys
from pathlib import Path
project_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(project_dir))
from app import *
from app.models import *

def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()