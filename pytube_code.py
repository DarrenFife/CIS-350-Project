import pytube as pyt
from pytube import extract
import os


class PytubeMethods:
    #Downloads Set Video to Project Folder (Need to Change Download Location)
    def pyDownload(url):
        # Expands the ~ to the user's home dir, but for me went to root
        #dir = os.path.expanduser("~/Downloads/YouTube-Downloads")
        dir = os.pardir + "/YouTube-Downloads/"
        print(dir)
        # Split yt url and take the second half which is the ID
        id = extract.video_id(url)
        # Test id
        # id = "dQw4w9WgXcQ";
        yt = pyt.YouTube(url)
        (yt.streams
            # Filter to only .mp4 files
            .filter(progressive=True, file_extension="mp4")
            .get_highest_resolution()

        #You can set the download location with the download function, but I couldn't figure out yet 
        # how to set it to desktop (or something else) without it being specific to my computer only
            .download(dir))
        print(id)

    pass
