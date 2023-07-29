from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.forms import TextInput
from .models import Items, Favorites, Basket, Profile
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


def profile(request, pk):
    favorites = Favorites.objects.filter(id_user=pk)
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
    item_in_basket = False

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.POST.get("type_POST") == "basket":

        #Проверка
        if request.POST.get("type_size") == "RU":
            if Basket.objects.filter(id_user=request.user.id, id_item=pk, item_type_size=request.POST.get("type_size"), item_size = request.POST.get("RU_size")):
                item_in_basket = True
        else:
            if Basket.objects.filter(id_user=request.user.id, id_item=pk, item_type_size=request.POST.get("type_size"), item_size = request.POST.get("EU_size")):
                item_in_basket = True

        if not item_in_basket:
            product_add_to_basket = Basket()
            product_add_to_basket.id_item = pk
            product_add_to_basket.id_user = request.user.id
            product_add_to_basket.item_type_size = request.POST.get("type_size")
            if request.POST.get("type_size") == "RU":
                product_add_to_basket.item_size = request.POST.get("RU_size")
            else:
                product_add_to_basket.item_size = request.POST.get("EU_size")
            product_add_to_basket.save()
            item_in_basket = True

        print(item_in_basket)

    item = Items.objects.get(id=pk)
    item.cost = beautiful_price(item.cost)
    in_favorites = False
    if Favorites.objects.filter(id_user=request.user.id, id_item=pk):
        in_favorites = True

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.POST.get("type_POST") == "like":
        if in_favorites:
            Favorites.objects.get(id_user=request.user.id, id_item=pk).delete()
            res = "/static/main/png/heart_icon.svg"

        else:
            product_add_to_favorite = Favorites()
            product_add_to_favorite.id_item = pk
            product_add_to_favorite.id_user = request.user.id
            product_add_to_favorite.save()
            res = "/static/main/png/heart_icon1.svg"

        return JsonResponse({"img": res})

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

    if in_favorites:
        icon = "/static/main/png/heart_icon1.svg"
    else:
        icon = "/static/main/png/heart_icon.svg"
    return render(request, "main/product_page.html", {"item": item, "images_count": range(len(item.images.all())), "icon": icon, "types_size": enumerate(list(types_size)), "sizes": sizes, "other_colors": other_colors})


def search_results(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        item = request.POST.get('item')
        search_items = Items.objects.filter(name__icontains=item)
        # users = Profile.objects.all()
        # search_users = []
        # for i in range(len(users)):
        #     search_users.append(users[i].user.username)
        if len(search_items) > 0 and len(item.replace(" ", '')) > 0:
            data = []
            for i in search_items:
                element = {
                    'pk': i.pk,
                    'name': i.name,
                    'image': '/static/' + str(i.images.all()[0]),
                    'url': "/product/" + str(i.pk)
                }
                data.append(element)
            res = data
        else:
            res = "Товар не найден"
        return JsonResponse({"item": res})
    return JsonResponse({})


def basket(request):
    user = request.user
    items_in_basket = Basket.objects.filter(id_user=user.id)
    items = []
    cost = 0
    for i in items_in_basket:
        items.append(Items.objects.get(id=i.id_item))
        cost += items[-1].cost
    return render(request, "main/basket.html", {"user": user, "items": items, "cost": cost})


