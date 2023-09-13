import unicodedata
import regex

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

   print(artists_parts)

   return artists_parts
