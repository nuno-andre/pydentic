from pathlib import Path
import sys

basedir = Path(__file__).parents[1]
sys.path.insert(0, str(basedir / 'src'))
