import os
import re

from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def extract_video_subclip(movie_name: str, start_time_str: str, end_time_str: str) -> None:
    # Convert start and end times from string to seconds
    start_time = start_time_str.replace(",", ":").split(":")
    end_time = end_time_str.replace(",", ":").split(":")

    start = (int(start_time[0]) * 60 * 60) + (int(start_time[1]) * 60) + \
        (int(start_time[2])) + (int(start_time[3]) / 1000)
    end = (int(end_time[0]) * 60 * 60) + (int(end_time[1]) * 60) + \
        (int(end_time[2])) + (int(end_time[3]) / 1000)

    # Create a regex pattern to match the movie name with any extension
    pattern = re.compile(re.escape(movie_name) + r'\.\w+')
    movie_file = None

    # Search for the file in the current directory
    for filename in os.listdir('./movies'):
        if pattern.match(filename):
            movie_file = filename
            break

    # Check if the movie file is not in MP4 format
    if movie_file:
        # Create a new filename with .mp4 extension
        mp4_filename = os.path.splitext(movie_file)[0] + '_awade_.mp4'
        original_clip = VideoFileClip("./movies/" + movie_file)
        subclip = original_clip.subclip(start, end)
        subclip.write_videofile(mp4_filename, codec="libx264")

    # ffmpeg_extract_subclip(
    #     movie_file,
    #     start_time,
    #     end_time,
    #     targetname=f"{movie_name}_awade.mp4"
    # )
