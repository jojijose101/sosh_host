from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.profile)
admin.site.register(models.Post)
admin.site.register(models.LikePost)
admin.site.register(models.FollowerCount)