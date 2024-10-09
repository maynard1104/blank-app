import streamlit as st
from pytube import YouTube

def main():
    st.title("YouTube Video Viewer")
    
    # URL input
    url = st.text_input("Enter YouTube URL:")
    
    if st.button("Load Video") and url:
        try:
            yt = YouTube(url)
            st.success(f"Successfully loaded: {yt.title}")
            
            # Video player
            st.video(url)
            
            # Video information
            st.write(f"Video Duration: {yt.length} seconds")
            st.write(f"Views: {yt.views}")
            st.write(f"Author: {yt.author}")
            
        except Exception as e:
            st.error(f"Error loading video: {str(e)}")

if __name__ == "__main__":
    main()
