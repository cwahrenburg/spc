from cs50 import SQL
from helpers import cs50_query_to_df
import sqlite3

# Database
DB = SQL("sqlite:///spc.db") 
CONN = sqlite3.connect("spc.db")