from cs50 import SQL
# from helpers import cs50_query_to_df
import sqlite3
from pathlib import Path

# Project Root Directory
rootDir = Path(__file__).resolve().parent

# Database
DB = SQL("sqlite:///spc.db") 
CONN = sqlite3.connect("spc.db")

qryMeasurementSQL = Path(rootDir / "sql" / "qry_measurements.sql").read_text(encoding='utf-8')
insertNoteSQL = Path(rootDir / "sql" / "insert_note.sql").read_text(encoding="utf-8")