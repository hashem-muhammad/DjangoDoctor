from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers

from doctor.models import Consultation


class ConsultationSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(read_only=True)

    class Meta:
        model = Consultation
        fields = ['id', 'doctor', 'type', 'price', ]


class ConsultationView(APIView):
    """
    add Consultation to doctor in POST request and check if exists
    if exists you can update it in PATCH request
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, type):
        _ = self
        try:
            return Consultation.objects.get(type=type)
        except Consultation.DoseNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):

        serializer = ConsultationSerializer(data=request.data)

        if serializer.is_valid():
            valid_data = serializer.validated_data
            type = valid_data['type']
            price = valid_data['price']
            qs = Consultation.objects.filter(
                doctor=request.user, type=type).exists()

            if qs:
                ObjectExists = {'status': 403,
                                'message': 'ObjectExists you can update it!'}
                return Response(ObjectExists, status=status.HTTP_403_FORBIDDEN)
            else:
                Consultation.objects.bulk_create(
                    [Consultation(doctor=request.user,
                                  type=type, price=price)])

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)

    def patch(self, request, type, *args, **kwargs):
        snippet = self.get_object(type)
        serializer = ConsultationSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
