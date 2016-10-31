from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse
from models import Users

# Create your views here.
def index(request):
    if 'uid' in request.session:
        return redirect(reverse('travel-index'))
    return render(request,
    'registration/index.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password1']
        c_password = request.POST['password2']

        if Users.objects.filter(email=email):
            messages.error(request, "Ruh Roh! Email is already in use.")
            return redirect(reverse('login-main'))

        result = Users.objects.register(first_name = first_name, last_name =last_name, email=email, password1=password, password2 = c_password)
        if result[0]:
            print "No Pass! {}".format(result[1])
            for row in result[1]:
                messages.error(request, row)
            return redirect(reverse('login-main'))
        else:
            hashed = Users.objects.create_password(password)
            user = Users(first_name = first_name, last_name = last_name, email= email, password = hashed)
            user.save()
            try:
                u = Users.objects.get(email=email)
            except:
                return HttpResponse("Ruh Roh! Something went wrong.v Please contact site administrator.")

            request.session['first_name'] = u.first_name
            request.session['uid'] = u.id
            return redirect(reverse('travel-index'))
    else:
        messages.error(request, "Invalid register method")
        return redirect(reverse('login-main'))
    pass

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = Users.objects.get(email = email)
        except:
            messages.error(request, "User not found!")
            return redirect(reverse('login-main'))
        if user and Users.objects.verify_password(password,user.password):
            # request.session['first_name'] = user.first_name
            # request.sesssion['last_name'] = user.last_name
            # request.session['uid'] = user.id
            request.session['first_name'] = user.first_name
            request.session['uid'] = user.id
            return redirect(reverse('travel-index'))
        else:
            messages.error(request, "Incorrect Password!")
            return redirect(reverse('login-main'))
    else:
        return redirect(reverse('login-main'))

def logout(request):
    messages.success(request, "You've successfully logged out, {}".format(request.session['first_name']))
    for key in request.session.keys():
        del request.session[key]
    return redirect(reverse('login-main'))
