from django.contrib import admin
from django.urls import path
from . import views




urlpatterns = [
    path('', views.index, name='index'),
    path('scrap/', views.scrape, name='scrape'), 
    path('search/', views.search_results, name='search_results'),
    path('formalsearch/', views.formalsearch, name='formalsearch'),
    path('about-us/', views.aboutus, name='about-us'),
    path('contact-us/', views.contactus, name='contact-us'),
    path('category/<str:category>/', views.category_view, name='category'),
]
