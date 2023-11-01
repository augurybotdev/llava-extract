import inspect
import sqlite3
import json
import json


class LicenseDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create table if it doesn't exist, with columns for image and json_data
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS LicenseData (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            middle_name TEXT,
            last_name TEXT,
            street_address TEXT,
            city TEXT,
            state TEXT,
            zip INTEGER,
            real_id BOOLEAN,
            organ_donor BOOLEAN,
            veteran_status BOOLEAN,
            DD INTEGER,
            customer_number TEXT,
            id_type TEXT,
            issue_date TEXT,
            expiration_date TEXT,
            date_of_birth TEXT,
            sex TEXT,
            eyes TEXT,
            class TEXT,
            height REAL,
            endorsements TEXT,
            restrictions TEXT,
            signature BOOLEAN,
            image BLOB,
            json_data TEXT
        )
        ''')

        conn.commit()
        conn.close()

    def insert_license_data(self, data, image_path=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Convert image to byte stream
        image_data = None
        if image_path:
            with open(image_path, 'rb') as f:
                image_data = f.read()

        # Serialize structured data to JSON string
        json_string = json.dumps(data)

        cursor.execute('''
        INSERT INTO LicenseData (
            first_name, middle_name, last_name, street_address, city, state, zip,
            real_id, organ_donor, veteran_status, DD, customer_number, id_type,
            issue_date, expiration_date, date_of_birth, sex, eyes, class, height,
            endorsements, restrictions, signature, image, json_data
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get("name", {}).get("first", {}).get("type"),
            data.get("name", {}).get("middle", {}).get("type"),
            data.get("name", {}).get("last", {}).get("type"),
            data.get("address", {}).get("street", {}).get("type"),
            data.get("address", {}).get("city", {}).get("type"),
            data.get("address", {}).get("state", {}).get("type"),
            data.get("address", {}).get("zip", {}).get("type"),
            data.get("real_id", {}).get("type"),
            data.get("organ_donor", {}).get("type"),
            data.get("veteran_status", {}).get("type"),
            data.get("DD", {}).get("type"),
            data.get("customer_number", {}).get("type"),
            data.get("id_type", {}).get("type"),
            data.get("issue_date", {}).get("type"),
            data.get("expiration_date", {}).get("type"),
            data.get("date_of_birth", {}).get("type"),
            data.get("sex", {}).get("type"),
            data.get("eyes", {}).get("type"),
            data.get("class", {}).get("type"),
            data.get("height", {}).get("type"),
            data.get("endorsements", {}).get("type"),
            data.get("restrictions", {}).get("type"),
            data.get("signature", {}).get("type"),
            image_data,
            json_string
        ))

        conn.commit()
        record_id = cursor.lastrowid
        conn.close()

        return record_id

    def retrieve_license_data(self, customer_number):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM LicenseData WHERE customer_number = ?
        ''', (customer_number,))

        record = cursor.fetchone()
        conn.close()

        if record:
            columns = [
                "id", "first_name", "middle_name", "last_name", "street_address", "city",
                "state", "zip", "real_id", "organ_donor", "veteran_status", "DD",
                "customer_number", "id_type", "issue_date", "expiration_date",
                "date_of_birth", "sex", "eyes", "class", "height", "endorsements",
                "restrictions", "signature", "image", "json_data"
            ]
            data = dict(zip(columns, record))

            # Deserialize the JSON data
            data["json_data"] = json.loads(data["json_data"])

            return data
        return None

    # Continue the definition of the LicenseDatabase class

    def update_license_data(self, customer_number, updated_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # If updating structured data, serialize it to a JSON string
        if "json_data" in updated_data:
            updated_data["json_data"] = json.dumps(updated_data["json_data"])

        columns = ", ".join([f"{key} = ?" for key in updated_data.keys()])
        values = list(updated_data.values()) + [customer_number]

        cursor.execute(f'''
        UPDATE LicenseData
        SET {columns}
        WHERE customer_number = ?
        ''', values)

        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()

        return updated


# Declare the path for the license_database module
license_database_module_path = "../data/storage"
license_data = LicenseDatabase

# Save the updated class definition to the .py file
with open(license_database_module_path, 'w') as f:
    f.write(inspect.getsource(license_data))
    f.write("\n")
    f.write(inspect.getsource(license_data.update_license_data))

license_database_module_path
