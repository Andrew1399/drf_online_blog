from django.contrib.auth import get_user_model
from rest_framework import serializers
from followers.models import Following


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ('id', 'following_user_id', 'created')


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ('id', 'user_id', 'created')


class UserFollowingSerializer(serializers.ModelSerializer):
    user_id = FollowingSerializer
    following_user_id = FollowersSerializer

    class Meta:
        model = Following
        fields = ('following_user_id', 'user_id', 'created')

