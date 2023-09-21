from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from app_users.models import UserProfile, Payments
from app_users.serializers import UserSerializer, UpdatePasswordSerializer, AvatarUpdateSerializer, PaymentSerializer


class UserViewSet(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser, )
    serializer_class = UserSerializer
    parser_classes = [JSONParser]

    def check_profile(self):
        if not UserProfile.objects.filter(user=self.request.user).exists():
            UserProfile.objects.create(user=self.request.user)

    def get_data(self):
        self.check_profile()
        profile = UserProfile.objects.get(user=self.request.user)
        return {
            'fullName': self.request.user.get_full_name(),
            'email': self.request.user.email,
            'phone': profile.phone,
            'avatar': profile.avatar}

    def get(self, request, *args, **kwargs):
        data = self.get_data()
        serializer = self.serializer_class(data)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user=request.user)
        instance = self.get_data()
        data = request.data
        serializer = self.serializer_class(instance=instance,
                                           data=data,
                                           partial=True)
        if serializer.is_valid():
            user.first_name, user.last_name = data['fullName'].split()
            user.email = data['email']
            profile.phone = data['phone']
            profile.avatar = data['avatar']
            user.save()
            profile.save()
        return Response(serializer.data)


class PasswordUpdateView(APIView):
    serializer_class = UpdatePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated, IsAdminUser,)
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        customer = request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            customer.set_password(serializer.data['password'])
            customer.save()
            update_session_auth_hash(request, customer)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvatarUpdateView(APIView):
    serializer_class = AvatarUpdateSerializer
    model = UserProfile
    permission_classes = (IsAuthenticated, IsAdminUser,)
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(user=request.user)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            profile.avatar = serializer.data['url']
            profile.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentView(APIView):
    serializer_class = PaymentSerializer
    model = Payments
    permission_classes = (IsAuthenticated, )
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, title='Первая попавшаяся')
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
