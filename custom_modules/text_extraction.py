import sys
import replicate
from dotenv import load_dotenv
import os
from IPython.display import Image
import sqlite3
sys.path.append("..")
from custom_modules import LicenseDatabase
load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN

api_endpoint = "https://replicate.com/yorickvp/llava-13b/api?tab=python"
headers = {"Content-Type": "application/json"}
db = LicenseDatabase("../data/storage/license_database.db")

states_dir = "../data/images/states/"

class Extract:
    def __init__(self, input_path=None, database_path="../data/storage/license_database.db"):
        self.input_path = input_path
        self.database_path = database_path

    def extract_text(self, image_path):
        output = replicate.run(
            "yorickvp/llava-13b:2facb4a474a0462c15041b78b1ad70952ea46b5ec6ad29583c0b29dbd4249591",
            input={
                "image": open(image_path, "rb"),
                "prompt": """Use the text from the image to fill in the values for each category within the JSON Schemas.

                    If a category is not present, write the value as "None"
                    If a category is present but you cannot extract the value, write the value as "Unknown Value"

                    Remember to look for non-character symbols that can indicate organ donor or veteran status.
                    veteran status is often indicated by looking for the word 'Veteran' in an unexpected place,
                    as a unique style font, not designated with any label.
                    A circle that contains a star indicates that it is `'real_id': 'true'`.
                    Replace the "string", "boolean" and "integer" values with the extracted text.

                    ```
                    {\
                        "name": {\
                            "first": "string",\
                            "middle": "string",\
                            "last": "string"\
                                },\
                        "address": {\
                            "street": "string",\
                            "city": "string",\
                            "state": "string",\
                            "zip": "integer"\
                                },\
                        "real_id": "boolean",\
                        "organ_donor": "boolean",\
                        "veteran_status": "boolean",\
                        "DD": "integer",\
                        "customer_number": "string",\
                        "id_type": "string",\
                        "issue_date": "string",\
                        "expiration_date": "string",\
                        "date_of_birth": "string",\
                        "sex": "string",\
                        "eyes": "string",\
                        "class": "string",\
                        "height": "float",\
                        "endorsements": "string",\
                        "restrictions": "string",\
                        "signature": "boolean"\
                            }"""
                }
            )
        extracted_text = ""
        for item in output:
            extracted_text += item
            print(item, end="")
        return extracted_text
    
    def select_state_directory(self, state_name):
        for dir_name in os.listdir(states_dir):
            dir_path = os.path.join(states_dir, dir_name)
            if dir_name.lower().startswith(state_name.lower()):
                return dir_path

    def process_input(self, input_path):
        if os.path.isfile(input_path):
            if input_path.lower().endswith(('.png','.jpg','.jpeg')):
                extracted_data = self.extract_text(input_path)
                filename = os.path.basename(input_path)
                db.insert_license_data(filename, extracted_data, input_path)
            
        elif os.path.isdir(input_path):
            directory_path = input_path
            for filename in os.listdir(directory_path):
                if filename.endswith(".png") or filename.endswith("jpg") or filename.endswith("jpeg"):
                    file_path = os.path.join(directory_path, filename)
                    extracted_data = self.extract_text(file_path)
                    print(filename.upper(), " : ", extracted_data)
                    db.insert_license_data(filename, extracted_data, file_path)
        else:
            print(f"'{input_path}' is an INVALID INPUT. it is neither a path to a valid image file or a directory of valid images")

    def check_table_schema(self, db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(LicenseData)")
        schema = cursor.fetchall()
        conn.close()
        return schema
    
    def get_schema(self):
        schema = self.check_table_schema(self.database_path)
        return schema
    
    def get_path(self, state):
        path = self.select_state_directory(state)
        return path
    
    def execute_process(self, state):
        path = self.get_path(state)
        self.process_input(path)    
        print("UPDATED_DataBase:: ",db)