"""
VideoSplitter.py

A command-line tool to split a video file into multiple chapter-based segments using ffmpeg.
Chapters are defined by a text file containing timestamps and titles.

Features:
    - Splits a video into chapters based on a chapters file.
    - Accepts command-line arguments for video file, chapters file, and output directory.
    - If arguments are not provided, prompts the user interactively.
    - Output files are named as "<chapter_number>. <chapter_title>.mp4" in the specified directory.

Usage:
    Command-line:
        python VideoSplitter.py -v <video_file> -c <chapters_file> -o <output_directory>
    Interactive (if arguments are omitted):
        python VideoSplitter.py
        # The script will prompt for missing parameters.

Chapters file format:
    Each line should contain a timestamp and a chapter title, separated by a space.
    Example:
        00:00:00 Welcome
        00:01:23 Introduction

Dependencies:
    - ffmpeg (Python package: pip install ffmpeg-python)
    - ffmpeg must be installed and available in your system PATH.

Author: Syfur Rahman
Date: 16.05.25

"""


import os
import ffmpeg
import argparse

timestamps = [] 
titles = []


def readChapters(chaptersFile):
    with open(chaptersFile) as allChapters:
        lines = allChapters.readlines()
        for line in lines:
            time, chapterTitle = line.strip().split(" ", 1)
            timestamps.append(time)
            titles.append(chapterTitle)


def split_video(videoFile, chaptersFile, outputDir):
    timestamps.clear()
    titles.clear()
    readChapters(chaptersFile)

    if outputDir:
        os.makedirs(outputDir, exist_ok=True)

    for chapter in range(len(timestamps)):
        outTitle = f"{chapter+1}. {titles[chapter]}.mp4"
        if outputDir:
            outTitle = f"{outputDir}/{outTitle}"

        if chapter == len(timestamps)-1:
            stream = ffmpeg.input(videoFile, ss = timestamps[chapter]).output(outTitle)
        else:
            stream = ffmpeg.input(videoFile, ss = timestamps[chapter], to = timestamps[chapter+1]).output(outTitle)
        ffmpeg.run(stream)


def main():
    parser = argparse.ArgumentParser(
        description="Split a video into chapters using timestamps and titles from a text file."
    )
    parser.add_argument('-v', '--video', help='Path to the video file')
    parser.add_argument('-c', '--chapters', help='Path to the chapters file')
    parser.add_argument('-o', '--output', help='Output directory for split videos')

    args = parser.parse_args()

    videoFile = args.video
    chaptersFile = args.chapters
    outputDir = args.output

    if not videoFile:
        videoFile = input("Location of Video File: ").strip()
    if not chaptersFile:
        chaptersFile = input("Location of Chapters File: ").strip()
    if not outputDir:
        outputDir = input("Output Directory: ").strip()

    split_video(videoFile, chaptersFile, outputDir)


if __name__ == "__main__":
    main()