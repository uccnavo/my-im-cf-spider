import os
import sys
import requests

# 1. 接收参数：关键词和数量
# sys.argv[1] 是关键词, sys.argv[2] 是数量
try:
    keyword = sys.argv[1]
    limit = int(sys.argv[2])
except (IndexError, ValueError):
    print("参数错误，使用默认值")
    keyword = "nature"
    limit = 5

# 2. Wallhaven API 地址 (筛选 General 和 Anime 类别)
url = f"https://wallhaven.cc/api/v1/search?q={keyword}&categories=110&purity=100"

# 3. 创建临时文件夹
os.makedirs("./images", exist_ok=True)

print(f"正在准备抓取关键词: {keyword}, 数量: {limit}")

try:
    response = requests.get(url, timeout=30).json()
    images = response.get('data', [])[:limit]
    
    if not images:
        print("未找到相关图片")
    
    for i, data in enumerate(images):
        img_url = data['path']
        try:
            img_data = requests.get(img_url, timeout=30).content
            # 保存文件，命名格式：关键词_序号.jpg
            file_path = f"./images/{keyword}_{i+1}.jpg"
            with open(file_path, 'wb') as f:
                f.write(img_data)
            print(f"成功保存第 {i+1} 张: {img_url}")
        except Exception as e:
            print(f"下载单张图片失败: {e}")
            
except Exception as e:
    print(f"爬虫运行出错: {e}")
