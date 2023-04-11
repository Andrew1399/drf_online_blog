from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from posts.models import Post
from posts.api.serializers import PostSerializer
from posts.api.pagination import PostPageNumberPagination
from posts.api.permissions import IsOwnerOrReadOnly


class PostCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostUpdateView(generics.UpdateAPIView):
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDestroyView(generics.DestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (AllowAny, )
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['title', 'content', 'user__first_name', 'user__last_name']
    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontaince=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return queryset_list
