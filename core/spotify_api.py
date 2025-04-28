import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# Spotify scope
SCOPE = "user-read-playback-state user-modify-playback-state"

# Global Spotify client
sp = None

def ensure_spotify_client():
    """Ensure Spotify client is authenticated and refreshed."""
    global sp
    if sp is None:
        print("🔄 Initializing Spotify Client...")
        sp_oauth = SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope=SCOPE,
            cache_path=".spotify_cache",
            open_browser=True
        )

        token_info = sp_oauth.get_cached_token()
        if not token_info:
            token_info = sp_oauth.get_access_token(as_dict=True)

        sp = spotipy.Spotify(auth=token_info['access_token'])
        sp.token_info = token_info
        sp.sp_oauth = sp_oauth

    # Refresh token if needed
    if sp.token_info['expires_at'] - int(time.time()) < 60:
        print("🔄 Refreshing Spotify token...")
        sp.token_info = sp.sp_oauth.refresh_access_token(sp.token_info['refresh_token'])
        sp._auth = sp.token_info['access_token']

def get_spotify_client():
    """Returns a valid Spotify client."""
    ensure_spotify_client()
    return sp

def find_local_device(sp_client):
    """Find and return this PC's Spotify device."""
    devices = sp_client.devices()

    for device in devices['devices']:
        if device['type'] == 'Computer':
            print(f"✅ Found local device: {device['name']}")
            return device['id']

    return None

def play_music():
    """Play music on this PC device only."""
    try:
        sp_client = get_spotify_client()
        device_id = find_local_device(sp_client)

        if not device_id:
            return "❌ Spotify is not active on your PC. Please open Spotify app."

        try:
            sp_client.start_playback(device_id=device_id)
            return "🎵 Playing music on Spotify."
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 403:
                print("🔄 Spotify 403 Restriction: Trying to play a default track...")

                # Play a fallback default track
                fallback_track_uri = "spotify:track:3n3Ppam7vgaVa1iaRUc9Lp"  # Example: Eminem - Without Me
                sp_client.start_playback(device_id=device_id, uris=[fallback_track_uri])
                return "🎵 Playback started with default track."
            else:
                raise e

    except Exception as e:
        return f"Error: {e}"

def pause_music():
    try:
        sp_client = get_spotify_client()
        device_id = find_local_device(sp_client)

        if not device_id:
            return "❌ No PC Spotify device found."

        sp_client.pause_playback(device_id=device_id)
        return "⏸ Music paused."

    except Exception as e:
        return f"Error: {e}"

def next_track():
    try:
        sp_client = get_spotify_client()
        device_id = find_local_device(sp_client)

        if not device_id:
            return "❌ No PC Spotify device found."

        sp_client.next_track(device_id=device_id)
        return "⏭ Skipped to next track."

    except Exception as e:
        return f"Error: {e}"

def previous_track():
    try:
        sp_client = get_spotify_client()
        device_id = find_local_device(sp_client)

        if not device_id:
            return "❌ No PC Spotify device found."

        sp_client.previous_track(device_id=device_id)
        return "⏮ Playing previous track."

    except Exception as e:
        return f"Error: {e}"

def play_specific_song(song_name):
    try:
        sp_client = get_spotify_client()
        device_id = find_local_device(sp_client)

        if not device_id:
            return "❌ No PC Spotify device found."

        results = sp_client.search(q=song_name, limit=1)
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            sp_client.start_playback(device_id=device_id, uris=[track_uri])
            return f"🎶 Playing {song_name} on Spotify."

        return "❌ Song not found."

    except Exception as e:
        return f"Error: {e}"
