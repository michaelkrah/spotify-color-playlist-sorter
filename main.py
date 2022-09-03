
from spotify_client import *
import os


def main():

    spotify_client = SpotifyClient(os.getenv("SPOTIFY_AUTHORIZATION_TOKEN"), os.getenv("SPOTIFY_USER_ID"))

    playlist = spotify_client.create_playlist("Hello World")
    print(f"Playlist '{playlist.name}' was created")


if __name__ == "__main__":
    main()


