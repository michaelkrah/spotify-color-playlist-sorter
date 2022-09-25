import color_sorter_algo
from spotify_client import *
import os


def main():

    spotify_client = SpotifyClient(os.getenv("SPOTIFY_AUTHORIZATION_TOKEN"), os.getenv("USER_ID"))

    tracks = spotify_client.get_playlist_tracks(os.getenv("PLAYLIST_ID"))
    playlist = spotify_client.create_playlist("test stuff", "test")

    tracks_modified = color_sorter_algo.color_sort_hsv(tracks, 10, (255, 0, 0))

    result = spotify_client.populate_playlist(playlist.id, tracks_modified)
    print(result)


if __name__ == "__main__":
    main()
