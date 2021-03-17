from django.urls import path
from mygutenberg import views

urlpatterns = [
    path('books/', views.RedirectionListeDesLivres.as_view()),
    path('book/<int:pk>/', views.LivreDetail.as_view()),
    path('book/<int:pk>/image', views.LivreImageRandomDetail.as_view()),
    path('book/<int:pk>/coverImage', views.LivreCoverImageDetail.as_view()),
    path('book/<int:pk>/image/<int:ipk>', views.LivreImageDetail.as_view()),
    path('frenchbooks/', views.LivresEnFrancaisList.as_view()),
    path('frenchbook/<int:pk>/', views.LivreEnFrancaisDetail.as_view()),
    path('englishbooks/', views.LivresEnAnglaisList.as_view()),
    path('englishbooks/<int:pk>/', views.LivreEnAnglaisDetail.as_view()),
]
