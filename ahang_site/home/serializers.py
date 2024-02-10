from rest_framework import serializers
from .models import SongPage, SubSong
from captcha.fields import CaptchaField


class SongHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongPage
        fields = ('title', 'slug', 'text', 'song', 'song_image', 'singer',)


class SearchSerializer(serializers.Serializer):
    search = serializers.CharField(max_length=40)


class YourTrySerializer(serializers.Serializer):
    video = serializers.FileField()


class ContactUsSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=20)
    subject = serializers.CharField(max_length=40)
    text = serializers.CharField(max_length=1000)


class SubSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSong
        fields = ('id', 'created', 'image_sub', 'user',)


class SingerSongSerialize(serializers.ModelSerializer):
    class Meta:
        model = SongPage
        fields = ('id', 'slug', 'song_image', 'created',)


class SongSerializer(serializers.ModelSerializer):
    related_song = serializers.SerializerMethodField()
    singer_song = serializers.SerializerMethodField()
    template_name = 'home/song.html'

    def get_singer_song(self, songpage):
        related_songs = SongPage.objects.none()
        for singer in songpage.singer.all():
            new_related_songs = related_songs | SongPage.objects.filter(
                singer__exact=singer).exclude(id=songpage.id).order_by('-created')[:5].only(
                'id', 'slug', 'song_image', 'created', )
            related_songs = new_related_songs
        serializer = SingerSongSerialize(instance=related_songs, many=True)
        return serializer.data

    def get_related_song(self, songpage):
        qs = SubSong.objects.filter(
            song_id=songpage.id, is_allowed=True).order_by('created').only(
            'id', 'created', 'user', 'image_sub', )
        serializer = SubSongSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = SongPage
        fields = '__all__'
