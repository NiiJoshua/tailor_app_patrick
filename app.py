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
                        arm_length INTEGER,
                        shoulder_length INTEGER
                   )
                   """)
    conn.commit()
    conn.close()

# Function to insert user data into database
def insert_data(client_name, arm_length, shoulder_length):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (client_name, arm_length, shoulder_length) VALUES (?, ?, ?)", (client_name, arm_length, shoulder_length))
    conn.commit()
    conn.close()    

# Function to search for user data by name
def search_data(client_name):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT client_name, arm_length, shoulder_length FROM users WHERE client_name=?", (client_name,))
    data = cursor.fetchall()
    conn.close()
    return data

# Code Body
def main():
    with st.sidebar:
        st.write("Welcome to Patricks Tailor shop")

    mode = st.sidebar.radio('Choose an option',['Input Data', 'Search Record'])

    if mode == 'Input Data':
        st.header("Client Data Entry")
        st.write("Enter user information below:")

        # Input fields 
        client_name = st.text_input("Name of Cleint")
        arm_length = st.number_input("arm_length (in cm)")
        shoulder_length = st.number_input("shoulder_length (in cm)")

        # Submit button to record user information
        if st.button("Submit"):
            create_table()  # Create the table if it doesn't exist
            insert_data(client_name, arm_length, shoulder_length)
            st.success("User information recorded successfully!")

    # Search data by name
    if mode == 'Search Record':
        st.header("Client Data Search")
        st.write("Enter user information below:")

        search_name = st.text_input("Search User by Name")
        if st.button("Search"):
            data = search_data(search_name)
            if data:
                st.write("User Information:")
                for user in data:
                    st.write(f"Name: {user[0]}, arm_length: {user[1]}, shoulder_length: {user[2]}")
            else:
                st.write("No user found with the given name.")

if __name__ == "__main__":
    main()