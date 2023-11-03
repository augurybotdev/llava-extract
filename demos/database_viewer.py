# !pip install SQLAlchemy mysqlclient
import os
import tempfile
import streamlit as st
from ext import Extract
import sqlite3
import pandas as pd

# Function to connect to the database and retrieve data

def run_main():
    st.title('Database Viewer for Llava Image to Structured JSON App')

    def get_data(table_name):
        conn = sqlite3.connect('../data/storage/license_database.db')
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    table_name = st.selectbox('Select Table', ['ImageData', 'LicenseData'])
    if st.button('Show Data'):
        df = get_data(table_name)
        st.write(df)
        
    
        
    form = st.form("a form")
    with form:
        upload = st.file_uploader("upload images to extract text", type=[".png", ".jpg", ".jpeg"])

        if upload is not None:
            temp_dir = tempfile.mkdtemp()
            file_name = upload.name
            temp_file_path = os.path.join(temp_dir, file_name)
            
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(upload.read())

        extract = Extract()
        extract_button = st.form_submit_button("Extract Text From Image")
        if extract_button:
            extract.process_input(temp_file_path)
            
            os.remove(temp_file_path)
            os.rmdir(temp_dir)


if __name__ == '__main__':
    run_main()