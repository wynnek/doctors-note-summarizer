from django.db import models

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/")
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title