import os
import requests
from uuid import uuid4
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import authenticate, login, logout
from users.models import User
from  django.views.generic import FormView
from users import forms, models
from django.urls import reverse_lazy
# Create your views here.


# def login_view(request):
#     if request.method == 'GET':
#         pass
#     if request.method == 'POST':
#         email= request.POST.get('email')
#         password=request.POST.get('password')
#         user=authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect(resolve_url('products:search')) # resolve를 쓰면 템플릿 태그처럼 주소값을 사용할수있다.
#     return render(request, 'users/login.html')

# def logout_view(request):
#     logout(request)
#     return redirect(resolve_url('products:search'))



class login_view(FormView):
    form_class= forms.LoginForm
    template_name='users/login.html'
    success_url=reverse_lazy('products:search')
    
    def form_valid(self, form):
        email=form.cleaned_data.get('email')  # 클래스로 만들 경우 form_valid는 form이 유효한 경우 발생되는 함수 // cleaned_data는 정제해주는 메서드
        password=form.cleaned_data.get('password')
        user=authenticate(self.request, username=email,password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
def logout_view(request):
    logout(request)
    return redirect(resolve_url('users:login'))

class SignUpView(FormView): # 회원가입 후 바로 로그인까지 시키려면 template_name도 바꾸고 form_valid에서 로그인에 필요한 걸 가져오면 가능
    template_name='users/signup.html'
    form_class=forms.SignUpForm
    success_url=reverse_lazy('users:login')
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def kakao_login(request):
    REST_API_KEY=os.environ.get('KAKAO_REST_API_KEY')
    REDIRECT_URI= 'http://127.0.0.1:8000/users/login/kakao/callback'
    return redirect(f'https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code')


class KakaoException(Exception):
    pass

def kakao_callback(request):
    try:
        code = request.GET.get('code')
        client_id =os.environ.get('KAKAO_REST_API_KEY')
        redirect_uri= 'http://127.0.0.1:8000/users/login/kakao/callback'
        token_requests = requests.get(f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}')
        token_json = token_requests.json()
        error = token_json.get('error', None)

        if error is not None:
            raise KakaoException()
        
        access_token=token_json.get('access_token')

        profile_request = requests.get(f'https://kapi.kakao.com/v2/user/me', headers={'Authorization': f'Bearer {access_token}'})

        profile_json=profile_request.json()
        kakao_account = profile_json.get('kakao_account')
        email = kakao_account.get('email', None)

        if email is None:
            email = f'{uuid4.hex}@kakao.com'



        nickname = kakao_account.get('profile').get('nickname')
        profile_image = kakao_account.get('profile').get('profile_image_url')
        

        try:
            user=models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                username = email,
                email = email,
                first_name = nickname,
                phone_number = '01000000000',
            )
            user.set_unusable_password()
            user.save()
        
        login(request, user)
        return redirect(resolve_url('products:search'))

        

    except KakaoException:
        return redirect(resolve_url('users:login'))