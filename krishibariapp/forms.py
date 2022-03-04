from cProfile import label
from dataclasses import field, fields
import imp
from pyexpat import model
from tkinter import Widget
from turtle import title
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import strawbarryVideoTable
from .models import *
from ckeditor.widgets import CKEditorWidget


class Video_form(forms.ModelForm):
    class Meta:
        model=strawbarryVideoTable
        fields= "__all__"
        # caption=forms.CharField()
        # caption.widget.attrs.update({'class':'form-control'})
        # video= forms.FileField()
        # video.widget.attrs.update({'class':'form-control-file'})
        # is_paid=forms.BooleanField()
        # is_paid.widget.attrs.update({'class':'form-check-input'})

class course_add(forms.ModelForm):
    class Meta:
        model=coursesList
        fields="__all__"
class video_add(forms.ModelForm):
    class Meta:
        model=allCourseVideos
        fields="__all__"
class add_post(forms.Form):
    title=forms.CharField(label='Title', max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    # auther= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'hidden','value':'','id':'authorid'}))
    article=forms.CharField(widget = CKEditorWidget())   
