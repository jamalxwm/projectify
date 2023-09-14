from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from unidecode import unidecode

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

def search_for_artist(token, artist):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    
    # Transliterate the artist name to its closest English representation
    artist_en = unidecode(artist)
    
    query = f"?q={artist_en}&type=artist&limit=50"
    query_url = url + query
    result = get(query_url, headers=headers)
    data = json.loads(result.content)

    # Check that the return data is not empty
    if 'artists' in data:
        json_results = data['artists']['items']
        for result_item in json_results:
            # Transliterate the artist name in the response to compare with the input
            result_name_en = unidecode(result_item['name'])
            if result_name_en.lower() == artist_en.lower():
                return result_item['name']

    return None

def search_for_artists(token, artists):
    matched_artists = []
    unmatched_artists = set()

    for artist in artists:
        found_artist = search_for_artist(token, artist)
        if found_artist is not None:
            matched_artists.append(found_artist)
        elif found_artist is None and '&' in artist:
            match_parts = artist.split('&')
            for part in match_parts:
                found_part = search_for_artist(token, part.strip())
                if found_part is not None:
                    matched_artists.append(found_part)
                else:
                    unmatched_artists.add(part)
        else:
            unmatched_artists.add(artist)

    return matched_artists, unmatched_artists


token = get_token()

test_list = ['Ben Böhmer', 'Rebūke', 'Millie Watts', 'Melé', 'Adrián Mills', 'HØLEIGH']
matched, unmatched = search_for_artists(token, test_list)
print(matched, unmatched)






