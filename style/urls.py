from django.urls import path
from . import views

app_name="urls"  #config에서 include에 사용할 이름 // 템플릿에서 사용할 이름


urlpatterns=[
    path('', views.StyleListView.as_view(), name="style"),
]