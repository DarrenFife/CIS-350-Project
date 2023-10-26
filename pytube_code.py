import pytube as pyt
from pytube import YouTube, Playlist, Channel, extract
from pytube.exceptions import VideoUnavailable
from pytube.exceptions import RegexMatchError
import os


class InvalidURLException(Exception):
    """Raised when URL is not valid"""
    pass


class InvalidVideoException(InvalidURLException):
    """Raised when URL is not a valid Video"""
    pass


class InvalidPlaylistException(InvalidURLException):
    """Raised when URL is not a valid Playlist"""
    pass


class InvalidChannelException(InvalidURLException):
    """Raised when URL is not a valid Channel"""
    pass


class Video(YouTube):
    """A video uploaded to YouTube.

    Keyword arguments:
    """
    # URL Parameter constructor
    def __init__(self, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"):
        """Construct a Video object using the video uploaded to the given YouTube link."""
        try:
            extract.video_id(url)
        except RegexMatchError as e:
            raise InvalidVideoException from e
        else:
            try:
                super().__init__(url)
            except VideoUnavailable:
                print(f'Video {url} is unavailable, skipping.')
                raise VideoUnavailable
            else:
                print(f'Creating video object: {url}')
                self.channel_name = pyt.Channel(self.channel_url).channel_name

    """Downloads Set Video to Project Folder"""
    def download_video(self, max_res=720):
        """Download a video from a YouTube link.

        Keyword arguments:
        channel_name -- string of the name of the channel that posted the given video
        path -- string of the download path ("YouTube-Downloads" folder placed parallel to the program folder)
        """

        # Expands the ~ to the user's home dir, but for me went to root
        # dir = os.path.expanduser("~/Downloads/YouTube-Downloads")
        path = os.pardir + "/YouTube-Downloads/" + self.channel_name + "/"

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


class YDPlaylist(Playlist):
    def __init__(self, url):
        if "list=" not in url:
            raise InvalidPlaylistException
        else:
            super().__init__(url)

            self.yd_playlist = []

            for url in super().video_urls:
                self.yd_playlist.append(Video(url))

    def download_playlist(self, max_res=720):
        for video in self.yd_playlist:
            video.download_video(max_res)


class YDChannel(Channel):
    def __init__(self, url):
        try:
            extract.channel_name(url)
        except RegexMatchError as e:
            raise InvalidChannelException from e
        else:
            super().__init__(url)

            print("Channel playlist: " + self.playlist_url)
            self.all_videos = YDPlaylist(self.playlist_url)

    def download_channel(self, max_res=720):
        self.all_videos.download_playlist()


def download_link(url):
    """Download a YouTube link by turning it into the right type of object"""
    try:
        c = YDChannel(url)
    except InvalidChannelException:
        print("Invalid Channel " + url)
        try:
            p = YDPlaylist(url)
        except InvalidPlaylistException:
            print("Invalid Playlist " + url)
            try:
                v = Video(url)
            except InvalidVideoException:
                print("Invalid Video " + url)
            else:
                print("Valid Video " + url)
                v.download_video()
        else:
            print("Valid Playlist " + url)
            p.download_playlist()
    else:
        print("Valid Channel " + url)
        c.download_channel()


# Test case
#download_link("https://www.youtube.com/playlist?list=PLdQkToevBvCpDNl4Udlnhn13y8y1mTi5A")
# Random Meme YouTuber I found test case
#download_link("https://www.youtube.com/@standjardanjar")
#download_link("https://youtu.be/T5KBMhw87n8?feature=shared")
#download_link("https://www.youtube.com/channel/UCDBrVr0ttWpoRY-_yZajp2Q")
