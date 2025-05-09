from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'watched', 'is_published', 'category', 'created_at', 'updated_at', 'get_photo_image')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    readonly_fields = ('watched',)
    list_filter = ('is_published', 'category', 'watched',)

    def get_photo_image(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="60">')
        return "-"

    get_photo_image.short_description = 'Изображение поста'


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
