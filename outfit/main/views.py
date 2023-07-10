from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.forms import TextInput


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
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_obj = request.user.profile
            profile_obj.user_name = profile_form['user_name'].value()
            profile_obj.user_surname = profile_form['user_surname'].value()
            profile_obj.gender = profile_form['gender'].value()
            profile_obj.birthday = profile_form['birthday'].value()
            profile_obj.country = profile_form['country'].value()
            try:
                profile_obj.img = request.FILES['img']
            except:
                pass

            profile_obj.save()
            return render(request, 'main/profile.html')
        else:
            print("no")
    else:
        profile_form = ProfileForm()
        profile_form.fields["user_name"].initial = request.user.profile.user_name
        profile_form.fields["user_surname"].initial = request.user.profile.user_surname
        profile_form.fields["gender"].initial = request.user.profile.gender
        profile_form.fields["birthday"].initial = request.user.profile.birthday
        profile_form.fields["country"].initial = request.user.profile.country

    return render(request, "main/profile_change.html", {"profile_form": profile_form})

