from django.contrib import admin
from .models import List
# Register your models here.

@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    filter_horizontal = ("products",)  #어떻게 보여줄 것인지 
    list_display= ("__str__", "count_products")