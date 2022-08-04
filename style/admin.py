from django.contrib import admin
from .models import Style, StyleImage
# Register your models here.

class StyleInline(admin.StackedInline):
    model=StyleImage
    extra=5

@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display=('__str__', 'count_products')
    inlines=[StyleInline]
    filter_horizontal=['products'] # ui변경 더블클릭시 오른쪽으로 이동함

@admin.register(StyleImage)
class StyleImageAdmin(admin.ModelAdmin):
    pass

