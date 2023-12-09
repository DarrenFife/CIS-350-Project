"""This module is where the pytube functions and objects are incorporated"""
import re

import os
from pytube import YouTube, Playlist, Channel, extract
from pytube.exceptions import VideoUnavailable
from pytube.exceptions import RegexMatchError, AgeRestrictedError


class InvalidURLException(Exception):
    """Raised when URL is not valid"""


class InvalidVideoException(InvalidURLException):
    """Raised when URL is not a valid YDVideo"""


class InvalidPlaylistException(InvalidURLException):
    """Raised when URL is not a valid Playlist"""


class InvalidChannelException(InvalidURLException):
    """Raised when URL is not a valid Channel"""


class YDVideo(YouTube):
    """A video uploaded to YouTube.

    Keyword arguments:
    """
    # URL Parameter constructor
    def __init__(self, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"):
        """Construct a YDVideo object using the video
        uploaded to the given YouTube link."""
        try:
            extract.video_id(url)
        except RegexMatchError as e:
            raise InvalidVideoException from e
        try:
            super().__init__(url)
            self.video_url = url

            bad_chars = "<>:\"/\\|?*"

            self.clean_title = re.sub(rf'[{bad_chars}]', '',
                                      self.title).removesuffix(
                                          "...").strip() + ".mp4"
            self.clean_author = re.sub(rf'[{bad_chars}]', '',
                                       self.author).removesuffix("...").strip()

            print(f'Creating video object: {self.clean_title} from {url}')
            self.download_path = (os.pardir + "/YouTube-Downloads/" +
                                  self.clean_author + "/")
        except VideoUnavailable as e:
            raise e

    def download_video(self, max_res):
        """Download a video from a YouTube link.

        Keyword arguments:
        channel_name -- string of the name of the channel
            that posted the given video
        path -- string of the download path
        ("YouTube-Downloads" folder placed parallel to the program folder)
        """
        video_name = self.clean_author + "/" + self.clean_title

        try:
            # Filter to only .mp4 files
            filtered_streams = super().streams.filter(progressive=True,
                                                      file_extension="mp4")

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

            best_res_stream.download(output_path=self.download_path,
                                     filename=self.clean_title,
                                     skip_existing=True)
            print("Video downloaded: " + self.download_path +
                  self.clean_title + " with ID: " + self.video_id)
        except AgeRestrictedError:
            print(f'Video {self.video_url} is age restricted,' +
                  'skipping as no credentials.')
            return video_name + " (Skipped as Age Restricted)"

        return video_name


class YDPlaylist(Playlist):
    """A playlist uploaded to YouTube."""
    def __init__(self, url):
        if "list=" not in url:
            raise InvalidPlaylistException
        else:
            super().__init__(url)

            bad_chars = "<>:\"/\\|?*"

            self.clean_title = re.sub(
                rf'[{bad_chars}]', '', self.title).removesuffix("...").strip()

            self.yd_playlist = []

            for video_url in self.video_urls:
                try:
                    v = YDVideo(video_url)
                    self.yd_playlist.append(v)
                except VideoUnavailable as e:
                    print(f'Video from {e.video_id} is unavailable, skipping.')

    def download_playlist(self, max_res):
        """Download a playlist from a YouTube link."""
        playlist_path = os.pardir + "/YouTube-Downloads/Playlists/"
        file_path = playlist_path + self.clean_title + ".txt"
        print(f"Downloading to {file_path}")
        if not os.path.exists(playlist_path):
            os.makedirs(playlist_path)

        video_urls = []

        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as old_fplaylist:
                video_urls = old_fplaylist.readlines()
                old_fplaylist.close()
            os.remove(file_path)

            for video in self.yd_playlist:
                video_save_path = video.download_video(max_res) + "\n"

                if video_save_path not in video_urls:
                    video_urls.append(video_save_path)
        else:
            for video in self.yd_playlist:
                video_urls.append(video.download_video(max_res) + "\n")

        with open(file_path, 'x', encoding="utf-8") as fplaylist:
            fplaylist.writelines(video_urls)
            fplaylist.close()

        return file_path


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
    """A channel uploaded to YouTube."""
    def __init__(self, url):
        try:
            base_url = "https://www.youtube.com" + extract.channel_name(
                url).removesuffix("/None") + "/"
            print("Base:", base_url)
        except RegexMatchError as e:
            raise InvalidChannelException from e
        else:
            super().__init__(base_url)

            self.all_videos = []

            for video_url in self.video_urls:
                try:
                    v = YDVideo(url=video_url)
                    print('Creating video object:' +
                          f'{v.clean_title} from {video_url}')
                    self.all_videos.append(v)
                except VideoUnavailable as e:
                    print(f'Video from {e.video_id} is unavailable, skipping.')

            self.playlist_urls = []

            channel_pages = {base_url, base_url + "videos/",
                             base_url + "playlists/",
                             base_url + "releases/", url}

            for extension in channel_pages:
                channel_page = extension
                try:
                    extract.channel_name(channel_page)
                except RegexMatchError as e:
                    print(channel_page + " not found.")
                else:
                    found_urls = list(_find_urls(
                        'playlistId', Channel(channel_page).initial_data))

                    # Skip Watch Later playlists as they break download
                    if "https://www.youtube.com/playlist?list=WL" in found_urls:
                        found_urls.remove(
                            "https://www.youtube.com/playlist?list=WL")

                    print(channel_page + " found playlist(s):")
                    print(found_urls)

                    # Ensure no duplicates
                    for found_url in found_urls:
                        if found_url not in self.playlist_urls:
                            self.playlist_urls.append(found_url)
                        else:
                            print("Found duplicate playlist url (skipped):",
                                  found_url)

            print("All urls:")
            print(self.playlist_urls)

    def download_channel_videos(self, max_res):
        """Download all the individual videos found on the channel page"""
        for video in self.all_videos:
            video.download_video(max_res)

    def download_channel_playlists(self, max_res):
        """Download all the playlists discovered for the channel"""
        valid_playlist_paths = []

        for playlist_url in self.playlist_urls:
            try:
                playlist = YDPlaylist(playlist_url)
            except InvalidPlaylistException:
                print("Invalid Playlist: " + playlist_url)
            else:
                print("Valid Playlist: " + playlist_url)
                valid_playlist_paths.append(
                    playlist.download_playlist(max_res))
        return valid_playlist_paths

    def download_channel(self, max_res):
        """Wrapper function to run the two helper functions"""
        self.download_channel_videos(max_res)
        self.download_channel_playlists(max_res)


def check_channel_or_playlist_url(url):
    """Checks if a link is a channel or playlist"""
    try:
        extract.channel_name(url)
    except InvalidChannelException:
        return False
    return True


def download_link(url, max_res):
    """Download a YouTube link by turning it into the right type of object"""
    link_confirmed = False
    message = "Link unconfirmed"

    try:
        c = YDChannel(url)
    except InvalidChannelException:
        message = "Invalid Channel url: " + url
    else:
        link_confirmed = True
        message = "Valid Channel url: " + url
        c.download_channel(max_res)
    if not link_confirmed:
        try:
            p = YDPlaylist(url)
        except InvalidPlaylistException:
            message = "Invalid Channel/Playlist url: " + url
        else:
            link_confirmed = True
            message = "Valid Playlist url: " + url
            p.download_playlist(max_res)
    if not link_confirmed:
        try:
            v = YDVideo(url)
        except VideoUnavailable:
            message = "Unavailable Video: " + url
        except InvalidVideoException:
            message = "Invalid Channel/Playlist/Video url: " + url
        else:
            message = "Valid Video: " + url
            v.download_video(max_res)

    return message


# Test case
# download_link(
# "https://www.youtube.com/playlist?
# list=PLdQkToevBvCpDNl4Udlnhn13y8y1mTi5A", 720)
# Random Meme YouTuber I found test case
# download_link("https://www.youtube.com/@standjardanjar", 720)
# download_link("https://youtu.be/T5KBMhw87n8?feature=shared", 720)
# download_link(
# "https://www.youtube.com/channel/UCDBrVr0ttWpoRY-_yZajp2Q", 720)

# Age restricted test
# download_link("https://www.youtube.com/watch?v=gSPbrmIpcy0", 720)

# download_link("https://www.youtube.com/@alyankovic/", 720)
