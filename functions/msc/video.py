import youtube_dl as ytdl
import disnake
import datetime

YTDL_OPTS = {
    "default_search": "ytsearch",
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": "in_playlist"
}


class Video:
    """Class containing information about a particular video."""

    def __init__(self, url_or_search, requested_by):
        """Plays audio from (or searches for) a URL."""
        with ytdl.YoutubeDL(YTDL_OPTS) as ydl:
            video = self._get_info(url_or_search)
            video_format = video["formats"][0]
            self.stream_url = video_format["url"]
            self.video_url = video["webpage_url"]
            self.title = video["title"]
            self.uploader = video["uploader"] if "uploader" in video else ""
            self.thumbnail = video[
                "thumbnail"] if "thumbnail" in video else None
            self.requested_by = requested_by

    def _get_info(self, video_url):
        with ytdl.YoutubeDL(YTDL_OPTS) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video = None
            if "_type" in info and info["_type"] == "playlist":
                return self._get_info(
                    info["entries"][0]["url"])  # get info for first video
            else:
                video = info
            return video

    def get_embed(self):
        embed = disnake.Embed(
            title=f"Đang phát bài {self.title}",
            description=f"Bởi `{self.uploader}`",
            color=disnake.Color.red(),
        )
        embed.video.url = self.video_url
        embed.set_thumbnail(url=self.thumbnail)
        embed.timestamp = datetime.datetime.now()
        return embed