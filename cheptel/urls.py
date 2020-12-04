from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('animal/new/', views.animal_new, name='animal_new'),
    path('animal/<str:pk>/edit/', views.animal_edit, name='animal_edit'),
    path('animal/<str:pk>/', views.animal_detail, name='animal_detail'),
    path('equipement/<str:pk>/', views.equip_detail, name='equip_detail'),
    path('animal/<str:pk>/nourrir', views.nourrir, name='nourrir'),
    path('animal/<str:pk>/divertir', views.divertir, name='divertir'),
    path('animal/<str:pk>/coucher', views.coucher, name='coucher'),
    path('animal/<str:pk>/reveiller', views.reveiller, name='reveiller'),
]