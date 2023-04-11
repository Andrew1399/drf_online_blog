from django.urls import path
from posts.api import endpoints

app_name = 'posts'

urlpatterns = [
    path('create/', endpoints.PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/', endpoints.PostRetrieveView.as_view(), name='post_detail'),
    path('<int:pk>/update/', endpoints.PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', endpoints.PostDestroyView.as_view(), name='post_delete'),
    path('', endpoints.PostListView.as_view(), name='post_list')
]
