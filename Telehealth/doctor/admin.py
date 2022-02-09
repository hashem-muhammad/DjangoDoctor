from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from doctor.models import Consultation, Doctor, DoctorBooking, DoctorSpeciality, DoctorWorkTime, Insurance, Language, Role, RoleTranslate, Speciality


@admin.register(Doctor)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'password',)}),
        ('Personal info', {'fields': ('phone',)}),
        ('Permissions', {
         'fields': ('is_active', 'is_staff', 'role', 'groups',)}),
        ('Note', {'fields': ('about',)})
    )

    add_fieldsets = (
        (None, {'fields': ('name', 'password1', 'password2')}),
        ('Personal info', {'fields': ('phone',)}),
        ('Permissions', {
         'fields': ('is_active', 'is_staff', 'role', 'groups',)}),
        ('Note', {'fields': ('about',)})
    )
    search_fields = ['name']
    list_display = ('name', 'phone',)
    ordering = ['name', ]
    list_per_page = 10


admin.site.register(Role)
admin.site.register(Speciality)
admin.site.register(Insurance)
admin.site.register(DoctorSpeciality)
admin.site.register(Consultation)
admin.site.register(DoctorWorkTime)
admin.site.register(DoctorBooking)
admin.site.register(Language)
admin.site.register(RoleTranslate)
