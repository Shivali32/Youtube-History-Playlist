# YouTube History Playlist Generator 🎵

Extracts your YouTube watch history from Google Takeout, filters out non-music content (podcasts, tutorials, ads), and ranks songs using an exponential time-decay algorithm (balancing frequency and recency).

## Features
- **Frequency + Recency Ranking**: Scores songs using a half-life time decay formula so songs you played recently rank higher, while all-time favorites still carry weight.
- **Smart Music Detection**: Filters out podcasts, news, ads, workouts, and other non-music videos.
- **1-Click Official YouTube Queue**: Generates a shareable URL to save the entire playlist directly into your YouTube library with one click.
- **Automated YouTube Account Creation**: Can directly create the playlist in your YouTube / YouTube Music library using \ytmusicapi\.

## Setup & Usage

1. **Install requirements**:
   \\\ash
   pip install -r requirements.txt
   \\\

2. **Download your watch history**:
   - Go to [Google Takeout](https://takeout.google.com).
   - Select **YouTube and YouTube Music** -> **History** -> **JSON** format.
   - Extract \watch-history.json\ into your Downloads folder (or project folder).

3. **Generate Playlist**:
   \\\ash
   python generate_playlist.py
   \\\

4. **Save to YouTube**:
   - Open \save_playlist.html\ in your browser and click **Open Playlist on YouTube**, then click **Save (+)** in YouTube.
   - Or run \python create_in_account.py\ for programmatic creation.
