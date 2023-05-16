from django.db import models
from solo.models import SingletonModel
from storage.constants import Role


class File(models.Model):
    uploaded_file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uploaded_file.name}, {self.id}"


class CurrentTerm(SingletonModel):
    value = models.IntegerField(default=0)


class VotedFor(SingletonModel):
    value = models.CharField(max_length=100, default=None, null=True)


class CommitLength(SingletonModel):
    value = models.IntegerField(default=0)


class Log(models.Model):
    term = models.IntegerField()
    file_blob = models.BinaryField()
    file_id = models.IntegerField()
    file_name = models.CharField(max_length=30)
