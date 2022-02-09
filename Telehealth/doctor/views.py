from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from dateutil import rrule
from doctor.models import Consultation, Doctor, DoctorBooking, DoctorSpeciality, DoctorWorkTime, Insurance, RoleTranslate, Speciality
from doctor.serializers import ConsultationSerializer, CustomRegisterSerializer, DoctorBookingRoleSerializer, DoctorBookingSerializer, DoctorInsuranceSerializer, DoctorSpecialityListSerializer, DoctorSpecialitySerializer, DoctorWorkTimeSerializer, InsuranceSerializer, RoleTranslateSerializer, SpecialitySerializer

from .Permissions.permissions import DoctorPermission


class CurrentUserView(APIView):
    """
    Return User info
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # there is no use of self, just to ignore the static warning.
        _ = self
        queryset = Doctor.objects.filter(id=request.user.id)
        serializer = CustomRegisterSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorSpecialityView(APIView):
    """
    In GET request will show all Speciality availiable to choice
    In PATCH request will add Speciality to doctor
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        queryset = Speciality.objects.all()
        serializer = SpecialitySerializer(queryset, many=True)
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

        queryset = DoctorSpeciality.objects.select_related(
            'doctor', 'speciality').all()
        serializer = DoctorSpecialityListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        except:
            raise Http404

    def post(self, request, *args, **kwargs):

        serializer = ConsultationSerializer(data=request.data)

        if serializer.is_valid():
            valid_data = serializer.validated_data
            type = valid_data['type']
            price = valid_data['price']
            queryset = Consultation.objects.filter(
                doctor=request.user, type=type).exists()

            if queryset:
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


class DoctorInsuranceView(APIView):
    """
    GET all Insurance Company to choise
    POST to save doctor with company name and insurance_number
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        queryset = Insurance.objects.all()
        serializer = InsuranceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        serializer = DoctorInsuranceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(doctor=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)


class DoctorBookingView(APIView):
    """
    make auto add date for doctor where doctor should just put the start_date,
    end_date and Integer consultation_time in min
    EX: start_date: 2022-02-08 11:30
    end_date: 2022-02-08 14:30
    consultation_time: 30
    System will create:
    2022-02-08 11:30, 2022-02-08 12:00, 2022-02-08 12:30, 2022-02-08 13:00 ..
    and make any of this date available to booking
    add DoctorPermission we can make any Custom Permission this just for Demo
    DoctorPermission: need to give booking permission to user to can set work time
    """
    permission_classes = [IsAuthenticated and DoctorPermission]

    def post(self, request, *args, **kwargs):

        serializer = DoctorBookingRoleSerializer(data=request.data)

        if serializer.is_valid():
            valid_data = serializer.validated_data
            doctor = request.user
            start_date = valid_data['start_date']
            end_date = valid_data['end_date']
            time = valid_data['consultation_time']
            for dt in rrule.rrule(
                    rrule.MINUTELY, interval=time, dtstart=start_date, until=end_date):
                DoctorWorkTime.objects.bulk_create([DoctorWorkTime(
                    date=dt,
                    doctor=doctor
                )])
            Done = {'message': 'added successfuly'}
            return Response(Done, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorBookingAvailable(APIView):
    """
    to see all availiable booking time
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        queryset = DoctorWorkTime.objects.filter(
            doctor=request.user, is_availiable=True)
        serializer = DoctorWorkTimeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetBookingView(APIView):
    """
    make booking and lock date for this booking and validate if booking exists 
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer = DoctorBookingSerializer(data=request.data)

        if serializer.is_valid():
            valid_data = serializer.validated_data
            date = valid_data['date']
            get_date = DoctorWorkTime.objects.get(date__exact=date)

            if get_date.is_availiable:
                serializer.save(patient=request.user)
                DoctorWorkTime.objects.filter(
                    date__exact=date).update(is_availiable=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                MsgError = {'message': 'you should choice valid time'}
                return Response(MsgError, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorPatientView(APIView):
    """
    get all users with date was booked for specific doctor
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = DoctorBooking.objects.filter(doctor=request.user)
        serializer = DoctorBookingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleTranslateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, lan, *args, **kwargs):

        queryset = RoleTranslate.objects.filter(lan__lan=lan)
        serializer = RoleTranslateSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
