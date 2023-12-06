from os import path
import pytest
from tkinter import Tk
from music_player import MusicPlayer

def test_music_player_initialization():
    """ Test the initialization of the MusicPlayer class. """
    root = Tk()
    music_player = MusicPlayer(root)

    assert music_player.master == root
    assert music_player.playlist == []
    assert music_player.playlist_index == 0
    assert music_player.paused is False
    assert music_player.current_music is None

def test_play_music():
    """ Test the play_music method. """
    root = Tk()
    music_player = MusicPlayer(root)
    music_player.music_listbox.selection_set(0)
    music_player.open_folder()
    music_player.music_listbox.selection_set(0)
    music_player.play_pause_music()

    assert music_player.paused is False

def test_pause_music():
    """ Test the pause_music method. """
    root = Tk()
    music_player = MusicPlayer(root)
    music_player.music_listbox.selection_set(0)
    music_player.open_folder()
    music_player.music_listbox.selection_set(0)
    music_player.play_pause_music()
    music_player.play_pause_music()

    assert music_player.paused is True

def test_next_music():
    """ Test the next_music method. """
    root = Tk()
    music_player = MusicPlayer(root)
    # Open the first folder
    music_player.music_listbox.selection_set(0)
    music_player.open_folder()
    # Select the first song then skip to the next song
    music_player.music_listbox.selection_set(0)
    music_player.next_music()

    # The current music should be the second song in the listbox
    assert path.basename(music_player.current_music) == music_player.music_listbox.get(1)

def test_previous_music():
    """ Test the previous_music method. """
    root = Tk()
    music_player = MusicPlayer(root)
    # Open the first folder
    music_player.music_listbox.selection_set(0)
    music_player.open_folder()
    # Select the second song then skip to the previous song
    music_player.music_listbox.selection_set(1)
    music_player.previous_music()

    # The current music should be the first song in the listbox
    assert path.basename(music_player.current_music) == music_player.music_listbox.get(0)

def test_play_playlist():
    """ Test the play_playlist method. """
    root = Tk()
    music_player = MusicPlayer(root)
    # Open the first playlist
    music_player.playlist_listbox.selection_set(0)
    music_player.open_playlist()
    # Play the playlist
    music_player.play_pause_music()

    # The current music should be the first song in the listbox
    assert path.basename(music_player.current_music) == music_player.music_listbox.get(0)

if __name__ == "__main__":
    pytest.main(["-v", __file__])