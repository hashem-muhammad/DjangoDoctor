from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers

from doctor.models import DoctorInsurance, Insurance


class InsuranceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Insurance
        fields = ['id', 'company', ]


class DoctorInsuranceSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(read_only=True)

    class Meta:
        model = DoctorInsurance
        fields = ['id', 'doctor', 'insurance', 'insurance_number', ]


class DoctorInsuranceView(APIView):
    """
    GET all Insurance Company to choise
    POST to save doctor with company name and insurance_number
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        qs = Insurance.objects.all()
        serializer = InsuranceSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DoctorInsuranceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(doctor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)
