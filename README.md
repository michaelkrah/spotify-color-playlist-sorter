# spotify-color-playlist-sorter

A python program that will take an existing Spotify playlist in your account and sort it by the dominant color of the album image. 

# Installation:

Install dependencies listed in the setup.py file

```
pip install .
```

# Use:

In order to use this program you will need your spotify user id, a playlist id, and an authorization token.

Your user id will be the same as your username on the [account overview](https://www.spotify.com/us/account/overview/)

To get the playlist ID you want, in Spotify, share a playlist and copy the share link. The ID is in the link between `playlist/` and `?si=`.

To get the authorization token you will need to go to [here](https://developer.spotify.com/console/post-playlists/). You will need to select the scopes 'playlist-modify-public', and 'user-library-modify'. 

These can either be entered as environment variables or they can be entered in 'main.py'. Running the program will create a new spotify playlist.
