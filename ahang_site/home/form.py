from captcha.fields import CaptchaField
from django import forms
from .models import SubSong


class MyTryForm(forms.ModelForm):
    captcha=CaptchaField()
    class Meta:
        model = SubSong
        fields = ['video', ]
        required=('video',)


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50)
