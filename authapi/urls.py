from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views


urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('generateOTP/', views.generateOTPForNumber, name='generate-otp'),
    path('verifyOTP/', views.verifyOTP, name='verify-otp'),
    path('registerUser/', views.registerUser, name='register-user'),
    path('token/', views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', views.dummyProtectedView, name='dummy-protected-view'),
    path('logout/', views.LogoutView.as_view(), name='auth_logout')
]