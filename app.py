import streamlit as st
import sqlite3
import pandas as pd

# Function to create a database table
def create_table():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        chest FLOAT,
                        shoulder FLOAT,
                        sleeve FLOAT,
                        neck FLOAT,
                        stomach FLOAT,
                        around_arm FLOAT,
                        shirt_length FLOAT,
                        cuff FLOAT,
                        hip FLOAT,
                        waist FLOAT,
                        thigh FLOAT,
                        knee FLOAT,
                        button FLOAT,
                        length FLOAT,
                        waist_to_knee FLOAT 
                   )
                   """)
    conn.commit()
    conn.close()

# Function to insert user data into database
def insert_data(name, chest, shoulder, sleeve, neck, stomach, around_arm, shirt_length, cuff, hip, waist, thigh, knee, button, length, waist_to_knee):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO records (name, chest, shoulder, sleeve, neck, stomach, around_arm, shirt_length, cuff, hip, waist, thigh, knee, button, length, waist_to_knee) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, chest, shoulder, sleeve, neck, stomach, around_arm, shirt_length, cuff, hip, waist, thigh, knee, button, length, waist_to_knee))
    conn.commit()
    conn.close()    

# Function to search for user data by name
def search_data(name):
    conn = sqlite3.connect("user_data.db")
    # cursor = conn.cursor()
    # cursor.execute("SELECT name, chest, shoulder, sleeve, neck, stomach, around_arm, shirt_length, cuff, hip, waist, thigh, knee, button, length, waist_to_knee FROM records WHERE name=?", (name,))
    # data = cursor.fetchall()
    query = f"SELECT * FROM records WHERE name LIKE '%{name}%'"
    record_df = pd.read_sql_query(query, conn)
    conn.close()
    return record_df

# Function to retrieve all user data
def all_users():
    conn = sqlite3.connect("user_data.db")
    records_df = pd.read_sql_query("SELECT * FROM records ORDER BY name DESC", conn)
    conn.close()
    return records_df

# Function to delete a record
def delete_a_record(id):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records WHERE id=?", (id,))
    conn.commit()
    conn.close()

# Function to delete all records
def delete_all_records():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records;",)
    conn.commit()
    conn.close()

# Confirm dialog
def confirm_dialog():
    confirm = st.button("Is the information correct?", ("Yes", "No"))
    return confirm == "Yes"
    

# Code Body
def main():
    with st.sidebar:
        # st.write("Welcome to 2DP Clothing")
        st.image('2dp.jpg')

    mode = st.sidebar.radio('What do you want to do?',['Input Data', 'Search Record','See all Records', 'Delete a Record','Delete all Records'])

    if mode == 'Input Data':
        st.header(":orange[Welcome to 2DP Clothing]")
        st.subheader("Client Data Entry")
        st.write("Enter user information below:")

        # Input fields 
        name = st.text_input("Name of Cleint")
        chest = st.number_input("Chest (inches)")
        shoulder = st.number_input("Shoulder (inches)")
        sleeve = st.number_input("Sleeve (inches)")
        neck = st.number_input("Neck (inches)")
        stomach = st.number_input("Stomach (inches)")
        around_arm = st.number_input("Around arm (inches)")
        shirt_length = st.number_input("Shirt length (inches)")
        cuff = st.number_input("Cuff (inches)")
        hip = st.number_input("Hip (inches)")
        waist = st.number_input("Waist (inches)")
        thigh = st.number_input("thigh (inches)")
        knee = st.number_input("Knee (inches)")
        button = st.number_input("Button (inches)")
        length = st.number_input("Trouser Length (inches)")
        waist_to_knee = st.number_input("Waist to knee (inches)")


        # Display records
        st.write("\nInformation you've entered. Please be sure it is right before you hit the submit button")
        st.subheader(":orange[Shirt / Top]")

        st.write(f"Name: {name}")
        st.write(f"Chest: {chest}")
        st.write(f"Shoulder: {shoulder}")
        st.write(f"Sleeve: {sleeve}")
        st.write(f"Neck: {neck}")
        st.write(f"Stomach: {stomach}")
        st.write(f"Around arm : {around_arm}")
        st.write(f"Shirt  length: {shirt_length}")
        st.write(f"Cuff : {cuff}")
        st.write(f"Hip: {hip}")

        st.subheader(":orange[Trouser]")
        st.write(f"Waist: {waist}")
        st.write(f"Thigh: {thigh}")
        st.write(f"Knee: {knee}")
        st.write(f"Button: {button}")
        st.write(f"Trouser length: {length}")
        st.write(f"Waist to knee: {waist_to_knee}")
        

        # Submit button to record user information
        if st.button("submit"):
            create_table()  # Create the table if it doesn't exist
            insert_data(name, chest, shoulder, sleeve, neck, stomach, around_arm, shirt_length, cuff, hip, waist, thigh, knee, button, length, waist_to_knee)
            st.success("User information recorded successfully!")

    # Search data by name
    if mode == 'Search Record':
        st.title(":orange[Record Search]")
        st.write("Enter a name below:")

        name = st.text_input("Search records by Name")
        if st.button("Search"):
            record_df = search_data(name)
            if not record_df.empty:
                st.dataframe(record_df)
            else:
                st.warning("Record not found")

    # See all records
    if mode == 'See all Records':
        st.title(":orange[Client Data Search]")
        st.header("Displaying all records")
        if st.button("See all records"):
            records = all_users()
            st.dataframe(records)

    # Delete a record
    if mode == 'Delete a Record':
        st.title(":orange[Delete a record]")
        st.header("Enter client id to delete that record \n If you are not sure, search record to capture user id")

        record_id = st.number_input("Enter client id to delete", min_value=1, step=1)
        st.warning("Are you sure you want to delete this record?")
        
        if st.button("Delete record"):
            delete_a_record(record_id)
            st.success("Record deleted successfully!")
            
    # Delete all records
    if mode == 'Delete all Records':
        st.title(":orange[Delete all records]")
        st.warning("Are you sure you want to delete all records?")
        
        if st.button("Delete all records"):
            delete_all_records()
            st.success("All Records deleted successfully!")
        

if __name__ == "__main__":
    main()