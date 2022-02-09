from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from django.db import transaction
from dj_rest_auth.registration.serializers import RegisterSerializer
from doctor.models import Doctor


class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=30)

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.phone = self.data.get('phone')
        user.name = self.data.get('name')
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = ['email', 'phone', 'address', 'image', 'about', ]


class CurrentUserView(APIView):
    """
    Return User info
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # there is no use of self, just to ignore the static warning.
        _ = self
        qs = Doctor.objects.filter(id=request.user.id)
        serializer = CustomRegisterSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
