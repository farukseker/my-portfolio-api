from django.db import models


class GameInfoModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)
    tags = models.ManyToManyField('tags.TagModel', blank=True)
    banner = models.ForeignKey(
        'media_manager.MediaModel',
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True
        )

    game_url = models.TextField(blank=True, default=None, null=True)

    def save(self, *args, **kwargs):
        if self.banner.media_type != self.banner.MediaType.IMAGE:
            raise 'banner media type must be image'
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)

