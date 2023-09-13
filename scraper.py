import requests
from bs4 import BeautifulSoup
import psycopg2
import json
import utils

clean_artists = utils.clean_artists

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

db_config = config_data["database"]

try:
    # Create a database connection
    connection = psycopg2.connect(
        dbname=db_config["name"],
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        port=db_config["port"]
    )

    # Create a cursor and execute SQL queries
    cursor = connection.cursor()

    drop_table_query = '''
    DROP TABLE IF EXISTS events'''

    cursor.execute(drop_table_query)
    connection.commit()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        header VARCHAR(255),
        date TEXT,
        artists TEXT[]
    );
    '''

    # Execute a simple query
    cursor.execute(create_table_query)
    connection.commit()

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)


webpage_response = requests.get('https://www.thewarehouseproject.com/')

content = webpage_response.content

soup = BeautifulSoup(content, 'html.parser')

counter = 0

for event in soup.select(".calendar_block_text"):
    # Prevent looping through mobile breakpoint divs to avoid duplicate entries
    if counter == 26:
        break

    header = event.find(class_='calendar_name').get_text().strip()
    date = event.find(class_='calendar_block_date').get_text()
    artists_div = event.find(class_='calendar_artists')
    artists = clean_artists(artists_div)

    insert_query = '''
    INSERT INTO events (header, date, artists)
    VALUES (%s, %s, %s);
    '''

    cursor.execute(insert_query, (header, date, artists))
    connection.commit()
    counter += 1

cursor.close()
connection.close()

