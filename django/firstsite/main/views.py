from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.

def index(responce):
    return HttpResponse("<h1> hey their</h1>")