from dotenv import load_dotenv
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

#Put your Client ID and your Client secret inside a .env file 
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

redirect_uri = "http://127.0.0.1:8888/callback/"
scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope
))

# Set how many albums to fetch from saved Spotify albums (max 50)
fetched_data = sp.current_user_saved_albums(limit = 20)

#Fetch album names and album cover image URLs from Spotify

album_titles = []
album_urls = []

for item in fetched_data['items']:   
    album = item['album']

    album_names = album['name']
    album_titles.append(album_names + " - Album Cover")

    cover_url = album['images'][0]['url']
    album_urls.append(cover_url)

# Download Album cover URLs into .jpg files indside the "album_covers" folder with coresponding name 

folder_name = "album_covers"
os.makedirs(folder_name, exist_ok = True)

index = 0
for url in album_urls:
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(folder_name, f"{album_titles[index]}.jpg")
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {url}")
    
    index += 1