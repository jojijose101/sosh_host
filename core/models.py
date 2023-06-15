from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime



# Create your models here.
user = get_user_model()

class profile(models.Model):
    firstnm = models.CharField(blank=True, max_length=100)
    lastnm = models.CharField(blank=True, max_length=100)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    email = models.TextField(max_length=100, blank=True)
    profileimg = models.ImageField(upload_to="profile_image", default='user-6380868_1280.webp')
    location = models.CharField(max_length=100,)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to="post_image")
    caption = models.TextField()
    created_at =models.DateTimeField(default=datetime.now)
    no_of_like = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    def __str__(self):
        return self.username

class FollowerCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    def __str__(self):
        return self.user
    
    
    
    
    