from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from socialnetwork.models import Post
from socialnetwork.serializers import UserSerializer, PostSerializer
from socialnetwork.services import get_user_additional_data


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        additional_data = get_user_additional_data(email)
        serializer.save(
            first_name=additional_data['first_name'],
            last_name=additional_data['last_name']
        )


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    @detail_route(methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()

        post.number_of_likes += 1
        post.save()

        return Response({'succes': True})

    @detail_route(methods=['post'])
    def unlike(self, request, pk=None):
        """In this method, if client is trying to unlike post with 0 likes,
        we're returning success False with HTTP 200 OK, and thus only informing client
        that the request has failed, without returning HTTP error code
        """
        post = self.get_object()

        if post.number_of_likes <= 0:
            return Response({'success': False})

        post.number_of_likes -= 1
        post.save()

        return Response({'success': True})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
