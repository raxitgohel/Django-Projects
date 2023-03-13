import re
from django.db import models

# Create your models here.
class book(models.Model):
    bookID = models.TextField(unique=True)
    authorID = models.TextField()
    bookName = models.TextField()
    authorName = models.TextField()
    status = models.BooleanField()
    def __str__(self) -> str:
        return super().__str__()