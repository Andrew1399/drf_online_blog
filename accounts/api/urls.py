from django.urls import path
from accounts.api import endpoints

app_name = 'accounts'

urlpatterns = [
    path('', endpoints.UserListView.as_view(), name='user_list'),
    path('<int:pk>/', endpoints.UserDetailView.as_view(), name='user_detail'),
    path('signup/', endpoints.UserRegistrationView.as_view(), name='signup'),
    path('login/', endpoints.UserLoginView.as_view(), name='login'),
    path('profiles/', endpoints.ProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>/update/', endpoints.ProfileUpdateView.as_view(), name='profile_update'),
    path('profiles/get/<int:pk>/', endpoints.UserProfileView.as_view(), name='user_profile')
]
