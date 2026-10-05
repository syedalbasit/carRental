from django.contrib import admin
from car_rental_app.models import *
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active']
    list_filter = ['email', 'is_staff', 'is_active', 'user_type']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'user_type')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active', 'user_type')}  # Include 'user_type'
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserType)
admin.site.register(Car)
admin.site.register(Category)
admin.site.register(CarModel)
admin.site.register(CarVariant)
admin.site.register(CarImage)
admin.site.register(Transmission)
admin.site.register(Rental)
admin.site.register(RentalStatus)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(FuelType)