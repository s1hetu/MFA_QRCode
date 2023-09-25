from django.conf.urls.static import static
from django.urls import path
from two_fa_setup import settings
from .views import VerifyOTP, Registration, Login, AuthDetails, Dashboard, Logout

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('register', Registration.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('auth_details', AuthDetails.as_view(), name='auth_details'),
    path('verify_otp', VerifyOTP.as_view(), name='verify-otp')
]