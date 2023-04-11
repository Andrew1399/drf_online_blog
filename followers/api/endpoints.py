from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from followers.api.serializers import UserFollowingSerializer
from followers.models import Following
from accounts.models import Profile


class UserFollowingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = UserFollowingSerializer
    queryset = Following.objects.all()

    def follow(self, request, pk):
        own_profile = request.user.profile_set.first()
        following_profile = Profile.objects.get(id=pk)
        own_profile.following.add(following_profile)
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Now you are following.'
        }
        return Response(response, status=status.HTTP_200_OK)

    def unfollow(self, request, pk):
        own_profile = request.user.profile_set.first()
        following_profile = Profile.objects.get(id=pk)
        own_profile.following.remove(following_profile)
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'You are unfollow now.'
        }
        return Response(response, status=status.HTTP_200_OK)
