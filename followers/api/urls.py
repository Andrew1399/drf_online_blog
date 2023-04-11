from django.urls import path
from followers.api import endpoints


app_name = 'followers'

following_list = endpoints.UserFollowingViewSet.as_view({
    'get': 'list',
    # 'post': 'create'
})


urlpatterns = [
    path('', following_list, name='followers_list'),
    path('follow/<int:pk>/', endpoints.UserFollowingViewSet.as_view({'post': 'follow'})),
    path('unfollow/<int:pk>/', endpoints.UserFollowingViewSet.as_view({'post': 'unfollow'}))
]
