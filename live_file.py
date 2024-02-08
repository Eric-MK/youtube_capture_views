import pandas as pd
from googleapiclient.discovery import build
import time  # Import the time module

def get_youtube_data(api_key, *video_ids):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    all_data = []
    
    for video_id in video_ids:
        # Get video details
        video_response = youtube.videos().list(part='snippet,liveStreamingDetails', id=video_id).execute()
        
        # Check if 'items' is present in the response and not empty
        if 'items' in video_response and video_response['items']:
            video_details = video_response['items'][0]['snippet']
            live_details = video_response['items'][0].get('liveStreamingDetails', {})

            data = {
                'Title': video_details.get('title', ''),
                'Video URL': f'https://www.youtube.com/watch?v={video_id}',
                'Views': live_details.get('concurrentViewers', 'Live Stream'),
                'Length (seconds)': live_details.get('actualStartTime', ''),
                'Author': video_details.get('channelTitle', ''),
                'Published Date': video_details.get('publishedAt', ''),
                'Description': video_details.get('description', ''),
                'Thumbnail URL': video_details['thumbnails']['default']['url'] if 'thumbnails' in video_details else '',
            }

            all_data.append(data)
        else:
            print(f"Error: No video details found for video ID {video_id}")
            
    return all_data

def main():
    api_key = ''
    
    ktn_home = "0HL14aKXsCY"
    ktn_news = "0HL14aKXsCY"
    citizen_news = "Bqv4O9x6a9U"
    
    video_ids = [citizen_news, ktn_news , ktn_home]
    
    while True:  # Loop indefinitely
        videos_data = get_youtube_data(api_key, *video_ids)
        
        if videos_data:
            df = pd.DataFrame(videos_data)
            
            # Generating a timestamped filename
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            excel_filename = f'output/youtube_live_data_{timestamp}.xlsx'
            df.to_excel(excel_filename, index=False)
            
            print(f"Video data has been saved to {excel_filename}")
        
        print("Waiting for the next update in 10 minutes...")
        time.sleep(600)  # Wait for 600 seconds (10 minutes) before the next iteration

if __name__ == "__main__":
    main()
