from django.contrib import admin
from .models import Restaurant, Table, Menu, Reservation

class TableInline(admin.TabularInline):
    model = Table
    extra = 1

class MenuInline(admin.TabularInline):
    model = Menu
    extra = 1

class RestaurantAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'owner']}),
    ]
    inlines = [TableInline, MenuInline]




admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Reservation)