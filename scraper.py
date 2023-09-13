import requests
from bs4 import BeautifulSoup
import psycopg2
import json
import unicodedata
import regex

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

events = []

for event in soup.select(".calendar_block_text"):
    header = event.find(class_='calendar_name').get_text().strip()
    date = event.find(class_='calendar_block_date').get_text()
    artists_div = event.find(class_='calendar_artists')
    artists = clean_artists(artists_div)
    events.append((header, date, artists))

insert_query = '''
INSERT INTO events (header, date, artists)
VALUES (%s, %s, %s);
'''

cursor.executemany(insert_query, events)
connection.commit()

cursor.close()
connection.close()

def clean_artists(artists_div):
   # Find all <em> tags in the HTML and remove them along with their contents
   for em_tag in artists_div.find_all('em'):
      em_tag.extract()
   
   # Replace <br> and <br/> tags with ' | '
   for br_tag in artists_div.find_all(['br', 'br/']):
      br_tag.insert_before(' ')
      br_tag.insert_after('|')
      
   # Normalize the text and split by '|'
   artists_text = unicodedata.normalize('NFKD', artists_div.get_text('|').strip().replace('\xa0', ' '))

   # Split the text by '|' and normalize each part
   pattern = r'\s*\|\s*|\b(?i)b2b\b|\.(?!(?<=\w\.)\w)|\b(?i)and\b|\b(?i)ft\b|\b(?i)vs\b'
   artists_parts = [part.strip() for part in regex.split(pattern, artists_text) if part.strip()]

   return artists_parts
