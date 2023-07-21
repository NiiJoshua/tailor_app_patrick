import streamlit as st
import sqlite3

# Function to create a database table
def create_table():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_name TEXT,
                        residence TEXT,
                        arm_length INTEGER,
                        shoulder_length INTEGER
                   )
                   """)