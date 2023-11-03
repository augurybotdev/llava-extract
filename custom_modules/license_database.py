import sqlite3
import json
import os


class LicenseDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create table if it doesn't exist, with columns for image name as PRIMARY KEY and JSON data
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ImageData (
            image_name TEXT PRIMARY KEY,
            json_data TEXT NOT NULL,
            image BLOB
        )
        ''')

        conn.commit()
        conn.close()
        
    def insert_license_data(self, image_name, data, image_path=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Convert image to byte stream
        image_data = None
        if image_path and os.path.isfile(image_path):
            with open(image_path, 'rb') as f:
                image_data = f.read()

        # Serialize structured data to JSON format
        json_data = json.dumps(data)

        # UPSERT operation: Update the entry if image_name already exists
        cursor.execute('''
        INSERT INTO ImageData (image_name, json_data, image)
        VALUES (?, ?, ?)
        ON CONFLICT(image_name) DO UPDATE SET
        json_data=excluded.json_data,
        image=excluded.image;
        ''', (image_name, json_data, image_data))

        conn.commit()
        conn.close()

    def retrieve_license_data(self, image_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT json_data, image FROM LicenseData WHERE image_name = ?
        ''', (image_name,))

        record = cursor.fetchone()
        conn.close()

        if record:
            data, image = record
            # Deserialize the JSON data
            data = json.loads(data)
            return {'data': data, 'image': image}
        return None

    def update_license_data(self, image_name, updated_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Serialize structured data to JSON string if not already a string
        if not isinstance(updated_data, str):
            updated_data = json.dumps(updated_data)

        cursor.execute('''
        UPDATE LicenseData
        SET json_data = ?
        WHERE image_name = ?
        ''', (updated_data, image_name))

        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()

        return updated

