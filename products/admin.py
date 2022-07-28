from django.contrib import admin
from .models import Product, Brand, Photo




# Register your models here.

class PhotoInline(admin.StackedInline): # 이걸 해당 어드민의 inlines에 넣으면 새로 만들기에서 항목이 추가됨   // TabularInline 혹은 StackedInline도 있음
    model=Photo
    extra=1 # 사진 개수


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("brand", "name_en", "name_ko") # 어드민 프로덕트 리스트들의 항목
    search_fields = ("brand__name", "name_en","name_ko", )
                        #그냥 brand로만 서치필드에 넣으면 원래는 객체이름을 가지고 있기 때문에 brand__변수명 을 해줘야 검색이 됨 Product인데 brand에 접속 가능한건 외래키 덕
    inlines=[PhotoInline]



@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass