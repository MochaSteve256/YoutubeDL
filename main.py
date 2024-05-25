import os
from pytube import YouTube, Playlist
import re
import string
from moviepy.editor import AudioFileClip

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
        yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first().download()
    else:
        audio_file = yt.streams.filter(only_audio=True).order_by("abr").desc().first().download()
        base, ext = os.path.splitext(audio_file)
        new_file = base + '.mp3'
        clip = AudioFileClip(audio_file)
        clip.write_audiofile(new_file)
        clip.close()
        os.remove(audio_file)


try:
    while True:
        # obtain link from user
        try:
            link = input("Video/Playlist URL: \n")
        except KeyboardInterrupt:
            exit()
        
        if not "youtu" in link:
            print("Invalid link!")
            continue
        # prompt user for music
        music = prompt_music()
        # check if link is a playlist and download accordingly
        try:
            if not "playlist" in link:
                if not music:
                    try:
                        os.chdir(os.path.expanduser("~/Videos/YouTube"))
                    except FileNotFoundError:
                        os.mkdir(os.path.expanduser("~/Videos/YouTube"))
                        os.chdir(os.path.expanduser("~/Videos/YouTube"))
                else:
                    try:
                        os.chdir(os.path.expanduser("~/Music/YouTube"))
                    except FileNotFoundError:
                        os.mkdir(os.path.expanduser("~/Music/YouTube"))
                        os.chdir(os.path.expanduser("~/Music/YouTube"))
                
                download_video(link, music)
            else:
                if not music:
                    try:
                        os.chdir(os.path.expanduser("~/Videos/YouTube/Playlists"))
                    except FileNotFoundError:
                        os.mkdir(os.path.expanduser("~/Videos/YouTube/Playlists"))
                        os.chdir(os.path.expanduser("~/Videos/YouTube/Playlists"))
                else:
                    try:
                        os.chdir(os.path.expanduser("~/Music/YouTube/Playlists"))
                    except FileNotFoundError:
                        os.mkdir(os.path.expanduser("~/Music/YouTube/Playlists"))
                        os.chdir(os.path.expanduser("~/Music/YouTube/Playlists"))
            
                pl = Playlist(link)
                pl._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
                print('Number of videos in playlist: %s' % len(pl.video_urls))
                print("Now downloading all videos from: " + pl.title)
                a = pl.title
                for c in list(string.punctuation):
                    a = a.replace(c, " ")
                while a.endswith(" "):
                    a = a[:-1]
                os.system("mkdir " + '"'  + a + '"')
                os.chdir(a)
                for v in pl.video_urls:
                    download_video(v, music)

        except Exception as e:
            print("Failed with an exception: " + str(e))
        print("Done! File(s) at: " + os.getcwd())

except Exception as e:
    print("Terminated: " + e)
