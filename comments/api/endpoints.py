from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostPageNumberPagination
from comments.models import Comment
from comments.api.serializers import CommentSerializer


class CommentRetrieveView(APIView):
    permission_classes = (IsOwnerOrReadOnly, )

    def get(self, request, pk, format=None):
        comment = Comment.objects.get(id=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


class CommentUpdateView(APIView):
    permission_classes = (IsOwnerOrReadOnly, )

    def put(self, request, pk, format=None):
        comment = Comment.objects.get(id=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': 'True',
                'status_code': status.HTTP_200_OK,
                'message': 'Your comment was updated successfully.',
                'data': serializer.data
            }
            return Response(response)
        else:
            response = {
                'success': 'False',
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Comment was not updated.',
                'error': serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteView(APIView):
    permission_classes = (IsOwnerOrReadOnly, )

    def delete(self, request, pk, format=None):
        comment = Comment.objects.get(id=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListCommentsView(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = CommentSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    pagination_class = PostPageNumberPagination
    search_fields = ['content', 'user__first_name', 'user__last_name']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.filter(id__gte=0)
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return queryset_list


class UserCreateCommentView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': 'True',
                'status_code': status.HTTP_201_CREATED,
                'message': 'You have successfully commented a post.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                'success': 'False',
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Your comment was not created.',
                'error': serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
