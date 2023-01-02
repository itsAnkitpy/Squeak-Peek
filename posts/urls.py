from django.contrib import admin
from django.urls import path

from .views import home, post_detail_view, post_list_view, post_create_view,post_delete_view,post_action_view

urlpatterns = [
    path('',post_list_view),
    path('action/',post_action_view),
    path('create/',post_create_view),
    path('<int:post_id>/',post_detail_view),
    path('<int:post_id>/delete/',post_delete_view),
    
]

