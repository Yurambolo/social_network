from django.contrib import admin
from .models import User, Post, Like

admin.site.register(User)
admin.site.register(Like)
admin.site.register(Post)
