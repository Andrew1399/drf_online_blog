from django.urls import path
from comments.api import endpoints

app_name = 'comments'

urlpatterns = [
    path('', endpoints.UserListCommentsView.as_view(), name='user_comments'),
    path('create/', endpoints.UserCreateCommentView.as_view(), name='comment_create'),
    path('comment/<int:pk>/', endpoints.CommentRetrieveView.as_view(), name='comment_detail'),
    path('comment/<int:pk>/update/', endpoints.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', endpoints.CommentDeleteView.as_view(), name='comment_delete')
]