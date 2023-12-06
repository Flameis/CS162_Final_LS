""" music_player.py
Luke Scovel
12/5/2023

Design:
Exceptions:
    class MusicPlayerError:
        init (Error_type)

    class NoMusicError (MusicPlayerError):

    class NoPlaylistError (MusicPlayerError):

    class PlayMusicError (MusicPlayerError):

    class PlaylistError (MusicPlayerError):

class MusicPlayer:
    def __init__
        construct buttons
        initialize variables
        initialize pygame mixer
        load music
        update time elapsed label

    def construct_buttons
        construct buttons

    def load_music
        get music files in folder
        add music files to listbox

    def load_folders
        get subdirectories in music folder
        add subdirectories to listbox

    def open_playlists
        get playlist files in music folder
        add playlist files to listbox

    def open_folder
        get selected folder
        if folder is selected, open it
        set folder path
        raise error if folder does not exist
        clear listbox
        load music

    def play_pause_music
        get selected music
        if music is selected, play it
        if music is in playlist, get path from playlist, otherwise get path from folder
        play music if it is not already playing, otherwise pause it

    def stop_music
        stop music

    def previous_music
        if current music is not first music in listbox, play previous music

    def next_music
        if current music is not last music in listbox, play next music

    def set_volume
        set volume of music
    
    def update_time_elapsed
        if music is playing, update time elapsed label
    
    def add_to_playlist
        if music is selected, add it to playlist
        join folder path and selected music to get full path

    def remove_from_playlist
        if music is selected, remove it from playlist
        remove music from playlist
        refresh playlist

    def open_playlist
        if playlist is selected, load it
        clear listbox
        add music files to listbox

    def save_playlist
        if playlist is selected, save it

    def add_new_playlist
        create new playlist
        clear selection and select new playlist

    def remove_playlist
        if playlist is selected, remove it
        remove playlist

    def display_metadata
        load audio file
        if audio file has metadata, display it

Inheritance Diagram:
+--------------------------+
|      MusicPlayerError    |
+--------------------------+
| - Malfunction_type       |
+--------------------------+
| + __init__(...)          |
+--------------------------+
              |-----------------------------|---> +--------------------------+---> +--------------------------+
+--------------------------+    +--------------------------+    |      PlayMusicError    |      |      PlaylistError      |
|      NoMusicError        |    |      NoPlaylistError     |    +--------------------------+    +--------------------------+ 
+--------------------------+    +--------------------------+              

This program is a GUI that allows the user to select music files and play them.
The user can also create playlists and add music to them.
 """

def install_dependencies():
    """ Installs the dependencies for the program. """
    check_call([executable, '-m', 'pip', 'install', 'pygame', 'eyed3'])

from subprocess import check_call
from sys import executable
from os import path, listdir, remove
import tkinter as tk

install_dependencies()
from pygame import mixer
import eyed3

class MusicPlayerError(Exception):
    """ A custom exception for the MusicPlayer class. """
    def __init__(self, Error_type):
        self.Malfunction_type = Error_type
        super().__init__(f"WARNING: {Error_type}")

class NoMusicError(MusicPlayerError):
    """ A custom exception for the MusicPlayer class. """
    def __init__(self):
        super().__init__("No music found.")

class NoPlaylistError(MusicPlayerError):
    """ A custom exception for the MusicPlayer class. """
    def __init__(self):
        super().__init__("No playlist found.")

class PlayMusicError(MusicPlayerError):
    """ A custom exception for the MusicPlayer class. """
    def __init__(self):
        super().__init__("Unable to play music, file may be missing.")

class PlaylistError(MusicPlayerError):
    """ A custom exception for the MusicPlayer class. """
    def __init__(self):
        super().__init__("Unable to load playlist.")

class MusicPlayer:
    def __init__(self, master):
        """ Initializes the GUI. """
        # Construct the buttons
        self.construct_buttons(master)

        # Initialize the variables
        self.playlist = []
        self.playlist_index = 0
        self.paused = False
        self.current_music = None
        self.music_dir = path.join(path.dirname(__file__), "music/")

        # Initialize Pygame mixer
        mixer.init()

        # Load the music
        self.load_folders()
        self.open_playlists()

        # Update the time elapsed label
        self.update_time_elapsed()

    def construct_buttons(self, master):
        """ Constructs the buttons for the GUI. """
        self.master = master
        self.master.title("Music Player")

        # Music listbox and buttons
        self.music_listbox = tk.Listbox(self.master, selectmode="single", selectbackground="black", width=50, height=15)
        self.music_listbox.grid(column=0, row=0, padx=5, pady=5, columnspan=2, sticky="ns")

        self.playlist_listbox = tk.Listbox(self.master, selectmode="single", selectbackground="black", width=50, height=15)
        self.playlist_listbox.grid(column=3, row=0, padx=5, pady=5, columnspan=2, sticky="ns")

        self.load_music_button = tk.Button(self.master, text="Refresh Music", command=self.load_folders)
        self.load_music_button.grid(column=0, row=1, sticky=tk.E, pady=5)

        self.open_folder_button = tk.Button(self.master, text="Open Folder", command=self.open_folder)
        self.open_folder_button.grid(column=1, row=1, sticky=tk.W, pady=5)

        # Music control buttons
        self.play_button = tk.Button(self.master, text="Play/Pause", command=self.play_pause_music)
        self.play_button.grid(column=0, row=2, sticky=tk.E, pady=5)

        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop_music)
        self.stop_button.grid(column=1, row=2, sticky=tk.W, pady=5)

        self.previous_button = tk.Button(self.master, text="Previous", command=self.previous_music)
        self.previous_button.grid(column=0, row=3, sticky=tk.E, pady=5)

        self.next_button = tk.Button(self.master, text="Next", command=self.next_music)
        self.next_button.grid(column=1, row=3, sticky=tk.W, pady=5)

        self.volume_scale = tk.Scale(self.master, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", length=200, command=self.set_volume)
        self.volume_scale.set(100)
        self.volume_scale.grid(column=0, row=4, columnspan=2)

        # Metadata and time elapsed labels
        self.metadata_label = tk.Label(self.master, text="")
        self.metadata_label.grid(column=0, row=5, columnspan=2, pady=5)

        self.time_elapsed_label = tk.Label(self.master, text="Time Elapsed: ")
        self.time_elapsed_label.grid(column=0, row=6, columnspan=2, pady=5)

        # Playlist buttons
        self.refresh_playlist_button = tk.Button(self.master, text="Refresh Playlist", command=self.open_playlists)
        self.refresh_playlist_button.grid(column=3, row=1, sticky=tk.E, pady=5)

        self.open_playlist_button = tk.Button(self.master, text="Open Playlist", command=self.open_playlist)
        self.open_playlist_button.grid(column=4, row=1, sticky=tk.W, pady=5)

        self.add_new_playlist_button = tk.Button(self.master, text="Add New Playlist", command=self.add_new_playlist)
        self.add_new_playlist_button.grid(column=3, row=2, sticky=tk.E, pady=5)

        self.remove_playlist_button = tk.Button(self.master, text="Remove Playlist", command=self.remove_playlist)
        self.remove_playlist_button.grid(column=4, row=2, sticky=tk.W, pady=5)

        self.add_to_playlist_button = tk.Button(self.master, text="Add to Playlist", command=self.add_to_playlist)
        self.add_to_playlist_button.grid(column=3, row=3, sticky=tk.E, pady=5)

        self.remove_from_playlist_button = tk.Button(self.master, text="Remove from Playlist", command=self.remove_from_playlist)
        self.remove_from_playlist_button.grid(column=4, row=3, sticky=tk.W, pady=5)

        self.save_playlist_button = tk.Button(self.master, text="Save Playlist", command=self.save_playlist)
        self.save_playlist_button.grid(column=3, row=4, columnspan=2, pady=5)

        self.current_playlist_label = tk.Label(self.master, text="Current Playlist: ")
        self.current_playlist_label.grid(column=3, row=5, columnspan=2, pady=5)

    def load_music(self):
        """ Loads the music files in the folder into the listbox. """
        # Clear the listbox
        self.music_listbox.delete(0, "end")

        # Get the music files in the folder
        music_files = [f for f in listdir(self.folder_path) if f.endswith(".mp3")]

        if not music_files:
            raise NoMusicError

        # Add the music files to the listbox
        for music_file in music_files:
            self.music_listbox.insert("end", music_file)

        # Select the first item in the listbox
        self.music_listbox.selection_set(0)
        

    def load_folders(self):
        """ Loads the subdirectories in the music folder into the listbox. """
        # Clear the listbox
        self.music_listbox.delete(0, "end")

        # Get the subdirectories in the music folder
        subdirectories = [d for d in listdir(self.music_dir) if path.isdir(path.join(self.music_dir, d))]

        if not subdirectories:
            raise NoMusicError

        # Add the subdirectories to the listbox
        for subdirectory in subdirectories:
            self.music_listbox.insert("end", subdirectory)

        # Select the first item in the listbox
        self.music_listbox.selection_set(0)

    def open_playlists(self):
        """ Loads the playlist files in the music folder into the listbox. """

        # Clear the listbox
        self.playlist_listbox.delete(0, "end")

        # Get the playlist files in the music folder
        playlist_files = [f for f in listdir(self.music_dir) if f.endswith(".txt")]

        # Add the playlist files to the listbox
        for playlist_file in playlist_files:
            self.playlist_listbox.insert("end", playlist_file)

        # Select the first item in the listbox
        self.playlist_listbox.selection_set(0)

    def open_folder(self):
        """ Opens the selected folder. """
        # Get the selected folder
        selected_index = self.music_listbox.curselection()

        # Turn off playlist mode
        self.playlist_mode = False

        # If a folder is selected, open it
        if selected_index:
            selected_folder = self.music_listbox.get(selected_index)
            # If the selected folder is not a music file, open it
            if not selected_folder.endswith(".mp3"):
                # Set the folder path
                self.folder_path = path.join(self.music_dir, selected_folder)

                # Raise an error if the folder does not exist
                if not path.exists(self.folder_path):
                    raise NoMusicError
                
                # Clear the listbox
                self.music_listbox.delete(0, "end")
                # Load the music
                self.load_music()

    def play_pause_music(self):
        """ Plays or pauses the music. """
        try:
            # Get the selected music
            selected_index = self.music_listbox.curselection()

            # If a music is selected, play it
            if selected_index:
                selected_music = self.music_listbox.get(selected_index)

                # If the music is in a playlist, get the path from the playlist, otherwise get the path from the folder
                if not self.playlist_mode:
                    music_path = path.join(self.folder_path, selected_music)
                else:
                    music_path = self.playlist[selected_index[0]]

                # Play the music if it is not already playing, otherwise pause it
                if self.current_music != music_path:
                    mixer.music.load(music_path)
                    mixer.music.play()
                    self.current_music = music_path
                    self.display_metadata(music_path)
                    self.paused = False
                elif self.paused:
                    mixer.music.unpause()
                    self.paused = False
                else:
                    mixer.music.pause()
                    self.paused = True

            # Update the time elapsed label
            self.update_time_elapsed()
        except:
            raise PlayMusicError

    def stop_music(self):
        """ Stops the music. """
        mixer.music.stop()
        self.paused = False

    def previous_music(self):
        """ Plays the previous music in the list box. """
        # If the current music is not the first music in the list box, play the previous music
        self.music_listbox.selection_set(first=self.music_listbox.curselection()[0]-1)
        if len(self.music_listbox.curselection()) != 1:
            self.music_listbox.selection_clear(first=self.music_listbox.curselection()[1])
        self.play_pause_music()

    def next_music(self):
        """ Plays the next music in the list box. """
        # If the current music is not the last music in the list box, play the next music
        self.music_listbox.selection_set(first=self.music_listbox.curselection()[0]+1)
        if len(self.music_listbox.curselection()) != 1:
            self.music_listbox.selection_clear(first=self.music_listbox.curselection()[0])
        self.play_pause_music()

    def set_volume(self, event):
        """ Sets the volume of the music. """
        mixer.music.set_volume(self.volume_scale.get()/100)

    def update_time_elapsed(self):
        """ Updates the time elapsed label. """
        # If the music is playing, update the time elapsed label
        if mixer.music.get_busy():
            current_time = mixer.music.get_pos() / 1000
            minutes, seconds = divmod(int(current_time), 60)
            self.time_elapsed_label.config(text="Time Elapsed: {:02d}:{:02d}".format(minutes, seconds))
            self.master.after(1000, self.update_time_elapsed)

    def add_to_playlist(self):
        """ Adds the selected music to the playlist. """
        # Get the selected music
        selected_index = self.music_listbox.curselection()

        # If a music is selected, add it to the playlist
        if selected_index:
            selected_music = self.music_listbox.get(selected_index)
            # Join the folder path and the selected music to get the full path
            music_path = path.join(self.folder_path, selected_music)
            self.playlist.append(music_path)

    def remove_from_playlist(self):
        """ Removes the selected music from the playlist. """
        # Get the selected music
        selected_index = self.music_listbox.curselection()

        # If a music is selected, remove it from the playlist
        if selected_index and self.playlist_mode:
            selected_music = self.music_listbox.get(selected_index)
            
            # Remove the music from the playlist
            for music in self.playlist:
                if selected_music in path.basename(music):
                    self.playlist.remove(music)
                    break

            # Refresh the playlist
            self.save_playlist()
            self.music_listbox.delete(selected_index)

    def open_playlist(self):
        """ Loads the selected playlist. """
        # Get the selected playlist
        selected_index = self.playlist_listbox.curselection()

        # Turn on playlist mode
        self.playlist_mode = True

        # If a playlist is selected, load it
        if selected_index:
            self.selected_playlist = self.playlist_listbox.get(selected_index)
            playlist_path = path.join(self.music_dir, self.selected_playlist)
            with open(playlist_path, "r") as playlist_file:
                self.playlist = playlist_file.read().splitlines()

            if not path.exists(playlist_path):
                raise PlaylistError(f"Playlist file not found: {playlist_path}")

            #Clear the listbox
            self.music_listbox.delete(0, "end")

            # Add the music files to the listbox
            for music in self.playlist:
                self.music_listbox.insert("end", path.basename(music))

            # Select the first item in the listbox
            self.music_listbox.selection_set(0)

            # Update the current playlist label
            self.current_playlist_label.config(text=f"Current Playlist: {self.selected_playlist}")

    def save_playlist(self):
        """ Saves the current playlist. """
        # Get the selected playlist
        if self.selected_playlist:
            playlist_path = path.join(self.music_dir, self.selected_playlist)
            # Save the playlist
            with open(playlist_path, "w") as playlist_file:
                for music in self.playlist:
                    playlist_file.write(music + "\n")

    def add_new_playlist(self):
        """ Adds a new playlist. """
        # Create a new playlist
        self.playlist_listbox.insert("end", f"Playlist {self.playlist_listbox.size()+1}.txt")

        # Clear the selection and select the new playlist
        self.playlist_listbox.selection_clear(0, "end")
        self.playlist_listbox.selection_set("end")
        self.playlist = []

        playlist_path = path.join(self.music_dir, f"Playlist {self.playlist_listbox.size()}.txt")

        with open(playlist_path, "w") as playlist_file:
            pass

        self.open_playlist()

    def remove_playlist(self):
        """ Removes the selected playlist. """
        try:
            # Get the selected playlist
            selected_index = self.playlist_listbox.curselection()

            # If a playlist is selected, remove it
            if selected_index:
                selected_playlist = self.playlist_listbox.get(selected_index)
                playlist_path = path.join(self.music_dir, selected_playlist)
                # Remove the playlist
                if path.exists(playlist_path):
                    self.playlist_listbox.delete(selected_index)
                    self.selected_playlist = None
                    self.playlist = []
                    self.current_playlist_label.config(text="Current Playlist: ")

                    remove(playlist_path)
        except FileNotFoundError:
            raise PlaylistError

    def display_metadata(self, file_path):
        """ Displays the metadata of the selected music. """
        # Load the audio file
        audio_file = eyed3.load(file_path)

        # If the audio file has metadata, display it
        if audio_file.tag:
            title = audio_file.tag.title
            artist = audio_file.tag.artist
            album = audio_file.tag.album
            duration = audio_file.info.time_secs

            # Display the metadata
            metadata_text = f"Title: {title}\nArtist: {artist}\nAlbum: {album}\nDuration: {int(duration)} seconds"
            self.metadata_label.config(text=metadata_text)

if __name__ == "__main__":
    root = tk.Tk()
    music_player = MusicPlayer(root)
    root.mainloop()