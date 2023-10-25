import pytube as pyt
from pytube import extract
import os


class Video(pyt.YouTube):
    """A video uploaded to YouTube.

    Keyword arguments:
    """
    # URL Parameter constructor
    def __init__(self, url):
        """Construct a Video object using the video uploaded to the given YouTube link."""
        super().__init__(url)

    # TODO: Make default constructor work?
    # Default constructor
    """def __init__(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        Video(url)
        """

    # Downloads Set Video to Project Folder
    def download_video(self):
        """Download a video from a YouTube link.

        Keyword arguments:
        channel_name -- string of the name of the channel that posted the given video
        path -- string of the download path ("YouTube-Downloads" folder placed parallel to the program folder)
        """
        channel_name = pyt.Channel(self.channel_url).channel_name

        # Expands the ~ to the user's home dir, but for me went to root
        # dir = os.path.expanduser("~/Downloads/YouTube-Downloads")
        path = os.pardir + "/YouTube-Downloads/" + channel_name + "/"
        (super().streams
            # Filter to only .mp4 files
            .filter(progressive=True, file_extension="mp4")
            .get_highest_resolution()
            .download(output_path=path, skip_existing=True))
        print("Video downloaded: " + path + self.title + " with ID: " + self.video_id)

    pass
