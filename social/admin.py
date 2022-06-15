from django.contrib import admin
from .models import Post, userProfile, Comment

admin.site.register(Post)
admin.site.register(userProfile)
admin.site.register(Comment)
