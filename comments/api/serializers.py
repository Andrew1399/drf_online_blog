from rest_framework import serializers
from django.contrib.auth.models import User
from comments.models import Comment
from posts.models import Post


class CommentSerializer(serializers.Serializer):
    user_qs = User.objects.all()
    posts_qs = Post.objects.all()
    user = serializers.PrimaryKeyRelatedField(queryset=user_qs)
    post = serializers.PrimaryKeyRelatedField(queryset=posts_qs)
    content = serializers.CharField(max_length=1000)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance