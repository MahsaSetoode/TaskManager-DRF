from django.shortcuts import render
from django.views import View
from django.conf import settings
from rest_framework.views import APIView
from django.views.generic import TemplateView


class HomeView(APIView):
    template = 'home/main.html'
    def get(self, request):
        return render(request, self.template)