import pymysql
import yaml
import time
from datetime import datetime

def connect_to_db(config):
    return pymysql.connect(
        host=config['database']['host'],
        user=config['database']['user'],
        password=config['database']['password'],
        database=config['database']['name']
    )

def extract_data(cursor, table):
    cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()

def convert_to_vectors(data):
    vectors = [d for d in data]
    return vectors

def update_vectors(cursor, table, vectors):
    for i, vector in enumerate(vectors):
        cursor.execute(f"UPDATE {table} SET vector_column = '{vector}' WHERE id = {i}")

def main():
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

    connection = connect_to_db(config)
    cursor = connection.cursor()

    while True:
        now = datetime.now()
        for table_info in config['tables']:
            if table_info['name'] in config['sync_whitelist']:
                if table_info['interval'] == 'daily' and now.hour == 0:
                    data = extract_data(cursor, table_info['name'])
                    vectors = convert_to_vectors(data)
                    update_vectors(cursor, table_info['name'], vectors)
                elif table_info['interval'] == 'frequent' and now.minute % 15 == 0:
                    data = extract_data(cursor, table_info['name'])
                    vectors = convert_to_vectors(data)
                    update_vectors(cursor, table_info['name'], vectors)
        connection.commit()
        time.sleep(60)  # Sleep for a minute

if __name__ == "__main__":
    main()
