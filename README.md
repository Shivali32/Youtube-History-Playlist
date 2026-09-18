# YouTube History Playlist Generator 🎵

Extracts your YouTube watch history from Google Takeout, filters out non-music content (podcasts, tutorials, ads), and ranks songs using an exponential time-decay algorithm (balancing frequency and recency).

## Features
- **Frequency + Recency Ranking**: Scores songs using a half-life time decay formula so songs you played recently rank higher, while all-time favorites still carry weight.
- **Smart Music Detection**: Filters out podcasts, news, ads, workouts, and other non-music videos.
- **Instant Browser Creation**: A 10-second JavaScript snippet you can run in your browser console to create the playlist in your YouTube account instantly.
- **Automated CLI Tool**: Can directly create the playlist in your YouTube / YouTube Music library using `ytmusicapi`.

## Quick Start: Add Playlist to Your Account (10 Seconds)

1. Open **[music.youtube.com](https://music.youtube.com)** or **[youtube.com](https://www.youtube.com)** in your browser (where you are logged into your account).
2. Press **F12** (or right-click anywhere -> **Inspect**) and click the **Console** tab.
3. Open `browser_console_creator.js`, copy the code, paste it into the Console, and press **Enter**.
4. The playlist is created in your account immediately, and the browser redirects directly to it!

---

## Running Locally

1. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download your watch history**:
   - Go to [Google Takeout](https://takeout.google.com).
   - Select **YouTube and YouTube Music** -> **History** -> **JSON** format.
   - Extract `watch-history.json` into your Downloads folder (or project folder).

3. **Generate Playlist**:
   ```bash
   python generate_playlist.py
   ```

4. **Create in Account via Python**:
   ```bash
   python create_in_account.py
   ```
