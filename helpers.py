import sys
import os

def find_data_file(filename) -> str:
    return os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "assets", filename)