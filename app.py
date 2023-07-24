import streamlit as st
import sqlite3
import pandas as pd

# Function to create a database table
def create_table():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS rec (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        chest FLOAT,
                        shoulder FLOAT,
                        sleeve_length FLOAT,
                        neck FLOAT,
                        stomach FLOAT,
                        around_arm FLOAT,
                        shirt_length FLOAT,
                        cuff FLOAT,
                        hip FLOAT,
                        waist FLOAT,
                        thigh FLOAT,
                        knee FLOAT,
                        bass FLOAT,
                        length FLOAT,
                        waist_to_knee FLOAT 
                   )
                   """)
    conn.commit()
    conn.close()

# Function to insert user data into database
def insert_data(name, chest, shoulder, sleeve_length, neck, stomach, around_arm, shirt_length, cuff, hip, waist, thigh, knee, bass, length, waist_to_knee):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rec (name, chest, shoulder, sleeve_length, neck, stomach, around_arm, shirt_length, cuff, hip, waist, thigh, knee, bass, length, waist_to_knee) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, chest, shoulder, sleeve_length, neck, stomach, around_arm, shirt_length, cuff, hip, waist, thigh, knee, bass, length, waist_to_knee))
    conn.commit()
    conn.close()    

# Function to search for user data by name
def search_data(name):
    conn = sqlite3.connect("user_data.db")
    # cursor = conn.cursor()
    # cursor.execute("SELECT name, chest, shoulder, sleeve, neck, stomach, around_arm, shirt_length, cuff, hip, waist, thigh, knee, bass, length, waist_to_knee FROM rec WHERE name=?", (name,))
    # data = cursor.fetchall()
    query = f"SELECT * FROM rec WHERE name LIKE '%{name}%'"
    record_df = pd.read_sql_query(query, conn)
    conn.close()
    return record_df

# Function to retrieve all user data
def all_users():
    conn = sqlite3.connect("user_data.db")
    rec_df = pd.read_sql_query("SELECT * FROM rec ORDER BY name DESC", conn)
    conn.close()
    return rec_df

# Function to delete a record
def delete_a_record(id):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rec WHERE id=?", (id,))
    conn.commit()
    conn.close()

# Function to delete all records
def delete_all_rec():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rec;",)
    conn.commit()
    conn.close()

# Function to run custom query
def run_custom_query(query):
    conn = sqlite3.connect("user_data.db")
    rec_df = pd.read_sql_query(query, conn)
    conn.close()
    return rec_df

# Confirm dialog
def confirm_dialog():
    confirm = st.button("Is the information correct?", ("Yes", "No"))
    return confirm == "Yes"
    

# Code Body
def main():
    with st.sidebar:
        # st.write("Welcome to 2DP Clothing")
        st.image('2dp.jpg')

    mode = st.sidebar.radio('What do you want to do?',['Input Data', 'Search Record','See all Records', 'Delete a Record', 'Run Custom Query'])

    if mode == 'Input Data':
        st.header(":orange[Welcome to 2DP Clothing]")
        st.subheader("Client Data Entry")
        st.write("Enter user information below:")

        # Input fields 
        name = st.text_input("Name of Cleint")
        chest = st.number_input("Chest (inches)")
        shoulder = st.number_input("Shoulder (inches)")
        sleeve_length = st.number_input("Sleeve Length (inches)")
        neck = st.number_input("Neck (inches)")
        stomach = st.number_input("Stomach (inches)")
        around_arm = st.number_input("Around arm (inches)")
        shirt_length = st.number_input("Shirt length (inches)")
        cuff = st.number_input("Cuff (inches)")
        hip = st.number_input("Hip (inches)")
        waist = st.number_input("Waist (inches)")
        thigh = st.number_input("thigh (inches)")
        knee = st.number_input("Knee (inches)")
        bass = st.number_input("bass (inches)")
        length = st.number_input("Trouser Length (inches)")
        waist_to_knee = st.number_input("Waist to knee (inches)")


        # Display Records
        st.write("\nInformation you've entered. Please be sure it is right before you hit the submit button")
        st.subheader(":orange[Shirt / Top]")

        st.write(f"Name: {name}")
        st.write(f"Chest: {round(chest,3)}")
        st.write(f"Shoulder: {round(shoulder,3)}")
        st.write(f"Sleeve Length: {round(sleeve_length,3)}")
        st.write(f"Neck: {round(neck,3)}")
        st.write(f"Stomach: {round(stomach,3)}")
        st.write(f"Around arm : {round(around_arm,3)}")
        st.write(f"Shirt  length: {round(shirt_length,3)}")
        st.write(f"Cuff : {round(cuff,3)}")
        st.write(f"Hip: {round(hip,3)}")

        st.subheader(":orange[Trouser]")
        st.write(f"Waist: {waist}")
        st.write(f"Thigh: {thigh}")
        st.write(f"Knee: {knee}")
        st.write(f"bass: {bass}")
        st.write(f"Trouser length: {length}")
        st.write(f"Waist to knee: {waist_to_knee}")
        

        # Submit button to record user information
        if st.button("submit"):
            create_table()  # Create the table if it doesn't exist
            insert_data(name, chest, shoulder, sleeve_length, neck, stomach, around_arm, shirt_length, cuff, hip, waist, thigh, knee, bass, length, waist_to_knee)
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
            rec = all_users()
            st.dataframe(rec)

    # Delete a record
    if mode == 'Delete a Record':
        st.title(":orange[Delete a record]")
        st.header("Enter client id to delete that record \n If you are not sure, search record to capture user id")

        record_id = st.number_input("Enter client id to delete", min_value=1, step=1)
        st.warning("Are you sure you want to delete this record?")
        
        if st.button("Delete record"):
            delete_a_record(record_id)
            st.success("Record deleted successfully!")
            
    # Delete all rec
    # if mode == 'Delete all rec':
        # st.title(":orange[Delete all rec]")
        # st.warning("Are you sure you want to delete all rec?")
        
        # if st.button("Delete all rec"):
        #     delete_all_rec()
        #     st.success("All rec deleted successfully!")

    # Run Custom query
    if mode == 'Run Custom Query':
        st.title(":orange[Run Custom Query]")
        st.warning("This is reserved for admin only!")
        query = st.text_area("Enter Custom SQL Query")
        
        if st.button("Run Query"):
            try:
                query_results = run_custom_query(query)
                st.dataframe(query_results)
            except Exception as e:
                st.error(f"Error executing the query: {e}")
            
        

if __name__ == "__main__":
    main()