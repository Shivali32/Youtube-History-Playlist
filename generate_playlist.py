import json
import math
import sys
from datetime import datetime, timezone
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

history_file = r"C:\Users\shiva\Downloads\takeout-20260917T180035Z-1-001\Takeout\YouTube and YouTube Music\history\watch-history.json"

with open(history_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Explicit exclusion list for non-music items
EXCLUDE_CHANNELS = [
    "raj shamani", "beerbiceps", "ranveer allahbadia", "samay raina", "tanmay bhat",
    "the lallantop", "barkha dutt", "mohak mangal", "dhruv rathee", "nitish rajput",
    "standup", "comedy", "vlog", "workout", "fitness", "gym", "tone and tighten",
    "veritasium", "mkbhd", "marques brownlee", "tech burner", "tedx", "kurzgesagt",
    "podcast", "talk show", "news", "recap", "explained", "monks & warriors",
    "motivational_guru", "alurkar music house" # storytelling/cassettes
]

EXCLUDE_TITLE_WORDS = [
    "podcast", "interview", "trailer", "teaser", "episode", "season", "highlights",
    "review", "full match", "gameplay", "walkthrough", "tutorial", "how to", "workout",
    "exercises", "q&a", "standup comedy", "vlog", "commercial", "ads", "reaction",
    "army operations", "बदली", "कथा", "भाऊ कदम"
]

MUSIC_CHANNELS = [
    "topic", "vevo", "music", "t-series", "tseries", "records", "saregama", 
    "coke studio", "sony", "yrf", "tips", "speed", "sound", "audio", "zee music",
    "the 9teen", "karan nawani", "anuv jain", "prateek kuhad", "darshan raval",
    "arijit", "badshah", "diljit", "shreya ghoshal", "sonu nigam", "atif aslam",
    "soumya m", "aditya a", "nesz", "dj ", "dj", "acoustic", "lofi", "speed records",
    "aaryasa official", "warner music"
]

MUSIC_TITLE_WORDS = [
    "song", "lyric", "lyrical", "audio", "official video", "music video", 
    "unplugged", "acoustic", "remix", "cover", "mashup", "ft.", "feat.", 
    "lo-fi", "lofi", "ost", "soundtrack", "album", "full video"
]

def is_music_video(title, channel, plays):
    # Music tracks are re-listened to; require at least 2 plays or known music channel
    t_low = title.lower()
    c_low = channel.lower()
    
    if any(ex in c_low for ex in EXCLUDE_CHANNELS):
        return False
    if any(ex in t_low for ex in EXCLUDE_TITLE_WORDS):
        return False
        
    is_channel_music = c_low.endswith("- topic") or "vevo" in c_low or any(mc in c_low for mc in MUSIC_CHANNELS)
    is_title_music = any(mt in t_low for mt in MUSIC_TITLE_WORDS)
    
    if is_channel_music or is_title_music:
        return True
        
    # If title has standard song separator and played multiple times
    if (" - " in title or " | " in title) and plays >= 3:
        return True
        
    return False

# Parse history
max_dt = datetime(1970, 1, 1, tzinfo=timezone.utc)
videos = defaultdict(lambda: {
    "title": "",
    "channel": "",
    "url": "",
    "plays": []
})

for item in data:
    if any("From Google Ads" in d.get("name", "") for d in item.get("details", [])):
        continue
        
    title = item.get("title", "")
    if not title.startswith("Watched "):
        continue
    title = title[len("Watched "):]
    
    url = item.get("titleUrl", "")
    if "v=" not in url:
        continue
    vid = url.split("v=")[1].split("&")[0]
    
    subs = item.get("subtitles", [])
    channel = subs[0].get("name", "") if subs else ""
    
    t_str = item.get("time")
    if not t_str:
        continue
    dt = datetime.fromisoformat(t_str.replace("Z", "+00:00"))
    if dt > max_dt:
        max_dt = dt
        
    v = videos[vid]
    v["title"] = title
    v["channel"] = channel
    v["url"] = f"https://www.youtube.com/watch?v={vid}"
    v["vid"] = vid
    v["plays"].append(dt)

T_HALF = 45.0  # 45 days half life

ranked = []
for vid, v in videos.items():
    if not is_music_video(v["title"], v["channel"], len(v["plays"])):
        continue
        
    # We require at least 2 plays to ensure it's a song the user actually listened to more than once
    if len(v["plays"]) < 2:
        continue
        
    score = 0.0
    for dt in v["plays"]:
        age_days = (max_dt - dt).total_seconds() / 86400.0
        decay = math.pow(2.0, -age_days / T_HALF)
        # Score = 0.15 base + 0.85 decay
        score += (0.15 + 0.85 * decay)
        
    recent_play = max(v["plays"])
    ranked.append({
        "vid": vid,
        "title": v["title"],
        "channel": v["channel"],
        "total_plays": len(v["plays"]),
        "score": score,
        "last_played": recent_play.strftime("%Y-%m-%d"),
        "url": v["url"]
    })

ranked.sort(key=lambda x: x["score"], reverse=True)

top_50 = ranked[:50]
video_ids = [s["vid"] for s in top_50]

# Build YouTube queue URL (up to 50 videos)
yt_queue_url = "https://www.youtube.com/watch_videos?video_ids=" + ",".join(video_ids)

print(f"Top 50 songs selected.")
print(f"YouTube 1-Click Save Link: {yt_queue_url}")

with open(r"C:\Users\shiva\.gemini\antigravity\brain\906dec70-711e-4918-89bf-6d9b1707262b\scratch\top_50_playlist.json", "w", encoding="utf-8") as out:
    json.dump({
        "youtube_queue_url": yt_queue_url,
        "songs": top_50
    }, out, indent=2, ensure_ascii=False)
