from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),

    path('posts/<int:post_id>/',
         views.PostDetailPage.as_view(),
         name='post_detail'
         ),

    path('category/<slug:category>/',
         views.CategoryPostsListView.as_view(),
         name='category_posts'
         )
]
