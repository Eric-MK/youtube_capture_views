import pandas as pd
from googleapiclient.discovery import build
import time  # Import the time module
import os  # Import the os module for file existence check

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
            }

            all_data.append(data)
        else:
            print(f"Error: No video details found for video ID {video_id}")
            
    return all_data

def main():
    api_key = ''  # Use your actual API key
    
    ktn_home = "SBxgLlZNebs"
    ktn_news = "0HL14aKXsCY"
    citizen_news = "YNN2atp2MoY"
    
    video_ids = [citizen_news, ktn_news , ktn_home]
    
    capture_count = 0  # Initialize capture count
    excel_filename = 'output/youtube_live_data.xlsx'  # Define the Excel filename

    while capture_count < 3:  # Loop until 3 captures are completed
        videos_data = get_youtube_data(api_key, *video_ids)
        
        if videos_data:
            # Add a timestamp or interval identifier to each row of data
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            for data in videos_data:
                data['Capture Time'] = timestamp
            
            # Check if the Excel file already exists
            if os.path.exists(excel_filename):
                # Read the existing data
                existing_df = pd.read_excel(excel_filename)
                new_df = pd.DataFrame(videos_data)
                updated_df = pd.concat([existing_df, new_df], ignore_index=True)
            else:
                updated_df = pd.DataFrame(videos_data)
            
            # Save the updated data back to the Excel file
            updated_df.to_excel(excel_filename, index=False)
            print(f"Video data has been saved/updated to {excel_filename}")
        
        capture_count += 1  # Increment the capture count
        
        if capture_count < 3:  # Check if we should continue
            print("Waiting for the next update in 10 minutes...")
            time.sleep(60)  # Wait for 600 seconds (10 minutes) before the next iteration
        else:
            print("Completed 3 captures.")

if __name__ == "__main__":
    main()
