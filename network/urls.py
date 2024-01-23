from django.urls import path
from . import views


app_name = 'network'

urlpatterns = [
    path('', views.AllPostsView.as_view(), name="posts_list"),
    path('following/', views.FollowingPostsView.as_view(), name='following_posts_list'),
    path('post/', views.post_create, name='post_create'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:post_id>/like/', views.post_like_unlike, name='post_like_unlike'),
    path('post/<int:post_id>/unlike/', views.post_like_unlike, name='post_like_unlike'),
]