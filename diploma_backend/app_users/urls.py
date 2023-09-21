from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from rest_framework import routers

from app_users.views import UserViewSet, PasswordUpdateView, AvatarUpdateView, PaymentView

app_name = 'app_users'

urlpatterns = [
    path('profile', UserViewSet.as_view(), name='profile'),
    path('profile/password', PasswordUpdateView.as_view(), name='post_profile_password'),
    path('profile/avatar', AvatarUpdateView.as_view(), name='post_profile_avatar'),
    path('payment', PaymentView.as_view(), name='post_payment'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

