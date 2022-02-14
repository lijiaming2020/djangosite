from django.contrib import admin
from .models import User_Info

# Register your models here.
@admin.register(User_Info)
class User_InfoAdmin(admin.ModelAdmin):
    pass