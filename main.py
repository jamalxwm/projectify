from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artists):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)

    for artist in artists:
        query = f"?q={artist}&type=artist&limit=50"
        query_url = url + query
        result = get(query_url, headers=headers)
        data = json.loads(result.content)

        if 'artists' in data:
            json_results = data['artists']['items']

            exact_match = False

            for result_item in json_results:
                if result_item['name'].lower() == artist.lower():
                    exact_match = True
                    found_artist = result_item['name']
                    print(f'Exact match found for: {found_artist}', result_item)
                    break

        if not exact_match:
            parts = artist.split(' & ')
            exact_match_part = False

            for part in parts:
                query_part = f"?q={part}&type=artist&limit=50"
                query_url = url + query_part
                result = get(query_url, headers=headers)
                json_results = json.loads(result.content)['artists']['items']

                for result_item in json_results:
                    if result_item['name'].lower() == part.lower():
                        print(f'Exact match found for: {part}', result_item)
                        exact_match_part = True
                        

                if exact_match_part:
                    continue



token = get_token()
test_list = ['Polo & Pan', 'Dan Shake & Sally C']
result = search_for_artist(token, test_list)
# artist_id = result['name']
# print(artist_id)

