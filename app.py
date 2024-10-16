# Using flask as backend
from flask import Flask, request, render_template
# Using Genius API 
import lyricsgenius as lg
import config
import youtube_search
from youtube_search import YoutubeSearch

app = Flask(__name__)

@app.route('/')
def index():
    # Rendering Home-Page
    return render_template('index.html')

@app.route('/', methods=['POST'])
def lys():
    # Getting Artist name as "artist"
    artist = request.form['artist']
    # Getting Song name as "song"
    song = request.form['song']
    # Using try and exception for printing the lyrics
    try:
        results = YoutubeSearch(artist + ' ' + song, max_results=1).to_dict()
        iframecode = results[0]["id"]
        # Using Genius via CLIENT ACCESS TOKEN
        genius = lg.Genius('config.api_key')
        # Searching song on Genius with artist and song name 
        txt = genius.search_song(song, artist)
        # If the song of the artist is found the lyrics is saved in "ly" variable
        ly = txt.lyrics
        ly = ly[ly.find("["):] if "[" in ly else ly
        # The lyrics is then send to "lyrics.html" page where the lyrics is shown
        return render_template('lyrics.html', artist=artist, song=song, lyrics=ly, iframecode=iframecode)
    except:
        # If no artist or no song is found then a exception is thrown 
        # And "error.html" is printed
        # It is also printed when the user forgets to give the name of artist or song
        return render_template('error.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=False) # or setting host to '0.0.0.0'