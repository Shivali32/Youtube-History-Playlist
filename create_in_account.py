import json
import os
import sys
from ytmusicapi import YTMusic, setup

PLAYLIST_FILE = os.path.join(os.path.dirname(__file__), "top_50_playlist.json")
AUTH_FILE = os.path.join(os.path.dirname(__file__), "browser.json")

def main():
    if not os.path.exists(PLAYLIST_FILE):
        print("Error: top_50_playlist.json not found! Run generate_playlist.py first.")
        return

    with open(PLAYLIST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    songs = data["songs"]
    video_ids = [s["vid"] for s in songs]

    print(f"Ready to create playlist with {len(video_ids)} top & recent songs.")

    if not os.path.exists(AUTH_FILE):
        print("\n--- One-Time Account Authentication ---")
        print("1. In Chrome, go to https://music.youtube.com (make sure you're logged into your account).")
        print("2. Press F12 -> Go to the Network tab.")
        print("3. Click any request (e.g. 'browse' or 'player') -> Right-click -> Copy -> Copy request headers.")
        print("4. Paste below and press Enter, then press Ctrl+Z and Enter:\n")
        try:
            setup(filepath=AUTH_FILE)
        except Exception as e:
            print(f"Setup error: {e}")
            return

    try:
        yt = YTMusic(AUTH_FILE)
        title = "My Top & Recent Songs"
        desc = "Automatically generated from YouTube watch history (most played & recently played)"
        print(f"Creating playlist: '{title}' in your account...")
        playlist_id = yt.create_playlist(title=title, description=desc, privacy_status="PRIVATE", video_ids=video_ids)
        print(f"\nSUCCESS! Playlist created in your YouTube account!")
        print(f"YouTube URL:       https://www.youtube.com/playlist?list={playlist_id}")
        print(f"YouTube Music URL: https://music.youtube.com/playlist?list={playlist_id}")
    except Exception as e:
        print(f"Failed to create playlist: {e}")

if __name__ == "__main__":
    main()
