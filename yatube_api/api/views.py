from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import AccessPermission
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AccessPermission, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AccessPermission, IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        if Post.objects.filter(id=post_id).exists():
            new_queryset = Comment.objects.filter(
                post=get_object_or_404(Post, pk=post_id)
            )
            return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, post_id=self.kwargs.get("post_id")
        )
