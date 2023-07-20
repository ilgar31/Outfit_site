from django.contrib import admin
from .models import Profile, Items, Item_images, Favorites

admin.site.register(Profile)
admin.site.register(Favorites)


class Item_imagesInline(admin.TabularInline):
    fk_name = 'item'
    model = Item_images


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    inlines = [Item_imagesInline, ]
