from django.contrib import admin
from .models import *


# Register your models here.


class SingerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_editable = ['name', ]
    search_fields = ['name', ]


class ViewAdmin(admin.ModelAdmin):
    list_display = ['ip', 'created', ]
    list_filter = (
        ('created',
         )
    )


class SubSongAdmin(admin.ModelAdmin):
    list_display = ['id','song', 'user', 'is_allowed', ]
    list_editable = ['is_allowed', ]
    search_fields = ['user', 'song', ]
    list_filter = ['is_allowed','song',]
    readonly_fields = ('user', 'like', 'song',)

class SubSongInline(admin.TabularInline):
    model = SubSong
    readonly_fields = ('song', 'user', 'is_allowed', 'like', 'video',)


class SongPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'slug','song_image', ]
    list_editable = ['title', ]
    list_display_links = ['id']
    readonly_fields = ('view',)
    search_fields = ['title', 'singer']
    prepopulated_fields = {
        'slug': ('title',)
    }
    list_filter = (
        ('singer',
         )
    )
    inlines = [SubSongInline]


admin.site.register(SongPage, SongPageAdmin)
admin.site.register(SubSong, SubSongAdmin)
admin.site.register(Singer, SingerAdmin)
admin.site.register(View, ViewAdmin)
