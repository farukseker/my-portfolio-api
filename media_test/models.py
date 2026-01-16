from django.db import models

class CloudinaryTest(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="test/")

    def __str__(self):
        return self.title
