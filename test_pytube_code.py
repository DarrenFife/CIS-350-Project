import os
from unittest import TestCase
import pytube_code as pytc
from pytube_code import YDVideo, YDPlaylist, YDChannel
from pytube.exceptions import VideoUnavailable, AgeRestrictedError


class TestYDVideo(TestCase):

    def test_download_video_with_string(self):
        """Test if the video downloads using the returned string"""
        v = YDVideo("https://youtu.be/T5KBMhw87n8?feature=shared")
        self.assertEqual(v.download_video(720), "standjar danjar/ElderScrollsKnightMeme.mp4.mp4")

    def test_download_video_with_file(self):
        """Normal video download test"""
        video_path = os.pardir + "/YouTube-Downloads/standjar danjar/ElderScrollsKnightMeme.mp4.mp4"
        print("Video path", video_path)
        if os.path.exists(video_path):
            os.remove(video_path)
            print("Removed video:", video_path)
        v = YDVideo("https://youtu.be/T5KBMhw87n8?feature=shared")
        video_path = os.pardir + "/YouTube-Downloads/" + v.download_video(720)
        print("Video path", video_path)
        self.assertTrue(os.path.exists(video_path))
        os.remove(video_path)

    def test_video_unavailable(self):
        """Private video test"""
        with self.assertRaises(VideoUnavailable):
            YDVideo("https://www.youtube.com/watch?v=XKN3uZX2QMA")

    def test_video_age_restricted(self):
        """Age restricted video test"""
        v = YDVideo("https://www.youtube.com/watch?v=gSPbrmIpcy0")
        error_message = 'alyankovic/WEIRD The Al Yankovic Story - teaser trailer.mp4 (Skipped as Age Restricted)'
        self.assertEqual(v.download_video(720), error_message)


class TestYDPlaylist(TestCase):
    @classmethod
    def setUpClass(self):
        """Setup for YDPlaylist tests"""
        self.p = YDPlaylist("https://www.youtube.com/playlist?list=PLdQkToevBvCpDNl4Udlnhn13y8y1mTi5A")

    def test_download_playlist_with_string(self):
        """Test if the playlist downloads using the returned string"""
        self.assertEqual(self.p.download_playlist(720), os.pardir + "/YouTube-Downloads/Playlists/350 Test Vids.txt")

    def test_download_playlist_with_file(self):
        """Test if the playlist downloads using the contents of the generated text file"""
        playlist_path = self.p.download_playlist(720)

        fplaylist = open(playlist_path, "r")
        video_paths = fplaylist.readlines()
        fplaylist.close()
        os.remove(playlist_path)
        self.assertEqual(len(video_paths), 3)
        video1 = 'Weird Al Yankovic/Amish Paradise (Parody of Gangsta\'s Paradise - Official HD.mp4\n'
        video2 = 'Weird Al Yankovic/Party In The CIA (Parody of Party In The U.S.A. by Miley Cy.mp4\n'
        video3 = 'CaptainSparklez/Fallen Kingdom - A Minecraft Parody of Coldplay\'s Viva la Vida (Music Video).mp4\n'
        self.assertEqual(video_paths[0], video1)
        self.assertEqual(video_paths[1], video2)
        self.assertEqual(video_paths[2], video3)
        # Would be nice to do this, but uncertain why file is not being found
        for video_path in video_paths:
            video_path = video_path.removesuffix("\n")
            file_path = os.pardir + "/YouTube-Downloads/" + video_path
            result = os.path.isfile(file_path)
            # print("Checking if exists:", file_path, result)
            self.assertTrue(result)
            os.remove(file_path)

    def test_double_download_playlist_with_file(self):
        # Test if the playlist downloads additional files using the contents of the generated the text file
        self.p.download_playlist(720)
        self.test_download_playlist_with_file()


class TestYDChannel(TestCase):
    @classmethod
    def setUpClass(self):
        playlists_path = os.pardir + "/YouTube-Downloads/Playlists/"
        if os.path.isdir(playlists_path):
            for filename in os.listdir(playlists_path):
                os.unlink(playlists_path + filename)
            os.rmdir(playlists_path)
        self.c = YDChannel("https://www.youtube.com/@standjardanjar")

    def test_download_channel_videos(self):
        """Test downloading all channel videos to check it doesn't error"""
        self.c.download_channel_videos(720)

    def test_download_channel_playlists(self):
        """Test downloaded all playlists from a channel"""
        playlist_paths = self.c.download_channel_playlists(720)
        for playlist_path in playlist_paths:
            path_found = os.path.isfile(playlist_path)
            print(f"Path {playlist_path} found: {path_found}")
            self.assertTrue(path_found)

    def test_download_channel(self):
        """Test downloading everything from a channel"""
        self.c.download_channel(720)


class Test(TestCase):
    def test_check_channel_or_playlist_url(self):
        """Test if checking is a channel works"""
        self.assertTrue(pytc.check_channel_or_playlist_url("https://www.youtube.com/@standjardanjar"))
        # not_channel = "https://www.youtube.com/watch?v=XKN3uZX2QMA"
        # self.assertFalse(pytc.check_channel_or_playlist_url(not_channel))

    def test_download_link(self):
        """Test if downloading link figures out what to do correctly"""
        valid_channel = "https://www.youtube.com/@standjardanjar"
        m = pytc.download_link(valid_channel, 720)
        self.assertEqual(m, "Valid Channel url: " + valid_channel)
        # invalid_channel = "https://www.youtube.com/cmarkiplier"
        # m = pytc.download_link(invalid_channel, 720)
        # self.assertEqual(m, "Invalid Channel url: " + invalid_channel)
        valid_playlist = "https://www.youtube.com/playlist?list=PLdQkToevBvCpDNl4Udlnhn13y8y1mTi5A"
        m = pytc.download_link(valid_playlist, 720)
        self.assertEqual(m, "Valid Playlist url: " + valid_playlist)
        # invalid_playlist = "https://www.youtube.com/playlist?list=PLdQkToevBvCpNl4Udln13y8y1mTi5A"
        # m = pytc.download_link(invalid_playlist, 720)
        # self.assertEqual(m, "Invalid Channel/Playlist url: " + invalid_playlist)
        valid_video = "https://youtu.be/T5KBMhw87n8?feature=shared"
        m = pytc.download_link(valid_video, 720)
        self.assertEqual(m, "Valid Video: " + valid_video)
        invalid_url = "https://www.youtube.com/watch?v=T5KBM87n8"
        m = pytc.download_link(invalid_url, 720)
        self.assertEqual(m, "Invalid Channel/Playlist/Video url: " + invalid_url)
        unavailable_video = "https://www.youtube.com/watch?v=XKN3uZX2QMA"
        m = pytc.download_link(unavailable_video, 720)
        self.assertEqual(m, "Unavailable Video: " + unavailable_video)
