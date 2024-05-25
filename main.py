import os
from pytube import YouTube, Playlist
import re
import string

def prompt_music():
    try:
        music = input("Is this a music download? (y/n)\n")
    except KeyboardInterrupt:
        exit()
    if music == "y":
        return True
    elif music == "n":
        return False
    else:
        return prompt_music()

def download_video(link, music):
    yt = YouTube(link)
    print("Downloading: " + yt.title)
    if not music:
        os.chdir(os.path.expanduser("~/Videos/YouTube"))
        yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first().download()
    else:
        os.chdir(os.path.expanduser("~/Music/YouTube"))
        yt.streams.filter(only_audio=True).order_by("abr").desc().first().download()

try:
    while True:
        try:
            link = input("Video/Playlist URL: \n")
        except KeyboardInterrupt:
            exit()
        
        if not link.find("youtu") > 0:
            print("Invalid link!")
            continue
        
        music = prompt_music()
        
        try:
            if "playlist" in link:
                pl = Playlist(link)
                pl._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
                print('Number of videos in playlist: %s' % len(pl.video_urls))
                print("Now downloading all videos from: " + pl.title)
                os.chdir("Playlists")
                a = pl.title
                for c in list(string.punctuation):
                    a = a.replace(c, " ")
                while a.endswith(" "):
                    a = a[:-1]
                os.system("mkdir " + '"'  + a + '"')
                os.chdir(a)
                for v in pl.video_urls:
                    download_video(v, music)
            else:
                download_video(link, music)
        except Exception as e:
            print("Failed with an exception: " + str(e))
            print("Done!")
except Exception as e:
    print("Terminated: " + e)
