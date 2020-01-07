from django.contrib import admin
from comments.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created')
    list_filter = ('created', 'updated')
    search_fields = ('user', 'body')


admin.site.register(Comment, CommentAdmin)
