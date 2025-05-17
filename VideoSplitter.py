"""
VideoSplitter.py

A command-line tool to split a video file into multiple chapter-based segments using ffmpeg.
Chapters are defined by a text file containing timestamps and titles.

Features:
    - Splits a video into chapters based on a chapters file.
    - Accepts command-line arguments for video file, chapters file, and output directory.
    - If arguments are not provided, prompts the user interactively.
    - Output files are named as "<chapter_number>. <chapter_title>.mp4" in the specified directory.
    - Check Integrity of a split by providing an -i or --integrity flag
    
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

def readChapters(chaptersFile):
    timestamps = []
    titles = []
    with open(chaptersFile) as allChapters:
        lines = allChapters.readlines()
        for line in lines:
            time, chapterTitle = line.strip().split(" ", 1)
            timestamps.append(time)
            titles.append(chapterTitle)
    return timestamps, titles


def timeStampConvert(timestamp):
    units = list(map(int, timestamp.strip().split(":")))
    return units[0]*3600 + units[1]*60 + units[2]


def split_video(videoFile, chaptersFile, outputDir):
    timestamps, titles = readChapters(chaptersFile)
    videoDuration = float(ffmpeg.probe(videoFile)['format']['duration'])

    if outputDir:
        os.makedirs(outputDir, exist_ok=True)

    for chapter in range(len(timestamps)):
        outTitle = f"{chapter+1}. {titles[chapter]}.mp4"
        if outputDir:
            outTitle = os.path.join(outputDir, outTitle)

        isLastChapter = chapter == len(timestamps)-1

        if os.path.exists(outTitle) :
            outmeta = ffmpeg.probe(outTitle)
            currentDuration = float(outmeta['format']['duration'])

            if isLastChapter:
                originalDuration = videoDuration - timeStampConvert(timestamps[chapter])
            else:
                originalDuration = timeStampConvert(timestamps[chapter+1]) - timeStampConvert(timestamps[chapter])
            
            if abs(originalDuration - currentDuration) < 1:
                print(f"{titles[chapter]} already exists!")
                continue

        if isLastChapter:
            stream = ffmpeg.input(videoFile, ss = timestamps[chapter]).output(outTitle)
        else:
            stream = ffmpeg.input(videoFile, ss = timestamps[chapter], to = timestamps[chapter+1]).output(outTitle)
        ffmpeg.run(stream)


def integrity_check(videoFile, chaptersFile, outputDir):
    timestamps, titles = readChapters(chaptersFile)
    videoDuration = float(ffmpeg.probe(videoFile)['format']['duration'])
    chaptersDuration = 0.0

    print("Running Integrity check...")

    for chapter in range(len(timestamps)):
        chapterFile = f"{chapter+1}. {titles[chapter]}.mp4"
        if outputDir:
            chapterFile = os.path.join(outputDir, chapterFile)

        isLastChapter = chapter == len(timestamps)-1

        if os.path.exists(chapterFile):
            chaptersDuration += float(ffmpeg.probe(chapterFile)['format']['duration'])

    if abs(videoDuration - chaptersDuration) > 1:
        print("Video Length Mismatch!")
        print(f"Original Video Duration: {videoDuration}")
        print(f"Total Chapters Duration: {chaptersDuration}")
        return False
    else:
        print("Split is performed Successfully!")


def main():
    parser = argparse.ArgumentParser(
        description="Split a video into chapters using timestamps and titles from a text file."
    )
    parser.add_argument('-v', '--video', help='Path to the video file')
    parser.add_argument('-c', '--chapters', help='Path to the chapters file')
    parser.add_argument('-o', '--output', help='Output directory for split videos')
    parser.add_argument('-i', '--integrity', action='store_true', help='Only check integrity, do not split video')

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

    if not args.integrity:
        split_video(videoFile, chaptersFile, outputDir)
        
    integrity_check(videoFile, chaptersFile, outputDir)


if __name__ == "__main__":
    main()