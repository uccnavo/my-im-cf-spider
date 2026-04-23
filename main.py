import os
import sys
import requests

# 接收从 Action 传过来的参数
keyword = sys.argv[1]
limit = int(sys.argv[2])
bot_token = sys.argv[3]
chat_id = sys.argv[4]

# Wallhaven API 搜索地址
#url = f"https://wallhaven.cc/api/v1/search?q={keyword}&categories=110&purity=100"
# categories=111 表示开启全部三类：常规、动漫、人物
# sorting=relevance 表示按相关性排序
url = f"https://wallhaven.cc/api/v1/search?q={keyword}&categories=111&purity=100&sorting=relevance"
os.makedirs("./images", exist_ok=True)

try:
    response = requests.get(url, timeout=30).json()
    images = response.get('data', [])[:limit]
    
    if not images:
        # 如果没搜到，给用户发个消息提醒
        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", 
                      data={'chat_id': chat_id, 'text': f"❌ 没找到关于 '{keyword}' 的图片"})
        sys.exit()

    for i, data in enumerate(images):
        img_url = data['path']
        img_data = requests.get(img_url, timeout=30).content
        file_path = f"./images/temp_{i}.jpg"
        
        with open(file_path, 'wb') as f:
            f.write(img_data)
        
        # --- 核心：将图片发回 Telegram ---
        with open(file_path, 'rb') as photo:
            requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendPhoto",
                data={'chat_id': chat_id, 'caption': f"✨ {keyword} ({i+1}/{len(images)})"},
                files={'photo': photo}
            )
        # ------------------------------
        print(f"已发送: {img_url}")

except Exception as e:
    print(f"出错: {e}")
