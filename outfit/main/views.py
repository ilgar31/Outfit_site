from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.forms import TextInput
from .models import Items, Favorites, Basket
from django.http import JsonResponse
import json


def index(request):
    return render(request, "main/index.html")


def goods(request):
    items = Items.objects.all()
    return render(request, "main/goods.html", {"items": items})


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
    favorites = Favorites.objects.filter(id_user=request.user.id)
    favorites_items = []
    for item in favorites:
        favorites_items.extend(Items.objects.filter(id=item.id_item))
    if request.method == "POST":
        logout(request)
        return redirect("home")
    return render(request, "main/profile.html", {"favorites_items": favorites_items})


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
            return redirect("profile")
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


def beautiful_price(number):
    cnt = 0
    new_price = ''
    for c in str(number)[::-1]:
        new_price += c
        cnt += 1
        if cnt % 3 == 0:
            new_price += ' '
    return new_price[::-1]


colors = {"Красный": "rgb(255, 0, 0)", "Белый": "rgb(255, 255, 255)", "Коричневый": "rgb(102, 51, 0)", "Черный": "rgb(0, 0, 0)", "Бежевый": "rgb(255, 204, 153)"}


def product_page(request, pk):
    item = Items.objects.get(id=pk)
    item.cost = beautiful_price(item.cost)
    in_favorites = False
    if Favorites.objects.filter(id_user=request.user.id, id_item=pk):
        in_favorites = True
    types_size = set()
    for i in item.sizes.all():
        types_size.add(i.type_size)
    sizes = {"RU": [], "EU": []}
    for i in item.sizes.all():
        if i.type_size == "RU":
            sizes["RU"].append(i.size)
        elif i.type_size == "EU":
            sizes["EU"].append(i.size)
    for i in sizes:
        sizes[i] = enumerate(sizes[i])

    other_colors = []
    for i in Items.objects.filter(name=item.name):
        other_colors.append([i, colors[i.color]])

    return render(request, "main/product_page.html", {"item": item, "images_count": range(len(item.images.all())), "in_favorites": in_favorites, "types_size": enumerate(list(types_size)), "sizes": sizes, "other_colors": other_colors})


def search_results(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        item = request.POST.get('item')
        search_items = Items.objects.filter(name__icontains=item)
        if len(search_items) > 0 and len(item.replace(" ", '')) > 0:
            data = []
            for i in search_items:
                element = {
                    'pk': i.pk,
                    'name': i.name,
                    'color': i.color,
                    'image': '/static/' + str(i.images.all()[0]),
                    'url': "product/" + str(i.pk)
                }
                data.append(element)
            res = data
        else:
            res = "Товар не найден"
        return JsonResponse({"item": res})
    return JsonResponse({})


def add_to_favourites(request, pk):
    user = request.user
    connection = Favorites.objects.filter(id_user=user.id, id_item=pk)
    if connection:
        connection[0].delete()
        return redirect("product_page", pk)
    product_add_to_favorite = Favorites()
    product_add_to_favorite.id_item = pk
    product_add_to_favorite.id_user = user.id
    print(product_add_to_favorite)
    product_add_to_favorite.save()
    return redirect("product_page", pk)


def basket(request):
    user = request.user
    items_in_basket = Basket.objects.filter(id_user=user.id)
    items = []
    for i in items_in_basket:
        items.append(Items.objects.get(id=i.id_item))
    print(items)
    return render(request, "main/basket.html", {"user": user, "items": items})


def add_to_basket(request, pk):
    user = request.user
    if Basket.objects.filter(id_user=user.id, id_item=pk):
        return redirect("product_page", pk)
    product_add_to_basket = Basket()
    product_add_to_basket.id_item = pk
    product_add_to_basket.id_user = user.id
    product_add_to_basket.save()
    return redirect("product_page", pk)

