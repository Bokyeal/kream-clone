from django.urls import path
from . import views

app_name="users"


urlpatterns=[
    path('login/', views.login_view.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/kakao', views.kakao_login, name='kakao_login'),
    path('login/kakao/callback', views.kakao_callback, name='kakao_callback'),
]