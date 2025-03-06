import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load API credentials from .env file
load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-modify-playback-state user-read-playback-state"
))

def get_active_device():
    """Returns the first active Spotify device or None."""
    devices = sp.devices()
    device_list = devices.get("devices", [])

    if not device_list:
        return None

    return device_list[0]["id"]  # Return the first active device ID

def open_spotify():
    """Opens Spotify app if not running (Windows/Linux)."""
    if os.name == "nt":  # Windows
        os.system("start spotify")
    else:  # Linux/Mac
        os.system("spotify &")

def play_music():
    """Ensure Spotify is running and start playback."""
    try:
        device_id = get_active_device()

        if not device_id:
            open_spotify()
            time.sleep(5)  # Wait for Spotify to fully start (Adjust time if needed)
            
            # Try getting the device again after opening Spotify
            device_id = get_active_device()
            if not device_id:
                return "Spotify opened, but no active device found. Please play a song manually."

        sp.start_playback(device_id=device_id)
        return "Playing music on Spotify."
    except Exception as e:
        return f"Error: {e}"

def pause_music():
    """Pause Spotify playback."""
    try:
        device_id = get_active_device()
        if not device_id:
            return "No active Spotify device found. Please open Spotify and play a song manually."

        sp.pause_playback(device_id=device_id)
        return "Music paused."
    except Exception as e:
        return f"Error: {e}"

def next_track():
    """Skip to the next song."""
    try:
        device_id = get_active_device()
        if not device_id:
            return "No active Spotify device found. Please open Spotify and play a song manually."

        sp.next_track(device_id=device_id)
        return "Skipped to the next track."
    except Exception as e:
        return f"Error: {e}"

def previous_track():
    """Go back to the previous song."""
    try:
        device_id = get_active_device()
        if not device_id:
            return "No active Spotify device found. Please open Spotify and play a song manually."

        sp.previous_track(device_id=device_id)
        return "Playing previous track."
    except Exception as e:
        return f"Error: {e}"

def play_specific_song(song_name):
    """Search and play a specific song."""
    try:
        device_id = get_active_device()
        if not device_id:
            open_spotify()
            time.sleep(5)  # Give time for Spotify to open
            device_id = get_active_device()
            if not device_id:
                return "Spotify opened, but no active device found. Please play a song manually."

        results = sp.search(q=song_name, limit=1)
        if results["tracks"]["items"]:
            track_uri = results["tracks"]["items"][0]["uri"]
            sp.start_playback(device_id=device_id, uris=[track_uri])
            return f"Playing {song_name} on Spotify."
        return "Song not found."
    except Exception as e:
        return f"Error: {e}"
