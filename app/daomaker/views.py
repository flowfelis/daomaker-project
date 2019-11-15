from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView

from .models import Task

import requests
from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup


class ParseURLAjax(View):
    http_method_names = ['get', 'post']

    def http_method_not_allowed(self, request, *args, **kwargs):

        return HttpResponse(
            'Error: Method Not Allowed', status=405)

    def get(self, request, *args, **kwargs):

        return render(request, 'daomaker/index.html')

    def post(self, request, *args, **kwargs):

        # Get url from UI
        try:
            request_url = request.POST['url']
        except KeyError:
            return HttpResponse('Url field can not be empty')

        # Try getting metadata from response
        try:
            response = requests.get(request_url)
        except MissingSchema:
            return HttpResponse('Missing Schema(http or https)')
        except:
            return HttpResponse('Please enter a valid url')

        # Try finding the meta data
        soup = BeautifulSoup(response.text, 'html.parser')
        fields = ('title', 'description', 'url', 'site_name', 'image')
        try:
            findings = {field: soup.find(property="og:" + field).get('content')
                        for field in fields}
        except AttributeError:
            return HttpResponse('failed')
        else:
            # Save to DB
            Task.objects.create(
                parsed_url=findings['url'],
                title=findings['title'],
                description=findings['description'],
                site_name=findings['site_name'],
                image_url=findings['image']
            )

            return HttpResponse('success', status=201)


class GetData(ListView):
    http_method_names = ['get']

    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponse(
            'Error: Method Not Allowed', status=405)

    template_name = 'daomaker/show_data.html'
    queryset = Task.objects.all().order_by('-date')
    context_object_name = 'tasks'
