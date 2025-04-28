import pygame
import sys
import os
import math
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import time

# Load Spotify Credentials
load_dotenv()

SPOTIFY_SCOPE = "user-read-playback-state user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope=SPOTIFY_SCOPE
))

def get_current_track_info():
    """Fetch current playing song info."""
    try:
        playback = sp.current_playback()
        if playback and playback.get("is_playing"):
            track = playback["item"]
            name = track["name"]
            artist = track["artists"][0]["name"]
            return f"{name} - {artist}"
        else:
            return "Nothing Playing"
    except Exception as e:
        print(f"Error fetching Spotify track: {e}")
        return "Error"

def vinyl_player():
    """Launches a Pygame window with a rotating vinyl record."""
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Vinyl Player")
    clock = pygame.time.Clock()

    # Load assets
    bg_color = (10, 10, 10)
    vinyl_img = pygame.image.load("assets/vinyl.png")  # <-- create or download a simple vinyl.png
    vinyl_img = pygame.transform.scale(vinyl_img, (400, 400))

    font = pygame.font.SysFont('Arial', 28)
    angle = 0  # For rotation
    track_info = "Fetching Track..."

    last_update = time.time()

    running = True
    while running:
        screen.fill(bg_color)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        # Rotate the vinyl
        rotated_vinyl = pygame.transform.rotate(vinyl_img, angle)
        rect = rotated_vinyl.get_rect(center=(400, 350))
        screen.blit(rotated_vinyl, rect)

        # Update rotation
        angle = (angle + 0.5) % 360

        # Update track info every 5 seconds
        if time.time() - last_update > 5:
            track_info = get_current_track_info()
            last_update = time.time()

        # Draw track info
        text_surface = font.render(track_info, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(400, 700))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    vinyl_player()
