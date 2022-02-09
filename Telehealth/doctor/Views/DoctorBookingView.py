from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from doctor.Permissions.permissions import DoctorPermission
from dateutil import rrule
from doctor.models import DoctorBooking, DoctorBookingRole, DoctorWorkTime


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
        doctor = request.user
        if serializer.is_valid():
            valid_data = serializer.validated_data
            start_date = valid_data['start_date']
            end_date = valid_data['end_date']
            time = valid_data['consultation_time']
            for dt in rrule.rrule(
                    rrule.MINUTELY, interval=time, dtstart=start_date, until=end_date):
                DoctorWorkTime.objects.bulk_create([DoctorWorkTime(
                    date=dt,
                    doctor=doctor
                )])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorBookingAvailable(APIView):
    """
    to see all availiable booking time
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        qs = DoctorWorkTime.objects.filter(
            doctor=request.user, is_availiable=True)
        serializer = DoctorWorkTimeSerializer(qs, many=True)
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
                get_date.update(is_availiable=False)
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
        qs = DoctorBooking.objects.filter(doctor=request.user)
        serializer = DoctorBookingSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
