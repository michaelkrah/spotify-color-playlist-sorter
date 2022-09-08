
from spotify_client import *
import os


def main():

    spotify_client = SpotifyClient(os.getenv("SPOTIFY_AUTHORIZATION_TOKEN"), "michaelkrah")
    print(os.getenv("SPOTIFY_AUTHORIZATION_TOKEN"))
    print(os.getenv("SPOTIFY_USER_ID"))

    tracks = spotify_client.get_playlist_tracks("1XW589QHysV2JIG2XzQORS?si=94e9e897d7334e93")

    result = spotify_client.populate_playlist("0vIocLhjLu02Z396pEYB4I?si=ac5fb86b49db4da6", tracks)
    print(result)


if __name__ == "__main__":
    main()
