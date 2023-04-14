from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('hello', views.hello, name='hello'),
    path('sum', views.sum, name='sum'),
    path('form', views.form, name='form'),
    path('', views.form, name='form'),
    path('download/', views.download_file, name='download_file'),
    path('limpar/', views.limpar_campos, name='limpar_campos'),
    path('json/', views.download_json, name='download_json'),
    path('upload/', views.upload_json, name='upload_json')
]


