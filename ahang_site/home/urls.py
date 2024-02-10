from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('home_api/', views.HomeAPI.as_view(), name='home_api'),
    path('contact_us_api/', views.ContactUsApi.as_view(), name='contact_us_api'),
    path('song_api/<slug>/<int:id>/', views.SongAPI.as_view(), name='song_api'),
    path('<int:page__num>/', views.home, name='home'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('new_chords/', views.new_chords, name='new_chords'),
    path('like_sub/<int:id>/', views.like_sub, name='like_sub'),
    path('song/<slug>/<int:id>/', views.song, name='song'),
]
