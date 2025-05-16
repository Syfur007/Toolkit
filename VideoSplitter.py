"""
VideoSplitter.py

This script splits a video file into multiple chapters based on timestamps and titles provided in a separate text file.

Usage:
    1. Place the video file (e.g., 'welcome.mp4') in the same directory as this script.
    2. Create a 'chapters.txt' file where each line contains a timestamp and a chapter title, separated by a space.
       Example line: 
            00:00:00 Welcome
            00:01:23 Introduction

How it works:
    - Reads chapter timestamps and titles from 'chapters.txt'.
    - Splits 'welcome.mp4' into separate video files for each chapter using ffmpeg.
    - Output files are named as "<chapter_number>. <chapter_title>.mp4".

Dependencies:
    - ffmpeg (Python package)
    - ffmpeg must be installed and available in your system PATH. (The app needs to be installed)

Author: Syfur Rahman
Date: 16.05.25

"""



import ffmpeg

inputVideo = ffmpeg.input("welcome.mp4")
timestamps = [] 
titles = []


def readChapters(chaptersFile):
    with open(chaptersFile) as allChapters:
        lines = allChapters.readlines()
        for line in lines:
            time, chapterTitle = line.strip().split(" ", 1)
            timestamps.append(time)
            titles.append(chapterTitle)


readChapters("chapters.txt")



for chapter in range(len(timestamps)):
    inTitle = "welcome.mp4"
    outTitle = f"{chapter}. {titles[chapter]}.mp4"
    if chapter == len(timestamps)-1:
        stream = ffmpeg.input(inTitle, ss = timestamps[chapter]).output(outTitle)
    else:
        stream = ffmpeg.input(inTitle, ss = timestamps[chapter], to = timestamps[chapter+1]).output(outTitle)
    ffmpeg.run(stream)


