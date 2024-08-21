from moviepy.editor import *

# Load the WebM file
webm_clip = VideoFileClip("sample.webm")

# Write the clip to an MP4 file
webm_clip.write_videofile("output.mp4", codec="libx264")