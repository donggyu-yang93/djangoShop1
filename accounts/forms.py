from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

# 폼 : 폼태그 ㅡㅡ HTML 태그 ㅡㅡ 프론트 단에서 사용자의 입력을 받는 인터페이스
# 장고의 폼 : HTML의 폼 역할, DB에 저장할 내용을 형식과 제약조건 결정


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'username')

class ResigterForm(forms.ModelForm):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput) # passwordInput이 비밀번호 안보이게 하는 그거
    password2 = forms.CharField(label='비밀번호 재입력', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data # SQL인젝션방지
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호가 서로 다릅니다.')
        return cd['password2']