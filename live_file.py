import pandas as pd 
from googleapiclient.discovery import build

def get_youtube_data(api_key, *video_ids):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    all_data = []
    
    for video_id in video_ids:
        # Get video details
        video_response = youtube.videos().list(part='snippet,liveStreamingDetails', id=video_id).execute()
        
        
        print(video_response)
        
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
    api_key = 'AIzaSyA70PJAcyWR0UbGUq98E8fpD_-ysHSuLKo'
    
    ktn_home = "3HKRlDRWdbc"
    ktn_news = "OdIxeE2eWSg"
    citizen_news = "cq3jNiquchw"
    
    video_ids = [citizen_news, ktn_news , ktn_home]  # Replace with your actual video IDs


    videos_data = get_youtube_data(api_key, *video_ids)
    
    if videos_data:
        df = pd.DataFrame(videos_data)
        
        # Export the DataFrame to an Excel file
        excel_filename = 'output/youtube_live_data.xlsx'
        df.to_excel(excel_filename, index=False)
        
        print(f"Video data has been saved to {excel_filename}")

if __name__ == "__main__":
    main()
