# backend/finlife/utils/youtube_api.py
import requests
from django.conf import settings

def search_youtube_videos(keyword, max_results=10):
    """
    유튜브 API를 사용하여 영상 검색
    """
    # settings.py에 YOUTUBE_API_KEY를 추가하거나, 여기에 직접 문자열로 넣으세요
    # 예: API_KEY = "AIzaSy..." 
    API_KEY = getattr(settings, 'YOUTUBE_API_KEY', 'AIzaSyAJbfefA6rNy64Bm-qgJHe2vvvFh1sBZvE')
    
    url = 'https://www.googleapis.com/youtube/v3/search'
    
    params = {
        'part': 'snippet',
        'q': keyword,          # 검색어
        'key': API_KEY,
        'maxResults': max_results,
        'type': 'video',       # 비디오만 검색
        'order': 'relevance',  # 관련도순
        'regionCode': 'KR',    # 한국 지역
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'items' not in data:
            return []
            
        videos = []
        for item in data['items']:
            videos.append({
                'video_id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'channel_title': item['snippet']['channelTitle'],
                'publish_date': item['snippet']['publishedAt'][:10], # YYYY-MM-DD
            })
            
        return videos
        
    except Exception as e:
        print(f"Youtube API Error: {e}")
        return []