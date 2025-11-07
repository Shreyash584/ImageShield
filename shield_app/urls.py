from django.urls import path
from . import views

app_name = 'shield_app'  # <<< This is crucial!

urlpatterns = [
    path('', views.index, name='index'),
    path('encrypt/', views.encrypt_image, name='encrypt'),
    path('decrypt/', views.decrypt_image, name='decrypt'),
]
