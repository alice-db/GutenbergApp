from django.urls import path
from mygutenberg import views

urlpatterns = [
    path('books/', views.RedirectionListeDesLivres.as_view()),
    path('book/<int:pk>/', views.LivreDetail.as_view()),
    path('book_regex/<str:regex>/', views.RechercheRegEx.as_view()),
    path('book_simple/<str:regex>/', views.RechercheSimple.as_view())
]
