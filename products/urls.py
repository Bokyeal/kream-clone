from django.urls import path
from . import views

app_name="products"  #config에서 include에 사용할 이름


urlpatterns=[
    # path('', views.product_list),
    path('', views.ProductListView.as_view()),
    path('test/', views.test),
    # path('<int:pk>/', views.detail, name="detail"),  # int:뒤에 이름은 자유롭게. 그 이름을 views의 인자로 사용
    path("<int:pk>", views.ProductDetail.as_view(), name="detail")
]