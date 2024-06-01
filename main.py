import json

class Song:
    def __init__(self, name, artist):
        self.name = name
        self.artist = artist

    def __str__(self):
        return f"{self.artist} - {self.name}"

class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []
        self.current_index = 0

    def add_song(self, song):
        self.songs.append(song)

    def delete_song(self, song_name):
        self.songs = [song for song in self.songs if song.name != song_name]

    def clear(self):
        self.songs = []

    def show(self):
        for song in self.songs:
            print(str(song))

    def sort_by_title(self, reverse=False):
        self.songs.sort(key=self._get_song_name, reverse=reverse)

    def sort_by_artist(self, reverse=False):
        self.songs.sort(key=self._get_song_artist, reverse=reverse)

    def play_current_song(self):
        if self.songs:
            print(f"Playing: {self.songs[self.current_index]}")
        else:
            print("No songs in playlist.")

    def next_song(self):
        if self.songs:
            self.current_index = (self.current_index + 1) % len(self.songs)
            self.play_current_song()
        else:
            print("No songs in playlist.")

    def previous_song(self):
        if self.songs:
            self.current_index = (self.current_index - 1) % len(self.songs)
            self.play_current_song()
        else:
            print("No songs in playlist.")

    def _get_song_name(self, song):
        return song.name

    def _get_song_artist(self, song):
        return song.artist

class PlaylistManager:
    def __init__(self):
        self.playlists = self.load_playlists()

    def create_playlist(self, name):
        if name not in self.playlists:
            self.playlists[name] = Playlist(name)
            print(f"Playlist '{name}' created.")
        else:
            print("A playlist with this name already exists.")

    def select_playlist(self, name):
        if name in self.playlists:
            return self.playlists[name]
        else:
            print("Playlist not found.")
            return None


    def load_playlists(self):
        try:
            with open('playlists.json', 'r') as f:
                data = json.load(f)
                loaded_playlists = {}
                for name, songs in data.items():
                    playlist = Playlist(name)
                    for song in songs:
                        song_obj = Song(song['name'], song['artist'])
                        playlist.add_song(song_obj)
                    loaded_playlists[name] = playlist
                return loaded_playlists
        except FileNotFoundError:
            return {}

    def save_playlists(self):
        data = {}
        for name, playlist in self.playlists.items():
            data[name] = [{'name': song.name, 'artist': song.artist} for song in playlist.songs]
        with open('playlists.json', 'w') as f:
            json.dump(data, f)

    def sort_playlists(self, criteria, reverse=False):
        for playlist in self.playlists.values():
            if criteria == 'title':
                playlist.sort_by_title(reverse=reverse)
            elif criteria == 'artist':
                playlist.sort_by_artist(reverse=reverse)
        self.save_playlists()

def manage_playlist(playlist):
    while True:
        print(f"\nManaging Playlist: {playlist.name}")
        print("1. Add Song")
        print("2. Delete Song")
        print("3. Show Songs")
        print("4. Sort by Title")
        print("5. Sort by Artist")
        print("6. Play Current Song")
        print("7. Next Song")
        print("8. Previous Song")
        print("9. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            song_name = input("Enter song name: ")
            artist_name = input("Enter artist name: ")
            song = Song(song_name, artist_name)
            playlist.add_song(song)
        elif choice == '2':
            song_name = input("Enter the name of the song to delete: ")
            playlist.delete_song(song_name)
        elif choice == '3':
            playlist.show()
        elif choice == '4':
            playlist.sort_by_title()
            print("Playlist sorted by title.")
        elif choice == '5':
            playlist.sort_by_artist()
            print("Playlist sorted by artist.")
        elif choice == '6':
            playlist.play_current_song()
        elif choice == '7':
            playlist.next_song()
        elif choice == '8':
            playlist.previous_song()
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")

def main():
    manager = PlaylistManager()
    while True:
        print("\nMain Menu:")
        print("1. Create Playlist")
        print("2. Manage Playlists")
        print("3. Search Songs")
        print("4. Show All Playlists")
        print("5. Show Songs in a Playlist")
        print("6. Sort Playlists")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter playlist name: ")
            manager.create_playlist(name)
        elif choice == '2':
            name = input("Enter playlist name to manage: ")
            playlist = manager.select_playlist(name)
            if playlist:
                manage_playlist(playlist)
        elif choice == '3':
            song_name = input("Enter the name of the song to search: ")
            search_song(manager, song_name)
        elif choice == '4':
            print("Playlists loaded:")
            for playlist in manager.playlists.values():
                print(f"\nPlaylist: {playlist.name}")
        elif choice == '5':
            playlist_name = input("Enter the name of the playlist: ")
            playlist = manager.select_playlist(playlist_name)
            if playlist:
                print(f"Songs in playlist '{playlist_name}':")
                playlist.show()
        elif choice == '6':
            sort_playlists(manager)
        elif choice == '7':
            manager.save_playlists()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")

def sort_playlists(manager):
    print("\nSort Playlists by:")
    print("1. Title Ascending")
    print("2. Title Descending")
    print("3. Artist Ascending")
    print("4. Artist Descending")
    choice = input("Enter your choice: ")

    if choice == '1':
        manager.sort_playlists('title', reverse=False)
        print("Playlists sorted by title in ascending order.")
    elif choice == '2':
        manager.sort_playlists('title', reverse=True)
        print("Playlists sorted by title in descending order.")
    elif choice == '3':
        manager.sort_playlists('artist', reverse=False)
        print("Playlists sorted by artist in ascending order.")
    elif choice == '4':
        manager.sort_playlists('artist', reverse=True)
        print("Playlists sorted by artist in descending order.")
    else:
        print("Invalid choice. Please enter a number from 1 to 4.")

def search_song(manager, song_name):
    found = False
    for playlist in manager.playlists.values():
        for song in playlist.songs:
            if song.name == song_name:
                print(f"Found '{song_name}' in playlist '{playlist.name}' by {song.artist}")
                found = True
    if not found:
        print(f"Song '{song_name}' not found.")

if __name__ == "__main__":
    main()
