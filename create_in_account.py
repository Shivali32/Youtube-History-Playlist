import json
import os
import re
import sys
from ytmusicapi import YTMusic
from ytmusicapi.auth.browser import setup_browser
from ytmusicapi.helpers import initialize_headers

PLAYLIST_FILE = os.path.join(os.path.dirname(__file__), "top_50_playlist.json")
AUTH_FILE = os.path.join(os.path.dirname(__file__), "browser.json")

def parse_curl_or_headers(text: str) -> dict:
    # Check if text is a curl command
    if "curl" in text and "-H" in text:
        headers = {}
        # Match -H 'Key: Value' or -H "Key: Value" or -H $'Key: Value'
        pattern = r"-H\s+[\$]?['\"]([^:]+):\s*([^'\"]+)['\"]"
        for key, val in re.findall(pattern, text):
            headers[key.strip().lower()] = val.strip()
        
        # Ensure base headers are present
        init_h = initialize_headers()
        init_h.update(headers)
        return init_h
    return None

def setup_from_input(auth_file: str):
    print("\n--- Paste What You Copied ---")
    print("Paste your 'Copy as cURL (bash)' or Request Headers here.")
    print("When done, press Enter, then press Ctrl+Z (or Ctrl+D) and press Enter:\n")
    
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
            
    raw = "\n".join(lines).strip()
    
    if not raw:
        print("Error: No input received.")
        return False
        
    # Try curl parsing first
    parsed_curl = parse_curl_or_headers(raw)
    if parsed_curl and "cookie" in parsed_curl:
        with open(auth_file, "w", encoding="utf-8") as f:
            json.dump(parsed_curl, f, indent=4)
        print(" Successfully parsed cURL headers and saved authentication!")
        return True
        
    # Fallback to standard ytmusicapi parser
    try:
        setup_browser(filepath=auth_file, headers_raw=raw)
        print(" Successfully parsed headers and saved authentication!")
        return True
    except Exception as e:
        print(f"❌ Could not parse headers: {e}")
        return False

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
        success = setup_from_input(AUTH_FILE)
        if not success:
            return

    try:
        yt = YTMusic(AUTH_FILE)
        title = "My Top & Recent Songs"
        desc = "Automatically generated from YouTube watch history (most played & recently played)"
        print(f"\n⏳ Creating playlist: '{title}' in your YouTube account...")
        playlist_id = yt.create_playlist(title=title, description=desc, privacy_status="PRIVATE", video_ids=video_ids)
        print(f"\n🎉 SUCCESS! Playlist created directly in your YouTube account!")
        print(f"👉 YouTube URL:       https://www.youtube.com/playlist?list={playlist_id}")
        print(f"👉 YouTube Music URL: https://music.youtube.com/playlist?list={playlist_id}")
    except Exception as e:
        print(f"\n❌ Failed to create playlist: {e}")
        if os.path.exists(AUTH_FILE):
            os.remove(AUTH_FILE)
            print("Removed invalid auth file. Please try again.")

if __name__ == "__main__":
    main()
