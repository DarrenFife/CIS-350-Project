import pytube as pyt
from pytube import YouTube, Playlist, Channel, extract
from pytube.exceptions import VideoUnavailable
from pytube.exceptions import RegexMatchError
import os

DOWNLOAD_DIR = os.pardir + "/YouTube-Downloads/"

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
        """Construct a Video object using the video
        uploaded to the given YouTube link."""
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
        channel_name -- string of the name of the channel
            that posted the given video
        path -- string of the download path
        ("YouTube-Downloads" folder placed parallel to the program folder)
        """

        path = DOWNLOAD_DIR + self.channel_name + "/"

        # Filter to only .mp4 files
        filtered_streams = super().streams.filter(progressive=True,
                                                  file_extension="mp4")
        # TODO: Filter by resolution instead to do this?
        # reversed_streams = super().streams.order_by("resolution")
        # print(reversed_streams)
        # filtered_streams = super().streams
        # print(filtered_streams)
        highest_res_stream = filtered_streams.get_highest_resolution()

        # Print resolutions for testing
        print([stream.resolution for stream in filtered_streams])

        # Initialize to the lowest res in case no res is below max res
        best_res_stream = filtered_streams.get_lowest_resolution()

        # Find the best res
        for stream in filtered_streams:
            if (stream.resolution is not None and
                    int(stream.resolution.removesuffix('p')) <= max_res):
                best_res_stream = stream

        print("Best res:", best_res_stream.resolution)

        best_res_stream.download(output_path=path, skip_existing=True)
        print("Video downloaded: " + path + self.title +
              " with ID: " + self.video_id)

    pass


class YDPlaylist(Playlist):
    def __init__(self, url):
        if "list=" not in url:
            raise InvalidPlaylistException
        else:
            super().__init__(url)

            self.yd_playlist = []

            for video_url in self.video_urls:
                self.yd_playlist.append(Video(video_url))

    def download_playlist(self, max_res=720):
        # TODO: Open file of
        print("Dir:", self.owner, "Title:", self.title + ".txt")
        print(self.title)
        for video in self.yd_playlist:
            # TODO: Get the name of the playlist owner, then save name of playlist.txt as in their folder under Playlists
            video.download_video(max_res)
            print("Append to txt:", video.channel_name + "/" + video.title)


def _find_ids(key, var):
    if hasattr(var, 'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in _find_ids(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for playlist_id in _find_ids(key, d):
                        yield playlist_id


def _find_urls(key, var):
    ids = set(_find_ids(key, var))
    for playlist_id in ids:
        url = f'https://www.youtube.com/playlist?list={playlist_id}'
        yield url


class YDChannel(Channel):
    def __init__(self, url):
        try:
            base_url = "https://www.youtube.com/" + extract.channel_name(url).split("/")[1] + "/"
            print("Base:", base_url)
        except RegexMatchError as e:
            raise InvalidChannelException from e
        else:
            super().__init__(base_url)

            self.all_videos = []

            for video_url in self.video_urls:
                self.all_videos.append(Video(video_url))

            self.playlist_urls = []

            channel_pages = {base_url, base_url + "videos/", base_url + "playlists/", base_url + "releases/", url}

            for extension in channel_pages:
                channel_page = base_url + extension
                try:
                    extract.channel_name(channel_page)
                except RegexMatchError as e:
                    print(channel_page + " not found.")
                else:
                    found_urls = list(_find_urls('playlistId', Channel(channel_page).initial_data))

                    # Skip Watch Later playlists as they break download
                    if "https://www.youtube.com/playlist?list=WL" in found_urls:
                        found_urls.remove("https://www.youtube.com/playlist?list=WL")

                    print(channel_page + " found playlist(s):")
                    print(found_urls)

                    # Ensure no duplicates
                    for found_url in found_urls:
                        if found_url not in self.playlist_urls:
                            self.playlist_urls.append(found_url)
                        else:
                            print("Found duplicate playlist url (skipped):", found_url)

            print("All urls:")
            print(self.playlist_urls)

    def download_channel_videos(self, max_res=720):
        for video in self.all_videos:
            video.download_video(max_res)

    def download_channel_playlists(self, max_res=720):
        for playlist_url in self.playlist_urls:
            try:
                playlist = YDPlaylist(playlist_url)
            except InvalidPlaylistException:
                print("Invalid Playlist: " + playlist_url)
            else:
                print("Valid Playlist: " + playlist_url)
                playlist.download_playlist(max_res)

    def download_channel(self, max_res=720):
        # TODO: Fix download_channel
        pass
        self.download_channel_videos(max_res)
        self.download_channel_playlists(max_res)


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
# download_link("https://www.youtube.com/playlist?list=PLdQkToevBvCpDNl4Udlnhn13y8y1mTi5A")
# Random Meme YouTuber I found test case
# download_link("https://www.youtube.com/@standjardanjar")
# download_link("https://youtu.be/T5KBMhw87n8?feature=shared")
# download_link("https://www.youtube.com/channel/UCDBrVr0ttWpoRY-_yZajp2Q")

#download_link("https://www.youtube.com/@alyankovic/")