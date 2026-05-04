from django.urls import path

from .views import log_in, register, logout_function, changePassword, emailRestPassword, verifyOtp, resetPassoword, profilePage, editProfile

urlpatterns = [
  path('login/', log_in, name='log_in'),
  path('register/', register, name='register'),
  path('logout/', logout_function, name='log_out'),
  path('change-password/', changePassword, name='change_password'),
  path('email-reset-password/', emailRestPassword, name='email_reset_password'),
  path('Verify-otp/', verifyOtp, name='verifyOtp'),
  path('reset-password/', resetPassoword, name='reset_password' ),
  path('profile/', profilePage, name='profile_page'),
  path('edit/', editProfile, name='edit_page'),
]