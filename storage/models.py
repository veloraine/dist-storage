from django.db import models

# Create your models here.
class File(models.Model):
    uploaded_file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

