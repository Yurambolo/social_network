from datetime import datetime

from django.db.models.functions import TruncDate
from django.db.models import Count
from rest_framework import generics, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .exceptions import LikeError
from .models import User, Post, Like
from .serializers import UserTokenObtainPairSerializer, UserRegisterSerializer, UserSerializer, PostSerializer, \
    LikeSerializer


class UserObtainTokenPairView(TokenObtainPairView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAdminUser]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAdminUser]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAdminUser]


class CreatePostView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            data = request.data
            data['author_id'] = request.user.id
            post = PostSerializer().create(request.data)
            post.save()
            return Response(status=201)
        except Exception as e:
            raise APIException(e)


class LikePostView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, post_id=None):
        try:
            if not Post.objects.filter(id=post_id).exists():
                raise LikeError("Post does not exist")
            like = Like.objects.filter(post_id=post_id, user_id=request.user.id).first()
            if like:
                raise LikeError("Post already liked")
            like = Like(user_id=request.user.id, post_id=post_id)
            like.save()
            return Response()
        except Exception as e:
            raise APIException(e)


class UnlikePostView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, post_id=None):
        try:
            if not Post.objects.filter(id=post_id).exists():
                raise LikeError("Post does not exist")
            like = Like.objects.filter(post_id=post_id, user_id=request.user.id).first()
            if not like:
                raise LikeError("Post is not liked")
            like.delete()
            return Response()
        except Exception as e:
            raise APIException(e)


class UserActivityView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, format=None, user_id=None):
        try:
            user = User.objects.filter(id=user_id).first()
            data = dict(last_login=user.last_login, last_activity=user.last_activity)
            return Response(data)
        except Exception as e:
            raise APIException(e)


class UserAnalyticsView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, format=None, user_id=None):
        try:
            likes = Like.objects.filter(user_id=user_id)
            date_from = request.GET.get("date_from", None)
            if date_from:
                date_from = datetime.strptime(date_from, '%d/%m/%Y')
                likes = likes.filter(created_at__gte=date_from)
            date_to = request.GET.get("date_to", None)
            if date_to:
                date_to = datetime.strptime(date_to, '%d/%m/%Y')
                likes = likes.filter(created_at__lte=date_to)
            data = likes.annotate(date=TruncDate('created_at')).values('date').annotate(likes=Count('id')).values(
                'date', 'likes')
            return Response(data)
        except Exception as e:
            raise APIException(e)
