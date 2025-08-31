from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    # if you want Cloudinary later:
    # cover = models.ImageField(upload_to='books/', blank=True, null=True)

    def __str__(self):
        return self.title
