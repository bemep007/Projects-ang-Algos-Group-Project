from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('create_account', views.create_account),
    path('login', views.login),
    path('dashboard', views.dashboard),
    # # account edit portion
    path('my_account/<int:user_id>', views.my_account),
    path('my_account/<int:user_id>/update', views.update_account),
]