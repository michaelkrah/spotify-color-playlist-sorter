class Track:
    """Track object, stores a single spotify track along with its name, URI/id, artist, and image URL link"""

    def __init__(self, name, id, artist, image):

        self.name = name
        self.id = id
        self.artist = artist
        self.image = image

    def create_spotify_uri(self):
        return f"spotify:track:{self.id}"

    def __gt__(self, other):
        return True

    def __repr__(self):
        return f"{self.name} by {self.artist}"

    def __str__(self):
        return f"{self.name} by {self.artist}"