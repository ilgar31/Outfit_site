from django.contrib import admin
from .models import Profile, Items, Item_images, Favorites, Item_sizes, Basket, Purchase, Items_purchase

admin.site.register(Profile)
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


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = [Items_purchaseInline, ]


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    inlines = [Item_imagesInline, Item_sizesInline]
