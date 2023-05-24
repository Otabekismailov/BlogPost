from django.contrib import admin

from blog.models import Post, Tag, Category, Comment, LikeDislike


# Register your models here.
class Postadmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'author', 'pub_year']


admin.site.register(Post, Postadmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(LikeDislike)
