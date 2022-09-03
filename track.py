class Track:
    """music"""

    def __init__(self, name, id, artist):

        self.name = name
        self.id = id
        self.artist = artist


    def create_spotify_uri(self):
        return f"spotify:track:{self.id}"

    def __str__(self):
        return f"{self.name} by {self.artist}"