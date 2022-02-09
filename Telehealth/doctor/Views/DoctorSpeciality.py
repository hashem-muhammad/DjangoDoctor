from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers

from doctor.models import DoctorSpeciality, Speciality


class SpecialitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Speciality
        fields = ['id', 'name', ]


class DoctorSpecialitySerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorSpeciality
        fields = ['id', 'speciality', ]


class DoctorSpecialityListSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(read_only=True, source='doctor.name')
    speciality = serializers.CharField(
        read_only=True, source='speciality.name')

    class Meta:
        model = DoctorSpeciality
        fields = ['id', 'doctor', 'speciality', ]


class DoctorSpecialityView(APIView):
    """
    In GET request will show all Speciality availiable to choise
    In POST request will add Speciality to doctor
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        qs = Speciality.objects.all()
        serializer = SpecialitySerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        serializer = DoctorSpecialitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(doctor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)


class DoctorSpecialityListView(APIView):
    """
    show all doctors in System with speciality
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        qs = DoctorSpeciality.objects.select_related(
            'doctor', 'speciality').all()
        serializer = DoctorSpecialityListSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
