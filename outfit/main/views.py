from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.forms import TextInput
from .models import Items, Favorites, Basket, Profile, Purchase, Items_purchase, Watched
from django.http import JsonResponse, HttpResponseNotFound
import json
import random
import datetime


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
    if pk != request.user.id:
        return HttpResponseNotFound("Страница другого пользователя")
    favorites = Favorites.objects.filter(id_user=pk)
    favorites_items = []
    for item in favorites:
        favorites_items.extend(Items.objects.filter(id=item.id_item))
    if request.method == "POST":
        logout(request)
        return redirect("home")
    data = []
    for offer in Purchase.objects.filter(id_user=pk):
        items = []
        for index, i in enumerate(offer.items.all()):
            if index == 3:
                items[2] = "more"
                break
            items.append(Items.objects.get(id=i.id_item).images.all()[0])
        data2 = dict()
        data2['items'] = items
        data2['offer'] = offer
        data.append(data2)
    return render(request, "main/profile.html", {"favorites_items": favorites_items, "data": data})


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
            return redirect("profile", request.user.id)
    else:
        profile_form = ProfileForm()
        profile_form.fields["user_name"].initial = request.user.profile.user_name
        profile_form.fields["user_surname"].initial = request.user.profile.user_surname
        if request.user.profile.gender:
            profile_form.fields["gender"].initial = request.user.profile.gender
        else:
            profile_form.fields["gender"].initial = "M"

        if request.user.profile.birthday:
            profile_form.fields["birthday"].initial = request.user.profile.birthday
        else:
            profile_form.fields["birthday"].initial = datetime.datetime.now()
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
    watched_items = []
    if request.user.is_authenticated:
        watched_items = Watched.objects.filter(profile=request.user.profile)
        if len(watched_items) == 7:
            watched_items[0].delete()
            watched_items = watched_items[1:]

        watched_items = list(map(lambda x: Items.objects.get(id=x.item_id), watched_items))[::-1]
        if len(Watched.objects.filter(item_id=pk)) == 1:
            Watched.objects.get(item_id=pk).delete()
        watched = Watched()
        watched.profile = request.user.profile
        watched.item_id = pk
        watched.save()

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.POST.get("type_POST") == "basket":
        #Проверка
        item_in_basket = False
        if request.POST.get("type_size") == "RU":
            if Basket.objects.filter(id_user=request.user.id, id_item=pk, item_type_size=request.POST.get("type_size"), item_size = request.POST.get("RU_size")):
                item_in_basket = True
        else:
            if Basket.objects.filter(id_user=request.user.id, id_item=pk, item_type_size=request.POST.get("type_size"), item_size = request.POST.get("EU_size")):
                item_in_basket = True

        if not item_in_basket and request.POST.get("class") == "buy_button":
            product_add_to_basket = Basket()
            product_add_to_basket.id_item = pk
            product_add_to_basket.id_user = request.user.id
            product_add_to_basket.item_type_size = request.POST.get("type_size")
            if request.POST.get("type_size") == "RU":
                product_add_to_basket.item_size = request.POST.get("RU_size")
            else:
                product_add_to_basket.item_size = request.POST.get("EU_size")
            item_in_basket = True
            product_add_to_basket.save()

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
    return render(request, "main/product_page.html", {"item": item, "images_count": range(len(item.images.all())), "icon": icon, "types_size": enumerate(list(types_size)), "sizes": sizes, "other_colors": other_colors, "watched_items": watched_items})


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
    count = 0
    for i in items_in_basket:
        items.append({"item": Items.objects.get(id=i.id_item), "basket": i})
        cost += items[-1]["item"].cost * items[-1]['basket'].count
        count += items[-1]['basket'].count

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.POST.get("type") == 'delete':
        item = Basket.objects.get(id=request.POST.get("id"))
        cost -= Items.objects.get(id=item.id_item).cost * item.count
        count -= item.count
        item.delete()
        return JsonResponse({"count": count, "cost": cost})
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.POST.get("type") == 'change_count':
        item = Basket.objects.get(id=request.POST.get("id"))
        item_count = item.count

        if request.POST.get("operation") == "plus":
            item_count += 1
            item.count += 1
            item.save()
            cost += Items.objects.get(id=item.id_item).cost
            count += 1
        else:
            item_count -= 1
            item.count -= 1
            item.save()
            cost -= Items.objects.get(id=item.id_item).cost
            count -= 1
        return JsonResponse({"count": count, "cost": cost, "item_count": item_count})

    return render(request, "main/basket.html", {"user": user, "items": enumerate(items), "cost": cost, "count": count})


def purchase(request):
    items = list(map(lambda x: {"item": Items.objects.get(id=x.id_item), "type_size": x.item_type_size, "size": x.item_size, "count": x.count}, Basket.objects.filter(id_user=request.user.id)))
    number = 0
    for i in items:
        i['number_item'] = number
        number += 1
    if request.method == "POST":
        new_purchase = Purchase()
        new_purchase.id_user = request.user.id
        new_purchase.offer_number = random.randint(100001, 999999)
        new_purchase.number = request.POST.get("number")
        new_purchase.FIO = request.POST.get("FIO")
        new_purchase.tg = request.POST.get("tg")
        new_purchase.email = request.POST.get("email")
        new_purchase.region = request.POST.get("region")
        new_purchase.city = request.POST.get("city")
        new_purchase.delivery = request.POST.get("delivery")
        new_purchase.payment = request.POST.get("payment")
        new_purchase.save()

        for i in items:
            item_purchase = Items_purchase()
            item_purchase.purchase = new_purchase
            item_purchase.id_item = i['item'].id
            item_purchase.item_type_size = i['type_size']
            item_purchase.item_size = i['size']
            item_purchase.count = i['count']
            item_purchase.save()
        return redirect("thanks", new_purchase.offer_number)
    return render(request, 'main/purchase.html', {"items": items})


def thanks(request, pk):
    if request.user.id != Purchase.objects.get(offer_number=pk).id_user:
        return HttpResponseNotFound("К сожалению это не ваш заказ")
    items = Items.objects.all()[:6]
    return render(request, 'main/thanks.html', {"items": items, "pk": pk})


def offer(request, pk):
    purchase_object = Purchase.objects.get(offer_number=pk)
    if request.user.id != purchase_object.id_user:
        return HttpResponseNotFound("К сожалению это не ваш заказ")
    purchase_object.date = purchase_object.date.strftime("%d.%m.%Y %H:%M")
    items = []
    index2 = 0
    cost = 0
    for i in purchase_object.items.all():
        data = dict()
        data['item'] = Items.objects.get(id=i.id_item)
        data["type_size"] = purchase_object.items.all()[index2].item_type_size
        data["size"] = purchase_object.items.all()[index2].item_size
        data['count'] = purchase_object.items.all()[index2].count
        data['final_cost'] = data["item"].cost * data['count']
        cost += data['final_cost']
        items.append(data)
        index2 += 1
    return render(request, 'main/offer.html', {"data": purchase_object, "items": items, "cost": cost})
