from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from ckeditor.fields import RichTextField

from django.db.models.signals import pre_save
from django.utils.text import slugify 

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, max_length=250, null=True, blank=True)
    timeStamp = models.DateField(auto_now_add=True, blank=True)
    content = RichTextField(blank=True, null=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title + " by " + self.author

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)
    replytimestamp = models.DateTimeField(default=now)
    def __str__(self):
        return self.comment[0:100] + "..." + " by " + self.user.username

