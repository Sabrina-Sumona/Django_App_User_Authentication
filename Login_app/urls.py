from django.conf.urls import url
from django.urls import path
from Login_app import views

app_name = 'Login_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
]
