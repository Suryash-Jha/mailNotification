from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('api/', views.callApi, name="api"),
    path('clientApi/', views.clientApi, name="clientApi"),


]
