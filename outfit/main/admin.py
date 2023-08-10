from django.contrib import admin
from .models import Profile, Items, Item_images, Favorites, Item_sizes, Basket, Purchase, Items_purchase, Watched, Search_history

admin.site.register(Favorites)
admin.site.register(Basket)


class Items_purchaseInline(admin.TabularInline):
    fk_name = 'purchase'
    model = Items_purchase

class Item_imagesInline(admin.TabularInline):
    fk_name = 'item'
    model = Item_images


class Item_sizesInline(admin.TabularInline):
    fk_name = 'item'
    model = Item_sizes


class WatchedInline(admin.TabularInline):
    fk_name = 'profile'
    model = Watched


class Search_historyInline(admin.TabularInline):
    fk_name = 'profile'
    model = Search_history


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = [Items_purchaseInline, ]


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    inlines = [Item_imagesInline, Item_sizesInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [WatchedInline, Search_historyInline, ]
