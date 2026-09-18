// --- 10-Second YouTube Playlist Creator ---
// 1. Open https://music.youtube.com (or https://www.youtube.com) in your browser where you are logged in.
// 2. Press F12 (or Right-Click -> Inspect) and click the "Console" tab.
// 3. Paste this code and press Enter!

(async () => {
  console.log("⏳ Creating playlist 'My Top & Recent Songs' in your account...");
  const videoIds = [
    "bP8ATWCvqzw", "kwjp52YYlwQ", "i6uTuA0ANMM", "YKcmMmJlKNk", "BrfRB6aTZlM",
    "nD1jhw6F-J4", "Ans8Y59cvds", "PwEvz2FLZ4I", "yhbVFtaBmso", "XF7TqbbAHrU",
    "JX409_Bq7m0", "fSS_R91Nimw", "8z8K-VMUIfo", "TVbI55pDdaI", "mYSOyDXJ6uM",
    "d2p2Lh9AbSY", "ycS5PagXvhQ", "zlt38OOqwDc", "zx_3gmcskZo", "t5OKlU0icRs",
    "zDtvoZAHVTY", "WnU0lH6C0EA", "2vKMY75kvjI", "HRcIDSawR18", "LpP4rtjACM8",
    "IgaB8n5Bj3U", "AB-I3vsUk6g", "iwoM7dJIK0w", "nP6AkuMMzaI", "B1Z1Ss6L_6M",
    "PFVwNbhVqkw", "k7_5e8R-d34", "AX7t8ZwroHQ", "FeR81vxTdBs", "zQGPxeFBPg8",
    "V3snyMEbG30", "X5THyXnyxv4", "M4bYA-xuZ6I", "kPtn26x8TZM", "qE3DfF66DNA",
    "NHQycTNjqpk", "x5fYTPvrz4g", "0mXL2UWT6Cg", "rTUjC5Kv0c8", "1a5nyrMtRsk",
    "fbdxYoFb64g", "r8O3URprq1M", "8iQU0ubwVdY", "HqUeSjsYLNU", "qTsAdjULqwg"
  ];
  
  const cookieMatch = document.cookie.match(/(?:^|;\s*)(?:SAPISID|__Secure-3PAPISID)=([^;]+)/);
  if (!cookieMatch) {
    alert("❌ Please make sure you are logged into your Google/YouTube account in this tab!");
    return;
  }
  
  const sapisid = cookieMatch[1];
  const origin = window.location.origin;
  const timestamp = Math.floor(Date.now() / 1000);
  const encoder = new TextEncoder();
  const hashBuffer = await crypto.subtle.digest("SHA-1", encoder.encode(`${timestamp} ${sapisid} ${origin}`));
  const hashHex = Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2, "0")).join("");
  const authHeader = `SAPISIDHASH ${timestamp}_${hashHex}`;
  
  const apiKey = window.ytcfg?.get("INNERTUBE_API_KEY");
  const context = window.ytcfg?.get("INNERTUBE_CONTEXT") || {
    client: { clientName: origin.includes("music") ? "WEB_REMIX" : "WEB", clientVersion: "1.20240918.01.00" }
  };
  
  try {
    const res = await fetch(`/youtubei/v1/playlist/create?key=${apiKey}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": authHeader,
        "X-Origin": origin
      },
      credentials: "include",
      body: JSON.stringify({
        context: context,
        title: "My Top & Recent Songs",
        description: "Auto-generated from YouTube watch history (most played & recently played)",
        privacyStatus: "PRIVATE",
        videoIds: videoIds
      })
    });
    
    const result = await res.json();
    if (result.playlistId) {
      console.log("✅ Playlist created! ID:", result.playlistId);
      alert("🎉 Success! Playlist created in your account. Redirecting now...");
      window.location.href = `/playlist?list=${result.playlistId}`;
    } else {
      console.error("Failed response:", result);
      alert("⚠️ Could not create playlist. See Console for details.");
    }
  } catch (err) {
    console.error("Error:", err);
    alert("Error: " + err.message);
  }
})();
