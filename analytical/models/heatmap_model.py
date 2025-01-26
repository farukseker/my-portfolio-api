from django.db import models


class HeatMapData(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    timestamp = models.DateTimeField()
    view = models.ForeignKey(
        'analytical.ViewModel',
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        editable=True
    )

    def __str__(self):
        return f"({self.x}, {self.y}) - {self.timestamp}"
