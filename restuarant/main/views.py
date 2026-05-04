import threading
from threading import Thread

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail

from .models import Contact, Category, Momo, Testimonial


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from datetime import datetime

from .models import Contact

from django.contrib.auth.decorators import login_required

from django.utils import timezone

# from resturant import settings 

# Create your views here.
def index(request):
    current_time = timezone.now()
    categories = Category.objects.all()
    testimonial = Testimonial.objects.all()

    #recieve cate_id from url
    c_id =  request.GET.get("cate_id")

    if c_id:      #if True
        #tyo catagory wala dehkau ney
        momos = Momo.objects.filter(catagory=c_id)
    else:
        momos = Momo.objects.all()
    # return render(request, 'main/index.html', {"cate":categories,"momo":momos, "cat_id":c_id, "ct":current_time})        #{"key":value} ==> dictionary(contexDictionary)

    context = {
        "cate":categories,
        "momo":momos, 
        "cat_id":c_id, 
        "ct":current_time,
        "testi":testimonial,
        }
    

    return render(request, 'main/index.html', context)        #{"key":value} ==> dictionary(contexDictionary)

def aboutPage(request):
    return render(request, 'main/about.html')

# def contactPage(request):
#     if request.method == 'POST':
#         #receive form data[i.e. data is receive in the form of dictionary]
#         data = request.POST
#         #get(receive) individual data
#         f_name = data["fullName"]
#         em = data["email"]
#         phone = data["phoneNumber"]
#         msg = data["msg"]

#         #save into data
#         Contact.objects.create(full_name=f_name, email=em, phone_number=phone, message=msg)

#         #send email
#         subject = "Zeleon Resturant"
#         message = "Thanks for contacting us"
#         message = f""" 
#                 Dear {f_name},
#                 Thanks for contacting us 
#                 We are gratefull to service you       
#                 """
#         from_email = "zeleonyagami@gmail.com"
#         recipient_list = [em]

#         # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#         # send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=False)

#         # t1 = Thread(target=send_mail, daemon=True)
#         # t1 = threading.Thread(target=send_mail,args=(subject, message, from_email, recipient_list, False),daemon=True)
#         # t1.start()

#         t1 = threading.Thread(target=send_mail,
#                               kwargs={
#                                   'subject': subject,
#                                   'message': message,
#                                   'from_email': from_email,
#                                   'recipient_list': recipient_list,
#                                   'fail_silently': False
#                               },
#                               daemon=True
#                               )

#         t1.start()

#         messages.success(request, "Submitted Successfully")
#         # return redirect('contact_page')
#         return redirect(reverse('contact_page') + '#helloDipak')


#     return render(request, 'main/contact.html')

def contactPage(request):
    if request.method == 'POST':
        #receive form data[i.e. data is receive in the form of dictionary]
        data = request.POST
        #get(receive) individual data
        f_name = data["fullName"]
        em = data["email"]
        phone = data["phoneNumber"]
        msg = data["msg"]

        #save into data
        Contact.objects.create(full_name=f_name, email=em, phone_number=phone, message=msg)

        #=========== send email with html file ==================
        subject = "Kiran Momo Restaurant"
        from_email = "zeleonyagami@gmail.com"
        to = [em]          #jaisle from  varxa tesko email
        
        
        # First, render the plain text content.
        text_content = render_to_string('main/EmailMessage.html', {"fullName":f_name, "date":datetime.now().year})  #{"key": value}

        # Secondly, render the HTML content.
        html_content = text_content

        # Then, create a multipart email instance. [i.e creating object of EmailMultiternative]
        msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=to)

        #lastly to remove html tags
        msg.attach_alternative(html_content, 'text/html')
        # msg.send() send [for fast (background running use deamon)]

        t1 = threading.Thread(target=msg.send, daemon=True)
        t1.start()

        messages.success(request, "Submitted Successfully")
        # return redirect('contact_page')
        return redirect(reverse('contact_page') + '#helloDipak')

    return render(request, 'main/contact.html')


def menuPage(request):
    momo = Momo.objects.all()

    return render(request, 'main/menu.html', {"momo":momo})

def servicesPage(request):
    return render(request, 'main/services.html')