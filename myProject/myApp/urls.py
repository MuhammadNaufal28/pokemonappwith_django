from . import views
from django.urls import path
from django.contrib import admin
from myApp import views


urlpatterns = [
    path("", views.home, name="home"),
    path('admin/', admin.site.urls),
    path('', views.pokemon_search, name='pokemon_search'),
    path('pokemon/<str:name>/', views.pokemon_detail, name='pokemon_detail'),
    path('ability/<str:ability_name>/', views.ability_detail, name='ability_detail'),
    path('gatcha/', views.gatcha, name='gatcha'),
    path('gatcha/gatcha_result/', views.gatcha_result, name='gatcha_result'),
    path('translate/<str:ability_name>/', views.translate_ability_effect, name='translate_ability_effect'),
]