from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, "main/index.html")


def goods(request):
    return render(request, "main/goods.html")


def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return render(request, 'main/index.html')
    else:
        user_form = UserRegistrationForm()
    return render(request, "main/registration.html", {"user_form": user_form})


def login_page(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            redirect('registration')
    return render(request, "main/login.html")


def profile(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    return render(request, "main/profile.html")


def profile_change(request):
    return render(request, "main/profile_change.html")

