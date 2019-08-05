""" Users Urls """

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
# from .views import UserLoginAPIView, UserSignUpAPIView, AccountVerificationAPIView
from .views import users as user_views

router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')

urlpatterns = [
    # path('users/login/', UserLoginAPIView.as_view(), name='login'),
    # path('users/signup/', UserSignUpAPIView.as_view(), name='signup'),
    # path('users/verify/', AccountVerificationAPIView.as_view(), name='verify'),
    path('', include(router.urls))
]
