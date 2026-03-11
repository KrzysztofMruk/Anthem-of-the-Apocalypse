import sqlite3
import sys


def create_connection(db_file): # Tworzenie połączenia z bazą danych
    conn = sqlite3.connect(db_file)
    return conn

