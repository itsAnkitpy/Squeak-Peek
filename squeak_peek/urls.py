from django.contrib import admin
from django.urls import path,include

from posts.views import home, post_detail_view, post_list_view, post_create_view,post_delete_view,post_action_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('create-post',post_create_view),
    path('posts',post_list_view),
    path('posts/<int:post_id>',post_detail_view),
    # path('api/posts/<int:post_id>/delete',post_delete_view),
    # path('api/posts/action',post_action_view),
    path('api/posts/', include('posts.urls'))
]

