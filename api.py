from flask_restful import Api, Resource
from flask import Flask, jsonify
from config import YANDEX_MUSIC_TOKEN
from yandex_music import Client
import os

app = Flask(__name__)
api = Api(app)
client = Client(YANDEX_MUSIC_TOKEN).init()


class MusicResourse(Resource):
    def get(self, user_track):
        search_result = client.search(user_track, type_='track', nocorrect=True)
        tracks = search_result.tracks.results
        track = tracks[0]
        filename = f"temp\{track.artists[0].name}-{track.title}.mp3"
        if os.path.exists(filename):
            os.remove(filename)
        track.download(filename)
        return jsonify({"response": "OK", "filename": filename})


class MusicAlbumResourse(Resource):
    def get(self, user_album):
        search_result = client.search(user_album, type_='album', nocorrect=True)
        albums = search_result.albums.results
        album = albums[0]
        info = f"{album.title}|{album.artists[0]['name']}"
        return jsonify({"response": "OK", "info": info})


api.add_resource(MusicResourse, '/api/v1/track/<string:user_track>')
api.add_resource(MusicAlbumResourse, '/api/v1/album/<string:user_album>')


if __name__ == '__main__':
    app.run(debug=True)




