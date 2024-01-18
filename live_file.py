import pandas as pd 
from googleapiclient.discovery import build

def get_youtube_data(api_key, video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)

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

        return data
    else:
        print(f"Error: No video details found for video ID {video_id}")
        return None

def main():
    api_key = 'AIzaSyA70PJAcyWR0UbGUq98E8fpD_-ysHSuLKo'
    video_id = 'cq3jNiquchw'  # Replace with your actual video ID

    video_data = get_youtube_data(api_key, video_id)
    
    if video_data:
        df = pd.DataFrame([video_data])
        
        # Export the DataFrame to an Excel file
        excel_filename = 'output/youtube_live_data.xlsx'
        df.to_excel(excel_filename, index=False)
        
        print(f"Video data has been saved to {excel_filename}")

if __name__ == "__main__":
    main()
