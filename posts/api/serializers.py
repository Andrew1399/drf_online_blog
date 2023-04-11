from django.contrib.auth.models import User
from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    read_time = serializers.IntegerField(default=0)
    liked = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'user', 'read_time', 'liked', 'created', 'updated']

    def update(self, instance, validated_data):
        liked = validated_data.pop('liked')
        for i in liked:
            instance.liked.add(i)
        instance.save()
        return instance
