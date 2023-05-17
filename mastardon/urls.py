from django.contrib import admin
from django.urls import path
from page import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index_view'),
    path('ping/', views.ping_view, name='ping_view'),
    path('admin/', admin.site.urls),
]
