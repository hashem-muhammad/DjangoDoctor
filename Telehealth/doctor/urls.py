from . import views
from django.urls import path, include


urlpatterns = [
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('get_my_account/', views.CurrentUserView.as_view()),
    path('set_speciality/', views.DoctorSpecialityView.as_view()),
    path('set_consultaion/', views.ConsultationView.as_view()),
    path('set_consultaion/<int:type>', views.ConsultationView.as_view()),
    path('set_insurance/', views.DoctorInsuranceView.as_view()),
    path('set_my_availabilit_slot/', views.DoctorBookingView.as_view()),
    path('get_my_availability_slots/', views.DoctorBookingAvailable.as_view()),
    path('set_booking/', views.SetBookingView.as_view()),
    path('get_my_patients/', views.DoctorPatientView.as_view()),
    path('doctors/', views.DoctorSpecialityListView.as_view()),
    path('get_role/<str:lan>/', views.RoleTranslateView.as_view()),
]
