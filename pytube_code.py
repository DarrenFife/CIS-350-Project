import pytube as pyt
import os


class PytubeMethods:
    #Downloads Set Video to Project Folder (Need to Change Download Location)
    def pyDownload():
        # Expands the ~ to the user's home dir, but for me went to root
        #dir = os.path.expanduser("~/Downloads/YouTube-Downloads")
        dir = os.pardir + "/YouTube-Downloads/"
        print(dir)
        # Test id
        id = "dQw4w9WgXcQ";
        yt = pyt.YouTube("https://youtu.be/" + id)
        (yt.streams
            # Filter to only .mp4 files
            .filter(progressive=True, file_extension="mp4")
            .get_highest_resolution()

        #You can set the download location with the download function, but I couldn't figure out yet 
        # how to set it to desktop (or something else) without it being specific to my computer only
            .download(dir))

    pass
