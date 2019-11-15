from django.urls import path

from . import views

urlpatterns = [
    path('', views.ParseURLAjax.as_view(), name='parse_url_ajax'),
    path('show-data', views.GetData.as_view(), name='show_data')
]
