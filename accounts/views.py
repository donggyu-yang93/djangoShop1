from django.shortcuts import render
from .forms import ResigterForm
# Create your views here.
# CRUD

def register(request):
    if request.method == "POST": #회원가입 데이터 입력완료
        user_form = ResigterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,'registration/register_done.html', {'new_user':new_user})
    else:
        # 회원가입 입력하는 상황
        user_form = ResigterForm()
    return render(request, 'registration/register.html', {'form':user_form})