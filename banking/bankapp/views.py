from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def homepage(request):
    return render(request, 'home.html')


def reg(request):
    return render(request, 'register.html')


def loginpage(request):
    return render(request, 'login.html')


@login_required(login_url='user_login')
def indexpage(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        psw = request.POST['psw']
        cpsw = request.POST['psw-repeat']

        if psw == cpsw:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username already Taken")
                print("username already exists")
                return redirect('reg')

            else:
                user = User.objects.create_user(username=username,
                                                password=psw)
                user.save()

                print("user created")

        else:
            print("password not matching")
            messages.info(request, "password not matching")
            return redirect('reg')
        return redirect('login')

    else:

        return render(request, 'login.html')


def user_login(request):
    try:
        if request.method == 'POST':
            try:
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    auth.login(request, user)
                    messages.info(request, f'Welcome {username}')
                    return redirect('indexpage')
                else:
                    messages.info(request, 'Invalid username or password')
                    return redirect('loginpage')
            except:
                messages.info(request, 'Invalid username or password')
                return render(request, 'login.html')
        else:

            return render(request, 'login.html')
    except:
        messages.info(request, 'Invalid username or password')
        return render(request, 'login.html')


@login_required(login_url='user_login')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('homepage')
