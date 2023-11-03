# !pip install SQLAlchemy mysqlclient
import streamlit as st
from custom_modules import Extract
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
        extract = Extract()
        extract_button = st.form_submit_button("Extract Text From Image")
        if extract_button:
            extract.process_input(upload)

if __name__ == '__main__':
    run_main()