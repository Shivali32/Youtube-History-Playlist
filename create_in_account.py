import json
import os
import re
import subprocess
import sys
from ytmusicapi import YTMusic

PLAYLIST_FILE = os.path.join(os.path.dirname(__file__), "top_50_playlist.json")
AUTH_FILE = os.path.join(os.path.dirname(__file__), "browser.json")
HEADERS_FILE = os.path.join(os.path.dirname(__file__), "headers.txt")

def extract_headers(raw: str) -> dict:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://music.youtube.com",
        "x-goog-authuser": "0"
    }
    
    # Extract cookie
    m_cookie = re.search(r"-H\s+[\$]?['\"]cookie:\s*([^'\"]+)", raw, re.IGNORECASE)
    if not m_cookie:
        m_cookie = re.search(r"['\"]?cookie['\"]?\s*[:=]\s*['\"]([^'\"]+)", raw, re.IGNORECASE)
    if not m_cookie:
        m_cookie = re.search(r"(?:^|\n)cookie:\s*([^\r\n]+)", raw, re.IGNORECASE)
        
    if m_cookie:
        headers["cookie"] = m_cookie.group(1).strip()
    
    # Extract authorization
    m_auth = re.search(r"SAPISIDHASH\s+([^\s'\"]+)", raw)
    if m_auth:
        headers["authorization"] = f"SAPISIDHASH {m_auth.group(1).strip()}"
    else:
        m_auth2 = re.search(r"-H\s+[\$]?['\"]authorization:\s*([^'\"]+)", raw, re.IGNORECASE)
        if m_auth2:
            headers["authorization"] = m_auth2.group(1).strip()

    # Extract x-goog-authuser
    m_user = re.search(r"x-goog-authuser[^\d]*(\d+)", raw, re.IGNORECASE)
    if m_user:
        headers["x-goog-authuser"] = m_user.group(1)
        
    return headers

def get_auth():
    if os.path.exists(AUTH_FILE):
        return True

    # If headers.txt already exists with content
    if os.path.exists(HEADERS_FILE):
        with open(HEADERS_FILE, "r", encoding="utf-8") as f:
            raw = f.read()
    else:
        raw = ""

    if not raw.strip():
        print("\n" + "="*70)
        print("Opening Notepad so you don't have to struggle with terminal pasting!")
        print("1. In Notepad, simply paste (Ctrl+V) what you copied.")
        print("2. Save the file (Ctrl+S) and CLOSE Notepad.")
        print("="*70 + "\n")
        
        with open(HEADERS_FILE, "w", encoding="utf-8") as f:
            f.write("# Paste your cURL or Request Headers below this line, then Save (Ctrl+S) and Close Notepad:\n\n")
            
        # Open notepad and wait for the user to close it
        subprocess.run(["notepad.exe", HEADERS_FILE])
        
        with open(HEADERS_FILE, "r", encoding="utf-8") as f:
            raw = f.read()

    headers = extract_headers(raw)
    
    if "cookie" not in headers:
        print("❌ Error: Could not find 'cookie' in what was pasted into headers.txt.")
        print("Please make sure you copied 'Copy as cURL (bash)' or the request headers.")
        if os.path.exists(HEADERS_FILE):
            os.remove(HEADERS_FILE)
        return False

    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(headers, f, indent=4)
        
    print("✅ Successfully parsed authentication credentials!")
    return True

def main():
    if not os.path.exists(PLAYLIST_FILE):
        print("Error: top_50_playlist.json not found! Run generate_playlist.py first.")
        return

    with open(PLAYLIST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    songs = data["songs"]
    video_ids = [s["vid"] for s in songs]

    print(f"Found {len(video_ids)} top & recent songs ready for playlist.")

    if not get_auth():
        return

    try:
        yt = YTMusic(AUTH_FILE)
        title = "My Top & Recent Songs"
        desc = "Automatically generated from YouTube watch history (most played & recently played)"
        print(f"\n⏳ Creating playlist '{title}' in your YouTube account...")
        playlist_id = yt.create_playlist(title=title, description=desc, privacy_status="PRIVATE", video_ids=video_ids)
        print(f"\n🎉 SUCCESS! Playlist created directly in your YouTube account!")
        print(f"👉 YouTube Playlist URL:       https://www.youtube.com/playlist?list={playlist_id}")
        print(f"👉 YouTube Music Playlist URL: https://music.youtube.com/playlist?list={playlist_id}")
    except Exception as e:
        print(f"\n❌ Error creating playlist: {e}")
        if os.path.exists(AUTH_FILE):
            os.remove(AUTH_FILE)
            print("Resetting invalid auth file so you can try again.")

if __name__ == "__main__":
    main()
