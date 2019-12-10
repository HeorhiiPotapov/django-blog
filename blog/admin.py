from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    # show all this fields in one string
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    # add filters to the right side
    list_filter = ('status', 'created', 'publish', 'author')
    # search for the current fields
    search_fields = ('title', 'body')
    # when typing in title field, slug field weel adding automaticaly
    prepopulated_fields = {'slug': ('title',)}
    # when add new post can find author by id
    row_id_fields = ('author',)
    # makes pusible show post by date_hierarchy, plased under search field
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(Comment, CommentAdmin)
