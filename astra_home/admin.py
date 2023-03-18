from django.contrib import admin

# Register your models here.
from .models import SiteUserModel, UserCartModel, CartModel, OrderModel, SportsModel


class HospitalModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(SiteUserModel, HospitalModelAdmin)


class UserCartModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserCartModel, UserCartModelAdmin)


class CartModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(CartModel, CartModelAdmin)


class OrderModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(OrderModel, OrderModelAdmin)


class SportsModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(SportsModel, SportsModelAdmin)
