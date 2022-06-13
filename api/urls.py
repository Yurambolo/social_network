from django.urls import path, include
from rest_framework import routers

from .views import UserObtainTokenPairView, UserRegisterView, UserViewSet, PostViewSet, LikeViewSet, LikePostView, \
    UnlikePostView, CreatePostView, UserActivityView, UserAnalyticsView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = [
    path('login/', UserObtainTokenPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('login/verify/', TokenVerifyView.as_view()),
    path('register/', UserRegisterView.as_view()),
    path('posts/create/', CreatePostView.as_view()),
    path('posts/<int:post_id>/like/', LikePostView.as_view()),
    path('posts/<int:post_id>/unlike/', UnlikePostView.as_view()),
    path('users/<int:user_id>/activity/', UserActivityView.as_view()),
    path('users/<int:user_id>/analytics/', UserAnalyticsView.as_view()),
    path('rest/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]
