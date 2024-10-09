import streamlit as st
import pafy
import cv2
import tempfile
import os
from pytube import YouTube

def download_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        # Create a temporary file
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, 'video.mp4')
        
        # Download the video
        stream.download(output_path=temp_dir, filename='video.mp4')
        
        return temp_path, yt.title
    except Exception as e:
        st.error(f"Error downloading video: {str(e)}")
        return None, None

def main():
    st.title("Online Video Viewer")
    
    # URL input
    url = st.text_input("https://www.youtube.com/watch?v=78yi4QbzYRs")
    
    if st.button("Load Video") and url:
        video_path, video_title = download_video(url)
        
        if video_path:
            st.success(f"Successfully loaded: {video_title}")
            
            # Video player
            st.video(video_path)
            
            # Video information
            try:
                cap = cv2.VideoCapture(video_path)
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                duration = frame_count / fps
                
                st.write(f"Video Duration: {duration:.2f} seconds")
                st.write(f"FPS: {fps}")
                
                cap.release()
            except Exception as e:
                st.error(f"Error getting video info: {str(e)}")

if __name__ == "__main__":
    main()
