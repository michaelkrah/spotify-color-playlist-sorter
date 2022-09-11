import color_sorter_algo
from spotify_client import *
import os


def main():

    spotify_client = SpotifyClient(os.getenv("SPOTIFY_AUTHORIZATION_TOKEN"), os.getenv("USER_ID"))

    # playlist_id = spotify_client.get_playlist_id()
    tracks = spotify_client.get_playlist_tracks("5yDChUYpXU27y963ForYXY")

    tracks_modified = color_sorter_algo.color_sort_HSV(tracks)

    playlist = spotify_client.create_playlist("Hello 4")

    result = spotify_client.populate_playlist(playlist.id, tracks_modified)
    print(result)


if __name__ == "__main__":
    main()
