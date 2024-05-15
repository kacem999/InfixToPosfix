from . import views
from django.urls import path

urlpatterns = [
    path('', views.Postfex_and_Arber, name="Home"),
    path('evaluation/', views.evaluation, name="eval"),
]
