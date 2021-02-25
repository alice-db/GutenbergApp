from django.urls import path
from mygutenberg import views

urlpatterns = [
    path('books/', views.BooksList.as_view()),
    path('book/<int:pk>/', views.BookDetail.as_view()),
]
