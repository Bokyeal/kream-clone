from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import authenticate, login, logout
from users.models import User
from  django.views.generic import FormView
from users import forms
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

class SignUpView(FormView):
    template_name='users/signup.html'
    form_class=forms.SignUpForm
    success_url=reverse_lazy('users:login')
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)