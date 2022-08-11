from django import forms
from . import models
from django.contrib.auth.password_validation import validate_password
class LoginForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': '예)kream@kream.co.kr', 'autoComplete': 'off'}))
    password=forms.CharField(max_length=20, required=True, widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'})) # forms.~~input안에 attrs는 html 의 style값들임

    # def clean_email(self):
    #     email=self.cleaned_data.get('email')
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError('User does not exist') # 그냥 clean 메서드는 모든 폼 값들을 수작업으로 정제하는 것/ cliean_변수명()은 지정한 변수
    def clean(self):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        try:
            user=models.User.objects.get(username=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error('password', forms.ValidationError('비밀번호가 틀립니다.'))

        except models.User.DoesNotExist:
            self.add_error('email', '없는 이메일 주소입니다.')


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields= ('email', 'first_name', 'last_name', 'phone_number')

    password=forms.CharField(max_length=20, required=True, widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))
    password1=forms.CharField(max_length=20, required=True, widget=forms.PasswordInput(attrs={'placeholder': '한번 더 입력해주세요'}))

    def clean_email(self):
        email=self.cleaned_data.get('email')
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError('이미 가입된 이메일입니다.')
        except models.User.DoesNotExist:
            return email
    def clean_password1(self):
        password=self.cleaned_data.get('password')
        password1=self.cleaned_data.get('password1')

        validate_password(password)
        if password != password1:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        else:
            return password


    
    def clean_phone_number(self):
        phone_number=self.cleaned_data.get('phone_number')
        try:
            models.User.objects.get(phone_number=phone_number)
            raise forms.ValidationError('이미 가입된 전화번호')
        except models.User.DoesNotExist:
            return phone_number

    def save(self, *args,**kwargs):
        user=super().save(commit=False) # True 하면 바로 db에 저장함. email필드를 수정하기 위해 False쓴거임
        email = self.cleaned_data.get('email')
        password= self.cleaned_data.get('password')
        user.username = email
        user.set_password(password) # 자동 해쉬화
        user.save()