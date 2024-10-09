import streamlit as st
import streamlit.components.v1 as components
from pytube import YouTube
import time
import ssl
import certifi

# SSL Context fix
ssl._create_default_https_context = ssl._create_unverified_context

def create_autoplay_html(video_id, muted=True):
    return f"""
    <iframe 
        width="300" 
        height="200" 
        src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute={1 if muted else 0}"
        frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
    """

def extract_video_id(url):
    if 'watch?v=' in url:
        return url.split('watch?v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        return url.split('youtu.be/')[1].split('?')[0]
    return None

def main():
    st.set_page_config(layout="wide")
    st.title("Automated Multi-Instance YouTube Viewer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        url = st.text_input("Enter YouTube URL:")
        num_instances = st.number_input("Number of instances to open", min_value=1, max_value=20, value=2)
    
    with col2:
        duration = st.number_input("Viewing duration (minutes)", min_value=1, max_value=60, value=5)
        start_button = st.button("Start Viewing")

    if start_button and url:
        video_id = extract_video_id(url)
        
        if video_id:
            try:
                yt = YouTube(url)
                st.success(f"Playing {num_instances} instances of: {yt.title}")
                
                # Create a grid layout for multiple videos
                cols = st.columns(3)  # 3 columns for better layout
                
                for i in range(num_instances):
                    with cols[i % 3]:
                        components.html(create_autoplay_html(video_id), height=220)
                
                # Countdown timer
                placeholder = st.empty()
                for remaining in range(duration * 60, -1, -1):
                    minutes, seconds = divmod(remaining, 60)
                    placeholder.text(f"Time remaining: {minutes:02d}:{seconds:02d}")
                    time.sleep(1)
                
                st.success(f"Finished watching {num_instances} instances for {duration} minutes!")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Invalid YouTube URL. Please check the URL and try again.")

if __name__ == "__main__":
    main()
