from django import forms
from django.contrib.auth.models import User
from .models import Articolo, Simple_str
from django.db import models

class PostForm(forms.ModelForm):

    class Meta:
        model = Articolo
        fields = ('title', 'text',)

class CreateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ReportForm(forms.ModelForm):

    class Meta:
        model = Simple_str
        fields = ('key',)
