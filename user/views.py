from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.
class IndexClass(View):
    def get(self, request):
        return HttpResponse("Hello World")
