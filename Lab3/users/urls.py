from django.urls import path
from .views import *

urlpatterns = [
    path('login/', SignInView.as_view(), name='login'),
    path('register/', SignUpView.as_view(), name='register'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('user-profile/', ProfileView.as_view(), name='user_profile')
]
