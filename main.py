import pandas as pd 
from pytube import YouTube


def get_youtube_data(video_url):
    yt = YouTube(video_url)
    
    data = {
        'Title': yt.title,
        'Video URL': yt.watch_url,
        'Views': yt.views,
        'Length (seconds)': yt.length,
        'Author': yt.author,
        'Published Date': yt.publish_date,
        'Description': yt.description,
        'Thumbnail URL': yt.thumbnail_url,
    }
    
    return data

def main():
    video_url = 'https://www.youtube.com/watch?v=WQ1yc-4KfIU&t=1171s'
    
    video_data = get_youtube_data(video_url)
    
    df = pd.DataFrame([video_data])
    
    # Export the DataFrame to an Excel file
    excel_filename = 'output/youtube_data.xlsx'
    df.to_excel(excel_filename, index=False)
    
    print(f"Video data has been saved to {excel_filename}")


if __name__ == "__main__":
    main()