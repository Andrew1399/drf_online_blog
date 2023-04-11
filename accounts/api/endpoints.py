from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from posts.api.permissions import IsOwnerOrReadOnly
from accounts.models import Profile
from accounts.api.serializers import (UserSerializer,
                                      UserRegistrationSerializer,
                                      ProfileUpdateSerializer,
                                      UserLoginSerializer,
                                      UserProfileSerializer)


class UserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username', 'profile__first_name']

    def get_queryset(self):
        queryset_list = User.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(username__icontains=query) |
                Q(profile__first_name__icontains=query)
            ).distinct()
        return queryset_list


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status_code': status_code,
            'message': 'User was created successfully'
        }
        return Response(response, status=status_code)


class UserLoginView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status': status_code,
            'message': 'You have successfully logged in.',
            'token': serializer.data['token']
        }
        return Response(response, status=status_code)


class ProfileListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['first_name', 'last_name', 'country', 'user__username']

    def get_queryset(self):
        queryset = Profile.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(country__icontains=query) |
                Q(user__username__icontains=query)
            ).distinct()
        return queryset


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()


class ProfileUpdateView(generics.UpdateAPIView):
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
