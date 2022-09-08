import json

import requests

from track import Track
from playlist import Playlist


class SpotifyClient:
    """Uses API"""

    def __init__(self, authorization_token, user_id):

        self.authorization_token = authorization_token
        self.user_id = user_id

    def get_playlist_tracks(self, playlist_id):

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) for track in response_json["tracks"]["items"]]
        return tracks

    def _place_get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.authorization_token}"
            }
        )
        return response

    def create_playlist(self, name):
        data = json.dumps({
            "name": name,
            "description": "Color tracks",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        print(response_json)

        playlist_id = response_json["id"]
        playlist = Playlist(name, playlist_id)
        return playlist

    def _place_post_api_request(self, url, data):
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.authorization_token}"
            }
        )
        return response


    def populate_playlist(self, playlist_id, tracks):
        track_uris = [track.create_spotify_uri() for track in tracks]
        request_body = json.dumps({
            "uris" : track_uris
            })
        endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        # response = self._place_post_api_request(url, data)
        # print(response)
        # response_json = response.status_code
        # print(response_json)
        # return response_json
        response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json",
                        "Authorization":f"Bearer {self.authorization_token}"})
        print(response.status_code)
        return response






