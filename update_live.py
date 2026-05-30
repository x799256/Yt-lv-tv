import urllib.request
import json
import re

CHANNELS = {
    "UC0GKelxahF1nHwKyGhfJVYA": "Menim_Tv"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for channel_id, channel_name in CHANNELS.items():
    try:
        # Birbaşa YouTube-un daxili pleyer datasına sorğu atırıq (Daha çətin bloklanır)
        url = f"https://www.youtube.com/embed/live_stream?channel={channel_id}"
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # HLS manifest linkini tapmaq üçün daha dəqiq axtarış modeli
        match = re.search(r'"hlsManifestUrl":"([^"]+)"', html)
        
        if match:
            m3u8_url = match.group(1).replace(r'\/', '/')
            with open(f"{channel_id}.m3u8", "w") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1,{channel_name}\n{m3u8_url}")
            print(f"{channel_name} üçün link uğurla yeniləndi.")
        else:
            raise Exception("Canlı yayın linki tapılmadı. Kanal yayımda olmaya bilər.")
            
    except Exception as e:
        print(f"XƏTA ({channel_name}): {str(e)}")
        # GitHub Action-ın qırmızı xəta verməməsi, sadəcə xəbərdarlıq etməsi üçün:
        exit(0)
