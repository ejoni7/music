from django.db import models
from accounts.models import User
from django.urls import reverse
from django_jalali.db import models as jmodels
from ckeditor_uploader.fields import RichTextUploadingField
from sorl.thumbnail import ImageField as ThumbImage

CHORDS = (
    ('A', 'A'),
    ('Bb', 'Bb'),
    ('B', 'B'),
    ('C', 'C'),
    ('Db', 'Db'),
    ('D', 'D'),
    ('Eb', 'Eb'),
    ('E', 'E'),
    ('F', 'F'),
    ('Gb', 'Gb'),
    ('G', 'G'),
    ('Ab', 'Ab'),
)


# Create your models here.
class Singer(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class SongPage(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(allow_unicode=True)
    created = jmodels.jDateField(auto_now_add=True)
    assumed_chord = models.CharField(choices=CHORDS, max_length=2)
    text = RichTextUploadingField()
    song = models.FileField(upload_to='mp3/', blank=True, null=True)
    song_image = models.ImageField(upload_to='song_pic', blank=True)
    singer = models.ManyToManyField(Singer, related_name='related_singer')
    view = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('home:song', args=[self.slug, self.id])

    def __str__(self):
        return self.title


class View(models.Model):
    ip = models.CharField(max_length=30)
    created = jmodels.jDateTimeField(auto_now_add=True)


class SubSong(models.Model):
    song = models.ForeignKey(SongPage, on_delete=models.CASCADE, related_name='related_song')
    created = jmodels.jDateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='related_user')
    video = models.FileField(upload_to='sub_video/', )
    like = models.ManyToManyField(User, blank=True, )
    is_allowed = models.BooleanField(default=False)
    image_sub = ThumbImage(upload_to='sub_songs/', default='1.jpg')

    def __str__(self):
        return self.song.title + str(self.user)

    def get_total_like(self):
        return self.like.count()
