from django.db import models
from django.contrib.auth.models import AbstractUser
from .Manager.manager import UserManager

# we have many way to support multi language, I put sample using databas
# we can ues external package but I don't know what you want


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    lan = models.CharField(max_length=5, null=True)

    def __str__(self) -> str:
        return f'{self.lan}'

# class role for demo to make Patient account
# default = DOCTOR because it is the mean for DEMO


class Role(models.Model):
    Role = (
        (1, 'Patient'),
        (2, 'Doctor'),
    )
    id = models.AutoField(primary_key=True)
    role = models.IntegerField(choices=Role, default=2)

    def __str__(self) -> str:
        return f'{self.role}'


class RoleTranslate(models.Model):
    id = models.AutoField(primary_key=True)
    lan = models.ForeignKey(Language, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    translate = models.CharField(max_length=10, null=True)

    def __str__(self) -> str:
        return f'{self.id}'


class Doctor(AbstractUser):
    USERNAME_FIELD = 'phone'
    username = None
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, null=True, blank=True)
    phone = models.IntegerField(null=True, unique=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=60, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=2)

    objects = UserManager()

    def __str__(self) -> str:
        return f'{self.name}'


class Speciality(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True)

    def __str__(self) -> str:
        return f'{self.name}'


class DoctorSpeciality(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.speciality}'


class Consultation(models.Model):
    consultation_type = (
        (1, 'Clinical'),
        (2, 'Online'),
    )
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    type = models.IntegerField(choices=consultation_type, default=1, null=True)
    price = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f'{self.type}'


class Insurance(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=40, null=True)

    def __str__(self) -> str:
        return f'{self.company}'


class DoctorInsurance(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, models.CASCADE)
    insurance = models.ForeignKey(Insurance, models.CASCADE)
    insurance_number = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.id}'


class DoctorBookingRole(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    consultation_time = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f'{self.date}'


class DoctorWorkTime(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    is_availiable = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.id}'


class DoctorBooking(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.id}'
