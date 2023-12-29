from django.contrib import admin
from .models import Post, Comment, ServerInformation, User

# Register your models here.


admin.site.register(Post)
admin.site.register(Comment)

admin.site.register(User)
admin.site.register(ServerInformation)
