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
    conn.commit()
    conn.close()

# Function to insert user data into database
def insert_data(client_name, residence, arm_length, shoulder_length):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (client_name, residence, arm_length, shoulder_length) VALUES (?, ?, ?)", (client_name, residence, arm_length, shoulder_length))
    conn.commit()
    conn.close()    

# Function to search for user data by name
def search_data(client_name):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name=?", (client_name))
    data = cursor.fetchall()
    conn.close()
    return data