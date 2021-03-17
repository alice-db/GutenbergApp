from django.urls import path
from myImageEngine import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('myImageFromString/<str:name>/', views.ImageEngine.as_view()),
    path('myBook/<int:book_id>/image/<int:image_id>/', views.ImageBook.as_view()),
    path('myBook/<int:book_id>/image/', views.ImageRandom.as_view()),
    path('myBook/<int:book_id>/cover/', views.ImageCover.as_view()),
]
