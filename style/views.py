from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.views.generic import ListView, DetailView

# Create your views here.


class StyleListView(ListView):
    model = models.Style
    template_name = "style/style.html"
    context_object_name='styles'
    ordering=['-created']