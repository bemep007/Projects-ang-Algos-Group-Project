from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),


    #Account page urls:
    # path(' n ', views.my_account),
    # path('my_account/<int:user_id>/update', views.update_account),
]