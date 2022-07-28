from django.urls import path
from . import views

app_name="products"  #config에서 include에 사용할 이름


urlpatterns=[
    path('', views.product_list),
]