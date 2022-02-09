from rest_framework import serializers
from django.db import transaction
from dj_rest_auth.registration.serializers import RegisterSerializer
from doctor.models import Consultation, Doctor, DoctorBooking, DoctorBookingRole, DoctorInsurance, DoctorSpeciality, DoctorWorkTime, Insurance, RoleTranslate, Speciality


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


class ConsultationSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(read_only=True)

    class Meta:
        model = Consultation
        fields = ['id', 'doctor', 'type', 'price', ]


class InsuranceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Insurance
        fields = ['id', 'company', ]


class DoctorInsuranceSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(read_only=True)

    class Meta:
        model = DoctorInsurance
        fields = ['id', 'doctor', 'insurance', 'insurance_number', ]


class DoctorBookingRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorBookingRole
        fields = ['id', 'start_date', 'end_date', 'consultation_time', ]


class DoctorWorkTimeSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(read_only=True)

    class Meta:
        model = DoctorWorkTime
        fields = ['id', 'doctor', 'date', 'is_availiable', ]


class DoctorBookingSerializer(serializers.ModelSerializer):
    patient = serializers.CharField(read_only=True)

    class Meta:
        model = DoctorBooking
        fields = ['id', 'patient', 'doctor', 'date', ]


class RoleTranslateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoleTranslate
        fields = ['translate', ]
