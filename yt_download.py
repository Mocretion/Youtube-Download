from pytube import YouTube
from pathlib import Path
import os

def getYoutubeVideo():
    print("Enter Youtube Link")
    strLink = input()
    
    print("Loading...")
    try:
        yt = YouTube(strLink,
             use_oauth=True,
             allow_oauth_cache=True)
        return yt
    except:
        print()
        return getYoutubeVideo()
    
    
def getFormat():
    print()
    print("1: mp4")
    print("2: mp3")
    
    format = input("Select format: ")

    if(format != "1" and format != "2"):
        return getFormat()
    
    if(format == "1"):
        return "mp4"
    else:
        return "mp3"


def downloadFile(files, yt, format):
    print()
    file = input("Choose Download: ")
    
    try:
        file = int(file)
        file = file - 1
    except:
        return downloadFile(files, yt, format)
    
    if(file < 0 or file > len(files)):
        return downloadFile(files, yt, format)
    
    file = str(files[file])
    itag = file.split('"')[1]
    
    print("Downloading...")
    yt.streams.get_by_itag(int(itag)).download(output_path=Path.home() / "Downloads")
    
    fileName = yt.streams.get_by_itag(int(itag)).default_filename
    
    if(format == "mp3" and ".mp4" in fileName):
        os.rename(os.path.join(Path.home() / "Downloads", fileName), os.path.join(Path.home() / "Downloads", fileName.replace('.mp4', '.mp3')))
        
    print("Done!")



while(True):
    yt = getYoutubeVideo()
    format = getFormat()

    if(format == 'mp4'):
        files = yt.streams.filter(file_extension="mp4").filter(progressive=True).order_by('resolution').desc()
    elif(format == 'mp3'):
        files = yt.streams.filter(only_audio=True).order_by('abr').desc()

    print()
    print()
    
    for i in range(len(files)):
        print(str(i + 1) + ": " + str(files[i]))

    downloadFile(files, yt, format)
    print()
    print()
    print()
    print("Maybe another?")