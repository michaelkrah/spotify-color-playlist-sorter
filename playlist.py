

class Playlist:
    """Playlist object, used to store name and id"""

    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __str__(self):
        return f"Playlist: {self.name}"
