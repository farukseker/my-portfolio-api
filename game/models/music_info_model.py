from urllib.parse import urlparse

from django.db import models
from game.utils import MetaHandler


class MusicInfoModel(models.Model):
    title = models.TextField(default=None, null=True, blank=True)
    description = models.TextField(default=None, null=True, blank=True)
    image = models.URLField(default=None, null=True, blank=True)
    url = models.URLField(default=None, null=True, blank=True)
    length = models.PositiveBigIntegerField(default=1, null=True, blank=True)

    def save(self, *args, **kwargs):
        source = MetaHandler(self.url)
        content = source.get_content()
        if self.title is None or self.title == '':
            self.title = content.get('title', None)
        if self.description is None or self.description == '':
            self.description = content.get('description', None)
        if self.image is None:
            self.image = content.get('image', None)

        super().save(*args, **kwargs)

    @property
    def compatible_name(self):
        return self.title if len(self.title) < 27 else f'{self.title[:26]} ...'

    @property
    def is_spotify_url(self):
        return self.is_this_url('spotify.com', 'open.spotify.com')

    def is_this_url(self, *host_name_list):
        try:

            parsed_url = urlparse(self.url)
            return parsed_url.hostname in host_name_list
        except Exception as exception:
            # mb type error ;
            print(exception)

            pass

    def __str__(self):
        platform = 'Spotify' if self.is_spotify_url else 'YouTube'
        return f'Music {self.title} | {platform}'