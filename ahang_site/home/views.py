import datetime
import os.path
import subprocess
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from .models import SongPage, SubSong, View, Singer
from .form import MyTryForm
from enum import IntEnum
from django.core.mail import EmailMessage
from django.contrib import messages
import ffmpeg
from rest_framework.views import APIView
from rest_framework import generics, mixins
from .serializers import SongHomeSerializer, SearchSerializer, SongSerializer, YourTrySerializer, \
    ContactUsSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


class Chord(IntEnum):
    A = 0
    Bb = 1
    B = 2
    C = 3
    Db = 4
    D = 5
    Eb = 6
    E = 7
    F = 8
    Gb = 9
    G = 10
    Ab = 11


# Create your views here.
def pagination(page__, quantity, instances, ordering, radius):
    p = Paginator(instances.order_by(ordering), quantity)
    page_ = p.page(int(page__))
    return {'queries': page_, 'page': p, 'page_num': page__, 'radius': radius}


def authen(request):
    if not request.user.is_authenticated:
        messages.info(request, 'لطفا ابتدا وارد حساب کاربری خود شوید')
        return redirect('accounts:login')
    else:
        return "hi "


def view_(request):
    ip = request.META.get('REMOTE_ADDR')
    if not View.objects.filter(ip__exact=ip).exists():
        View.objects.create(ip=ip)
    return View.objects.count()


def home(request, page__num=1):
    songs = None
    if request.method == 'POST':
        search_ = request.POST.get('search')
        if search_ is not None:
            songs = SongPage.objects.filter(title__icontains=search_).order_by('queried')
            singers = Singer.objects.filter(name__icontains=search_)
            for singer in singers:
                songs_2 = singer.related_singer.all()
                songs = songs | songs_2
    else:
        view_(request)
        songs = SongPage.objects.all()
    context = pagination(page__num, 2, songs, '-title', 2)
    return render(request, 'home/home.html', context)


# regen Api View
# class HomeAPI(APIView, PageNumberPagination):
#     def get(self, request: Request):
#         view_(request)
#         songs = SongPage.objects.all()
#         songs = self.paginate_queryset(songs, request, )
#         songserializer = SongHomeSerializer(songs, many=True)
#         return self.get_paginated_response(songserializer.data)
#
#     def post(self, request: Request, page__num=1):
#         serializer = SearchSerializer(data=request.data)
#         if serializer.is_valid():
#             search_ = serializer.data['search']
#             if search_ is not None:
#                 songs = SongPage.objects.filter(title__icontains=search_).order_by('-title')
#                 singers = Singer.objects.filter(name__icontains=search_)
#                 for singer in singers:
#                     songs_2 = singer.related_singer.all()
#                     songs = songs | songs_2
#                 songs = songs.only
#                 songs = self.paginate_queryset(songs, request, )
#                 songserializer = SongHomeSerializer(songs, many=True)
#                 return self.get_paginated_response(songserializer.data)
#         else:
#             return self.get(request)

# i couldnt check captcha because it didnt show me correctly
def song(request, slug, id):
    if request.method == 'POST':
        authen(request)
        form = MyTryForm(request.POST, request.FILES)
        if form.is_valid():
            human = True
            data = form.cleaned_data
            x = SubSong.objects.create(song_id=id,
                                       user_id=request.user.id,
                                       video=data['video'], )
            path = x.video.name
            filename = '/' + x.song.slug + '.'
            out = path.replace('sub_video/', 'sub_songs/').replace('mp4', 'jpg').replace(r'/*.', filename)
            # create file sub song in deploying add ffmpeg.exe to python path and install ffmpeg_python
            (
                ffmpeg.input('media/' + path, ss='00:00:50').filter(
                    'thumbnail').filter('scale', 180, -1).output('media/' + out, vframes=1).run())
            x.image_sub = out
            x.save()
            messages.success(request, 'ویدیوی شما با موفقیت ارسال شد ، پس از بررسی منتشر خواهد شد')
            return redirect(request.META.get('HTTP_REFERER'))

        else:
            messages.error(request, 'ویدیوی شما بارگداری نشد')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        view_(request)
        song_ = SongPage.objects.filter(id=id, slug=slug)
        if song_.exists():
            song_ = SongPage.objects.get(id=id, slug=slug)
            song_.view += 1
            song_.save()
            form = MyTryForm()
            sub_songs = SubSong.objects.filter(song_id=id, is_allowed=True).order_by('created')
            related_songs = set()
            for singer in song_.singer.all():
                related_songs.add(
                    SongPage.objects.filter(singer__exact=singer).exclude(id=id).order_by('-created')[:5])
            context = {'form': form, 'sub_songs': sub_songs, 'song': song_, 'related_songs': related_songs}
            return render(request, 'home/song.html', context)
        else:
            return redirect(request.META.get('HTTP_REFERER'))


# class SongAPI(APIView, PageNumberPagination):
#     def post(self, request, slug, id):
#         # CHECK AUTHNTICATION
#
#         if SongPage.objects.filter(id=id, slug=slug).exists():
#             serializer = YourTrySerializer(data=request.data)
#             if serializer.is_valid() :
#                 x = SubSong.objects.create(song_id=id,
#                                            user_id=self.request.user.id, # check user id in real api
#                                            video=request.FILES['video'], )
#                 path = x.video.name
#                 filename = '/' + x.song.slug + '.'
#                 out = path.replace('sub_video/', 'sub_songs/').replace('mp4', 'jpg').replace(r'/*.', filename)
#                 # create file sub song in deploying add ffmpeg.exe to python path and install ffmpeg_python
#                 (
#                     ffmpeg.input('media/' + path, ss='00:00:50').filter(
#                         'thumbnail').filter('scale', 180, -1).output('media/' + out, vframes=1).run())
#                 x.image_sub = out
#                 x.save()
#                 return Response(serializer.data, status.HTTP_200_OK)
#             else:
#                 return HttpResponse(serializer.data,status.HTTP_400_BAD_REQUEST)
#
#     def get(self, request, slug, id):
#         view_(request)
#         song_ = SongPage.objects.filter(id=id, slug=slug)
#         if song_.exists():
#             song_ = SongPage.objects.get(id=id, slug=slug)
#             song_.view += 1
#             song_.save()
#         form = MyTryForm()
#         serializer = SongSerializer(song_, context={'request': request, 'form': form, }, many=False)
#         return Response(serializer.data, status.HTTP_200_OK)

# call this with javascript and return a message
def like_sub(request, id):
    url = request.META.get('HTTP_REFERER')
    authen(request)
    if SubSong.objects.filter(id=id).exists():
        sub = SubSong.objects.get(id=id)
        sub.like.add(request.user)
        sub.save()
        message = 'success'
    return redirect(url)


def send_email_to_me(sub, contain, email):
    contain += '\n' + 'from : ' + email
    sus = EmailMessage(
        sub,
        contain,
        email,
        ('desprdo.kolbe@gmail.com',),
    )
    sus.send(fail_silently=False)  # you should change before deploy


def contact_us(request):
    if request.method == 'GET':
        return render(request, 'home/contact_us.html')
    if request.method == 'POST':
        sub = request.POST.get('subject')
        email = request.POST.get('email')
        contain = request.POST.get('contain')
        send_email_to_me(sub, contain, email)
        messages.success(request, 'درخواست شما با موفقیت ارسال شد')
        return redirect('topic:main')


# class ContactUsApi(APIView):
#     def post(self, request):
#         serializer = ContactUsSerializer(data=request.data)
#         if serializer.is_valid():
#             send_email_to_me(serializer.data['subject'], serializer.data['text'], serializer.data['email'])
#             return Response(serializer.data, status.HTTP_200_OK)
#         else:
#             return Response(None, status.HTTP_400_BAD_REQUEST)


# send 'choice_key' and 'assumed_key' and 'list_chords' as dictionary and resieve th context with javascript
def new_chords(request, **kwargs):
    chords = []
    difference = Chord[kwargs['choice_key']].value - Chord[kwargs['assumed_key']].value
    for arg in kwargs['list_chords']:
        new_num = (Chord[arg].value + difference + 12) % 12
        new_chord = Chord(new_num).name
        chords.append(new_chord)
    context = {'choice_key': kwargs['choice_key'], 'list_chords': chords}
    return JsonResponse(context)
