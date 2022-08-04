from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from authsystem import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout


def home(request):
 return render (request, "users/index.html")

def signup(request):
 if request.method == "POST":
     username=request.POST.get('username')
     fname=request.POST.get('fname')
     sname=request.POST.get('sname')
     email=request.POST.get('email')
     pass1=request.POST.get('pass1')
     pass2=request.POST.get('pass2')
     if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
     if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
     if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
     if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
     myuser= User.objects.create_user(username, email, pass1) 
     myuser.first_name= fname
     myuser.save()
     
     messages.success(request, "You have been successfully registered !!")

     subject = "Welcome to Django Login!!"
     message = "Hello " + myuser.first_name + "!! \n" + "Welcome !! We have also sent you a confirmation email, please confirm your email address."        
     from_email = settings.EMAIL_HOST_USER
     to_list = [myuser.email]
     send_mail(subject, message, from_email, to_list, fail_silently=True)
        
     return redirect ("signin")

 return render (request, "users/signup.html")

def signin(request):
 if request.method == "POST":
       username=request.POST.get('username')
       pass1=request.POST.get('pass1')

       user=authenticate(username=username, password= pass1)
       if user is not None:
         login(request, user)
         fname= user.first_name
         return render (request, "users/index.html",{'fname':fname})
       else:
        messages.error(request, "Bad Credentials")
        return redirect (home)
 
 return render (request, "users/signin.html")

def signout(request):
  logout(request)
  messages.success(request, "Logged Out Successfully!!")
  return redirect(home)



