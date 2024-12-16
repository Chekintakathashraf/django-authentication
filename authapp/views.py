from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .email import sendOtpToEmail
import random
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


from django.contrib import messages

User = get_user_model()



def login_page(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')

        user_obj = User.objects.filter(phone_number = phone_number)
        if not user_obj.exists():
            return redirect('/')
        email = user_obj[0].email
        otp = random.randint(1000, 9999)
        user_obj.update(otp = otp)
        subject = "OTP for Login"
        message  = f"You otp is {otp}"

        sendOtpToEmail(
            email,subject, message
        )

        return redirect(f'/check-otp/{user_obj[0].id}/') 

    return render(request, 'login.html')




def check_otp(request, user_id):

            
    if request.method == "POST":
        user_obj = User.objects.get(id = user_id)
            
        otp = request.POST.get('otp')
        print(type(otp), type(user_obj.otp))
        if int(otp) == user_obj.otp:
            login(request, user_obj)
            return redirect('/dashboard/') 
        messages.error(request, "Invald OTP.")
        return redirect(f'/check-otp/{user_obj.id}/') 
    
    return render(request, 'check_otp.html')


@login_required(login_url='/')
def dashboard(request):
    return HttpResponse("You are logged in")