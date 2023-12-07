import os
from os import startfile
from unittest import TestCase
import pytube_code
from pytube_code import YDVideo, YDPlaylist, YDChannel
from pytube.exceptions import VideoUnavailable, AgeRestrictedError


class TestYDVideo(TestCase):
    def test_download_video(self):
        # Normal video download test
        video_path = os.pardir + "/YouTube-Downloads/standjar danjar/ElderScrollsKnightMeme.mp4"
        print("Video path", video_path)
        if os.path.exists(video_path):
            os.remove(video_path)
            print("Removed video")
        else:
            print("Does not exist")
        v = YDVideo("https://youtu.be/T5KBMhw87n8?feature=shared")
        video_path = os.pardir + "/YouTube-Downloads/" + v.download_video(720)
        print("Video path", video_path)
        # For some reason exists does not return true in either case
        self.assertTrue(os.path.exists(video_path))

    def test_video_unavailable(self):
        # Private video test
        v = YDVideo("")
        self.assertRaises(VideoUnavailable)

    def test_video_age_restricted(self):
        # Age restricted video test
        v = YDVideo("https://www.youtube.com/watch?v=gSPbrmIpcy0")
        v.download_video(720)
        self.assertRaises(AgeRestrictedError)


class TestYDPlaylist(TestCase):
    def test_download_playlist(self):
        self.fail()


class TestYDChannel(TestCase):
    def test_download_channel_videos(self):
        self.fail()

    def test_download_channel_playlists(self):
        self.fail()

    def test_download_channel(self):
        self.fail()


class Test(TestCase):
    def test_check_channel_or_playlist_url(self):
        self.fail()

    def test_download_link(self):
        self.fail()
