from django.db import models


class TagCategoryModel(models.Model):
    name = models.CharField(max_length=50, default=None)
    tags = models.ManyToManyField('TagModel', blank=True)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.name)


class TagModel(models.Model):
    category = models.ForeignKey('TagCategoryModel', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, default='')

    class IconType(models.TextChoices):
        FONT_AWESOME = "1", "FA"
        IMAGE = '2', 'image'
        NONE = '3', 'None'

    icon_type = models.CharField(
        max_length=1,
        choices=IconType.choices,
        default=IconType.NONE
    )
    icon = models.TextField(help_text='when call (fa/src) use this refs', default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.name}@{self.category.name if self.category else None}'
