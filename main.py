import os
from pytube import YouTube, Playlist
import re
import string
try:
    alreadyRun = False
    while 1:
        link = input("Video/Playlist URL: \n")
        music = 0
        def prompt():
            global music
            music = input("Is this a music download? (y/n)\n")
            if music == "y":
                music = True
            elif music == "n":
                music = False
            else:
                prompt()
        #prompt()
        music = False
        if not alreadyRun:
            if music:
                os.chdir("../../../Music/YouTube")
            else:
                os.chdir("../../../Videos/YouTube")
        alreadyRun = True
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
                    yt = YouTube(v)
                    print("Downloading: " + yt.title)
                    if not music:
                        yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first().download()
                    else:
                        yt.streams.filter(only_audio=True).desc().first().download()
            else:
                yt = YouTube(link)
                print("Downloading: " + yt.title)
                if not music:
                    yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first().download()
                else:
                    yt.streams.filter(only_audio=True).desc().first().download()
        except Exception as e:
            print("Failed with an exception: " + str(e))
            print("Done!")
except Exception as e:
    print("Terminated: " + e)
