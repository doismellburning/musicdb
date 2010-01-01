from django.contrib import admin

from musicdb.nonclassical import models

class ArtistAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'is_solo_artist')}
        ),
        (None, {
            'fields': ('nationality',)}
        ),
    )
    search_fields = ('name',)
admin.site.register(models.Artist, ArtistAdmin)

class AlbumAdmin(admin.ModelAdmin):
    fields = ('title', 'artist', 'year', 'cover')
    search_fields = ('title',)
    raw_id_fields = ('artist',)
admin.site.register(models.Album, AlbumAdmin)

class CDAdmin(admin.ModelAdmin):
    fields = ('album', 'num')
    raw_id_fields = ('album',)
admin.site.register(models.CD, CDAdmin)

class TrackAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'num')}
        ),
        (None, {
            'fields': ('cd',)}
        ),
    )
    raw_id_fields = ('cd',)
    search_fields = ('title',)
admin.site.register(models.Track, TrackAdmin)
