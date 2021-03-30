from django.urls import path
from mygutenberg import views

urlpatterns = [
	path('books/', views.RedirectionListeDesLivres.as_view()),
	path('book/<int:pk>/', views.LivreDetail.as_view()),
	#path('book/<string:term>/', views.LivreDetail.as_view())
]
