import unicodedata
import regex
import re
from spotify_search import search_for_artists, get_token

token = get_token()

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
   pattern =  r'\s*\|\s*|\b(?i)b2b\b|\.(?!(?<=\w\.)\w|^I\.)|\b(?i)and\b|\b(?i)ft\b|\b(?i)vs\b|\s*\+\s*'
   artists_parts = [part.strip() for part in regex.split(pattern, artists_text) if part.strip()]
   
   removed_substrings = remove_substrings(artists_parts)
   replaced_strings = replace_strings(removed_substrings)
   removed_empty_strings = list(filter(remove_empty_strings, replaced_strings))                            
   split_and_extracted_strings = split_and_extract_artists(removed_empty_strings)
   matched_artists, unmatched_artists = search_for_artists(token, split_and_extracted_strings)
   print(matched_artists, unmatched_artists)

   return artists_parts

def remove_substrings(parts_list):
    
    pattern = r'( - Live|Dance Regular: |Born On Road: | In:session|\+ Many More| \[live\]| Presents Evolve|Special Guest: |a-z|Day & Night across five stages in|around Depot Mayfield|All Tickets £25|Register for instant access to the pre-sale via the link below|Pre-sale - 10am Wednesday 13th September|General sale - 10am Thursday 14th September| \(Reel-to- Reel Live\)| \(Daytimers\)|30 Years Of V Recordings - | - Recording Live From The Depot| - DJ Set)'
    removed_substrings = []
    # Remove unecessary substring from artist names and append to the removed substrings list
    for part in parts_list:
     removed_substrings.append(re.sub(pattern, '', part))
    
    return removed_substrings


def replace_strings(artist_list):
    replaced_strings = []

    i = 0
    while i < len(artist_list):
        if artist_list[i] == 'I' and i + 1 < len(artist_list) and (artist_list[i + 1] == 'Jordan' or artist_list[i + 1] == 'JORDAN' and i + 1 < len(artist_list)):
            replaced_strings.append('I. Jordan')
            i += 2
        elif artist_list[i] == 'Rossi':
            replaced_strings.append('Rossi.')
            i += 1
        elif artist_list[i] == 'XCLUB':
            replaced_strings.append('XCLUB.')
            i += 1
        elif artist_list[i] == 'blk':
            replaced_strings.append('blk.')
            i += 1
        elif artist_list[i] == 'Egg (Porij)':
            replaced_strings.append('Porij')
            i += 1
        elif re.match(r'.*TBA.*', artist_list[i]):
            replaced_strings.append('TBA')
            i += 1
        elif artist_list[i].startswith('ANOTR'):
            replaced_strings = ['ANOTR']
            break
        elif artist_list[i].startswith('Full line up to be revealed'):
            replaced_strings = ['TBA']
            break
        else:
            replaced_strings.append(artist_list[i])
            i += 1
    return replaced_strings

def split_and_extract_artists(input_list):
    result_list = []

    for item in input_list:
        # Split the item at '(' and ')'
        parts = item.split('(')
        
        # The first part is the main name
        main_name = parts[0].strip()
        result_list.append(main_name)
        
        # Extract elements inside parentheses and split them by comma and space
        if len(parts) > 1:
            elements = parts[1].replace(')', '').split(', ')
            result_list.extend(elements)
    
    return result_list

def remove_empty_strings(string):
    if len(string) <= 1:
        return None
    else:
        return string.strip()