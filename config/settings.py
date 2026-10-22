"""Project paths and environment configuration."""
import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")
OUTPUT_DIR = str(PROJECT_ROOT / "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
