import re
import urllib.request
import os

# Bura istədiyiniz YouTube Kanal ID-lərini və onlara vermək istədiyiniz adları yazın
CHANNELS = {
    "UC0GKelxahF1nHwKyGhfJVYA": "Menim_Tv",
    "UC9FvGfvvcmXYxxxxx": "Trt_Haber" # Nümunə ikinci kanal
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for channel_id, channel_name in CHANNELS.items():
    try:
        url = f"https://www.youtube.com/channel/{channel_id}/live"
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # Səhifənin içindən m3u8 linkini axtarırıq
        match = re.search(r'"hlsManifestUrl":"([^"]+)"', html)
        
        if match:
            m3u8_url = match.group(1).replace(r'\/', '/')
            
            # Hər kanal üçün ayrıca .m3u8 faylı yaradırıq
            with open(f"{channel_id}.m3u8", "w") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1,{channel_name}\n{m3u8_url}")
            print(f"{channel_name} uğurla yeniləndi.")
        else:
            print(f"{channel_name} üçün canlı yayın linki tapılmadı (Kanal yayımda olmaya bilər).")
            
    except Exception as e:
        print(f"Xəta baş verdi ({channel_name}): {str(e)}")
