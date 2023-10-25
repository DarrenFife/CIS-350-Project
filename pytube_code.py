import pytube as pyt
from pytube import extract
import os


class Video(pyt.YouTube):
    """A video uploaded to YouTube.

    Keyword arguments:
    """
    # URL Parameter constructor
    def __init__(self, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"):
        """Construct a Video object using the video uploaded to the given YouTube link."""
        super().__init__(url)


    # Downloads Set Video to Project Folder
    def download_video(self, max_res=720):
        """Download a video from a YouTube link.

        Keyword arguments:
        channel_name -- string of the name of the channel that posted the given video
        path -- string of the download path ("YouTube-Downloads" folder placed parallel to the program folder)
        """
        channel_name = pyt.Channel(self.channel_url).channel_name

        # Expands the ~ to the user's home dir, but for me went to root
        # dir = os.path.expanduser("~/Downloads/YouTube-Downloads")
        path = os.pardir + "/YouTube-Downloads/" + channel_name + "/"

        # Filter to only .mp4 files
        filtered_streams = super().streams.filter(progressive=True, file_extension="mp4")
        # TODO: Filter by resolution instead to do this?
        #reversed_streams = super().streams.order_by("resolution")
        #print(reversed_streams)
        #filtered_streams = super().streams
        #print(filtered_streams)
        highest_res_stream = filtered_streams.get_highest_resolution()

        # Print resolutions for testing
        print([stream.resolution for stream in filtered_streams])

        # Initialize to the lowest res in case no res is below max res
        best_res_stream = filtered_streams.get_lowest_resolution()

        # Find the best res
        for stream in filtered_streams:
            if stream.resolution is not None and int(stream.resolution.removesuffix('p')) <= max_res:
                best_res_stream = stream

        print("Best res:", best_res_stream.resolution)

        best_res_stream.download(output_path=path, skip_existing=True)
        print("Video downloaded: " + path + self.title + " with ID: " + self.video_id)

    pass
