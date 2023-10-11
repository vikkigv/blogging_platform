from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from core.serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django_filters.rest_framework import DjangoFilterBackend

class LoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            print(user, token)
            login(request, user)
            return Response({'token': token.key})
        else:
            return Response({'message': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):

    def post(self, request, format=None):
        self.request.user.auth_token.delete()
        message = {'message': 'User logged out successfully'}
        return Response(message, status=status.HTTP_200_OK)

class BlogListApiView(generics.ListAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author_id']

class BlogCreateApiView(APIView):
    serializer_class = BlogSerializer

    def post(self, request):
        data = request.data
        print(data, self.request.user, type(self.request.user))
        data['author_id'] = self.request.user.id
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    # def get_queryset(self):
    #     user = self.request.user
    #     return user.blog_set.all()


class BlogUpdateDeleteApiView(APIView):
    serializer_class = BlogSerializer

    def put(self, request, pk):
        user = self.request.user
        data = request.data
        data.pop('comments', None)

        try:
            blog_obj = Blog.objects.get(id=pk)
        except:
            return Response({'message': 'No Blog Found'}, status=status.HTTP_400_BAD_REQUEST)

        if user.id != blog_obj.author_id.id:
            return Response({'message': "You don't have access to edit this blog"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BlogSerializer(blog_obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Blog Updated!'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            blog_obj = Blog.objects.get(id=pk)
            blog_obj.delete()
            return Response({'message': 'Blog Deleted'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'No Blog Found'}, status=status.HTTP_400_BAD_REQUEST)


class BlogCommentsCreateApiView(APIView):
    serializer_class = BlogCommentsSerializer

    def post(self, request):
        data = request.data
        data['user_id'] = self.request.user.id
        serializer = BlogCommentsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Comment created!'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)