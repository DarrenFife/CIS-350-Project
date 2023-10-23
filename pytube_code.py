import pytube as pyt


class PytubeMethods:
    #Downloads Set Video to Project Folder (Need to Change Download Location)
    def pyDownload():
        yt = pyt.YouTube("https://youtu.be/dQw4w9WgXcQ")
        stream = yt.streams.get_highest_resolution()
        #You can set the download location with the download function, but I couldn't figure out yet 
        # how to set it to desktop (or something else) without it being specific to my computer only
        stream.download()

    pass
