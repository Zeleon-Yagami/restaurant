import secrets
import threading

from django.shortcuts import render, redirect, get_object_or_404

from .models import CustomUser, Otp

from django.contrib import messages

from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError

import re

from django.contrib.auth import authenticate, login ,logout

from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import PasswordChangeForm

from django.utils import timezone
from datetime import timedelta

from django.core.mail import send_mail

from django.urls import reverse

from .models import CustomUser, Profile

 

# Create your views here.

"""
def register(request):
    if request.method == 'POST':
        data = request.POST
        name = data['fullName']
        phone = data['phone']
        username = data['username']
        email = data['email']
        password = data['password']
        confirm_password = data['Re-password']

        if password == confirm_password:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect('register')
            
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect('register')
            CustomUser.objects.create_user(full_name=name, phone_number=phone, username=username, email=email, password=password)
            messages.success(request, "Register Successfully")
            return redirect('register')
            
        else:
            messages.error(request,"Password does not match")
            return redirect('register')            #url ko name = 'register' waala resiter ho
        

    return render(request, 'auth/register.html')

"""

#now including validation
"""
def register(request):
    if request.method == 'POST':
        data = request.POST
        name = data['fullName']
        phone = data['phone']
        username = data['username']
        email = data['email']
        password = data['password']
        confirm_password = data['Re-password']

        if password == confirm_password:
            try:

                validate_password(password)

                if CustomUser.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists")
                    return redirect('register')
            
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                    return redirect('register')
                
                if CustomUser.objects.filter(phone_number=phone).exists():
                    messages.error(request, "Phone number already register")
                    return redirect('register')
                
                CustomUser.objects.create_user(full_name=name, phone_number=phone, username=username, email=email, password=password)
                messages.success(request, "Register Successfully")
                return redirect('register')
            
            except ValidationError as e:
                for err in e.messages:
                    messages.error(request, err)
                return redirect('register')
            
            
        else:
            messages.error(request,"Password does not match")
            return redirect('register')            #url ko name = 'register' waala resiter ho
        

    return render(request, 'auth/register.html')
"""

def register(request):
    if request.method == 'POST':
        data = request.POST
        name = data['fullName']
        phone = data['phone']
        username = data['username']
        email = data['email']
        password = data['password']
        confirm_password = data['Re-password']

        if password == confirm_password:
            try:
                # user = CustomUser(full_name=name, phone_number=phone, username=username, email=email)
                # validate_password(password, user)

                validate_password(password)

                #for more validation
                if not re.search(r'[A-Z]', password):
                    messages.error(request, "Password must contain aleast one capital letter")
                    return redirect('register')
                
                if not re.search(r'\d', password):
                    messages.error(request, "Password must contain a digit")
                    return redirect('register')
                
                if not re.search(r'[\w_]', password):
                    messages.error(request, "Password must contain a Sepcial character")
                    return redirect('register')

                if CustomUser.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists")
                    return redirect('register')
            
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                    return redirect('register')
                
                if CustomUser.objects.filter(phone_number=phone).exists():
                    messages.error(request, "Phone number already register")
                    return redirect('register')
                
                CustomUser.objects.create_user(full_name=name, phone_number=phone, username=username, email=email, password=password)
                messages.success(request, "Register Successfully")
                return redirect('register')
            
            except ValidationError as e:
                for err in e.messages:
                    messages.error(request, err)
                return redirect('register')
            
            
        else:
            messages.error(request,"Password does not match")
            return redirect('register')            #url ko name = 'register' waala resiter ho
        

    return render(request, 'auth/register.html')


# def log_in(request):
#     if request.method == 'POST':
#         data = request.POST
#         email = data['email']
#         password = data['password']

#         return redirect('log_in')

#     return render(request, 'auth/login.html')


def log_in(request):
    if request.method == 'POST':
        data = request.POST
        email = data['email']
        password = data['password']

        remmber_me = data.get('rem_me')

        # User = authenticate(request, email=email, password=password)     #User(user object) or None
        user = authenticate(email=email, password=password)     #User(user object) or None

        if user is not None:           #if user
            login(request, user)
            if remmber_me:             #if on
                request.session.set_expiry(86400)        #add session    #login until 24 hour 
            else:
                request.session.set_expiry(0)         #destory session #logout when brower close

            return redirect('menu_page')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('log_in')

    return render(request, 'auth/login.html')


def logout_function(request):
    logout(request)
    messages.success(request, "logout successfully")
    return redirect('log_in')


@login_required(login_url='log_in')
def changePassword(request):

    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        #receive form data
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password change sucessfully")
            return redirect('log_in')
    return render(request, 'auth/changePassword.html', {'form':form})

"""
def emailRestPassword(request):
    if request.method == 'POST':
        data = request.POST
        email = data['email']

        #At first, check user exist or not using this email
        if not CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Invaild email address")
            return redirect('email_reset_password')
        
        #findind user
        user = CustomUser.objects.get(email=email)
        #Delete previous otp of this user
        # otp = Opt.objects.filter(user=user)
        # otp.delete()
        #in one line
        Otp.objects.filter(user=user).delete()


        #now generate otp in database and send it in email
        #========== generate opt =============
        otp = ''.join(secrets.choice("0123456789")for _ in range(4))
        #save into database
        Otp.objects.create(
            user=user,
            otp=otp,
            created_at = timezone.now(),
            expired_at = timezone.now()+timedelta(minutes=5)
            )
        #send mail

        subject = "OPT Verifications"
        message =  f'''
                    Your Otp is {otp}.
                    Please verify within 5 minute.
                    Do not share it with anyone
                    '''
        from_email =  "zeleonyagami@gmail.com"
        recipient_list = [email]
    
        
        #send main
        # send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=False)
        t1 = threading.Thread(target=send_mail,
                              args=(subject, message, from_email, recipient_list, False),
                              daemon=True
                              )
        t1.start()
        messages.success(request, "Otp sent successfully, please check your mail")

        # return redirect('verifyOtp')

        #set user id in url in patameter
        return redirect(reverse('verifyOtp')+f"?user_id={user.id}")



    return render(request, 'auth/reset-password/emailResetPassword.html')

def verifyOtp(request):

    if request.method == 'POST':
        data = request.POST
        otp = data['otp']
        uid = data['userId']

        #find otp row(recond) using this user than do this
        user = CustomUser.objects.get(id=uid)
        otp_recond = Otp.objects.filter(user=user, otp=otp).first()
        # otp_recond = Opt.objects.filter(user=CustomUser.objects.get(user=uid), otp=otp)   #in one line


        if not otp_recond:  #if false
            messages.error(request, "Invaild OTP")
            # return redirect('verifyOtp')
            return redirect(reverse('verifyOtp')+f"?user_id={user.id}")
        

        #check otp  expired or not
        current_time = timezone.now()
        if current_time>otp_recond.expired_at:    #if current_time>expired time
            otp_recond.delete()  #delete expired OTP
            messages.error(request, "OTP expired")
            return redirect(reverse('verifyOtp')+f"?user_id={user.id}")


        #==== otp valid case ====
        #first delete otp from database and then redirect to change password page
        otp_recond.delete()
        #return redirect('reset_password')
        return redirect(reverse('reset_password')+f'?user_id={user.id}')

    return render(request, 'auth/reset-password/verifyOtp.html')


def resetPassoword(request):
    if request.method == 'POST':
        data = request.POST
        password = data['password']
        confirm_password = data['Re-password']
        uid = data['userId']

        #find user using this id 
        user = CustomUser.objects.get(id=uid)
        
        if password == confirm_password:
            user.set_password(password)    #hash password
            user.save()
            messages.success(request, "Password Reset Successfully")
            return redirect('log_in')
        else:
            messages.error(request, "Paasword does not match")
            return redirect(reverse('reset_passwprd')+ f'?user_id={user.id}')
    return render(request, 'auth/reset-password/resetPassword.html')
"""


#================= set user_id in session ==============================

def emailRestPassword(request):
    if request.method == 'POST':
        data = request.POST
        email = data['email']

        #At first, check user exist or not using this email
        if not CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Invaild email address")
            return redirect('email_reset_password')
        
        #findind user
        user = CustomUser.objects.get(email=email)
        #Delete previous otp of this user
        # otp = Opt.objects.filter(user=user)
        # otp.delete()
        #in one line
        Otp.objects.filter(user=user).delete()


        #now generate otp in database and send it in email
        #========== generate opt =============
        otp = ''.join(secrets.choice("0123456789")for _ in range(4))
        #save into database
        Otp.objects.create(
            user=user,
            otp=otp,
            created_at = timezone.now(),
            expired_at = timezone.now()+timedelta(minutes=5)
            )
        #send mail

        subject = "OPT Verifications"
        message =  f'''
                    Your Otp is {otp}.
                    Please verify within 5 minute.
                    Do not share it with anyone
                    '''
        from_email =  "zeleonyagami@gmail.com"
        recipient_list = [email]
    
        
        #send main
        # send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=False)
        t1 = threading.Thread(target=send_mail,
                              args=(subject, message, from_email, recipient_list, False),
                              daemon=True
                              )
        t1.start()
        messages.success(request, "Otp sent successfully, please check your mail")


        #set user id in session

        request.session['user_id'] = user.id

        return redirect('verifyOtp')

        #set user id in url in patameter
        # return redirect(reverse('verifyOtp')+f"?user_id={user.id}")



    return render(request, 'auth/reset-password/emailResetPassword.html')

def verifyOtp(request):

    if request.method == 'POST':
        data = request.POST
        otp = data['otp']
        
        #receive user id from form
        # uid = data['userId']

        #receive uesr id from session
        uid = request.session['user_id']

        if not uid:
            messages.error(request, "Session expired.. Please reset password again")
            return redirect('reset_password')

        #find otp row(recond) using this user than do this
        user = CustomUser.objects.get(id=uid)
        otp_recond = Otp.objects.filter(user=user, otp=otp).first()
        # otp_recond = Opt.objects.filter(user=CustomUser.objects.get(user=uid), otp=otp)   #in one line


        if not otp_recond:  #if false
            messages.error(request, "Invaild OTP")
            return redirect('verifyOtp')
            # return redirect(reverse('verifyOtp')+f"?user_id={user.id}")
        

        #check otp  expired or not
        current_time = timezone.now()
        if current_time>otp_recond.expired_at:    #if current_time>expired time
            otp_recond.delete()  #delete expired OTP
            messages.error(request, "OTP expired")
            return redirect('verifyOtp')
            # return redirect(reverse('verifyOtp')+f"?user_id={user.id}")


        #==== otp valid case ====
        #first delete otp from database and then redirect to change password page
        otp_recond.delete()
        return redirect('reset_password')
        # return redirect(reverse('reset_password')+f'?user_id={user.id}')

    return render(request, 'auth/reset-password/verifyOtp.html')


def resetPassoword(request):
    if request.method == 'POST':
        data = request.POST
        password = data['password']
        confirm_password = data['Re-password']
        
        #receive user id from form
        # uid = data['userId']

        #receive user from session
        uid = request.session['user_id']

        if not uid:
            messages.error(request, "Session expired.. Please reset password again")
            return redirect('reset_password')

        #find user using this id 
        user = CustomUser.objects.get(id=uid)
        
        if password == confirm_password:
            user.set_password(password)    #hash password
            user.save()
            messages.success(request, "Password Reset Successfully")
            return redirect('log_in')
        else:
            messages.error(request, "Paasword does not match")
            return redirect('reset_password')
            # return redirect(reverse('reset_password')+ f'?user_id={user.id}')
    return render(request, 'auth/reset-password/resetPassword.html')


@login_required(login_url='log_in')
def profilePage(request):
    # usr = request.user
    # profile, created = Profile.objects.get_or_create(user=usr)

    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'profile/profile.html', {'pro':profile})


@login_required(login_url='log_in')
def editProfile(request):
    profile = Profile.objects.get(user=request.user)
    # Profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        #recieve from data
        data = request.POST
        fn = data['full_name']
        uname = data['username']
        em = data['email']
        phone = data['phone_number']
        gen = data['gender']
        bod = data['date_of_birth']

        #receive image
        pro_pic = request.FILES.get('profile_image')

        #find user and profile
        user = request.user
        # profile = Profile.objects.get(user=user)      # We already fetch(get) profile
        # profile = Profile.objects.get(user=request.user)

        #check unique things already exits or not
        #check email already exists or not 
        if CustomUser.objects.filter(email=user.email).exclude(id=user.id).exists():
            messages.error(request, "User with this email already exist")
            return redirect('edit_page')
        
        if CustomUser.objects.filter(phone=user.phone_number).exists():
            messages.error(request,"User with this number already exist")
            return redirect('edit_page')

        #Set database with incoming form data
        user.full_name = fn
        user.username = uname
        user.email = em
        user.phone_number = phone
        
        profile.gender = gen
        profile.date_of_birth = bod
        profile.updated_at = timezone.now()    #setting current time

        if pro_pic:     #if true
            profile.profile_pic = pro_pic

        #Now finally save user and profile into database
        user.save()
        profile.save()
        messages.success(request, "Profile updated successfully")
        return redirect('profile_page')
        
    return render(request, 'profile/edit.html', {'pro':profile})