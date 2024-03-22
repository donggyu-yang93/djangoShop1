from django.shortcuts import render, redirect
from .forms import ResigterForm, CustomUserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

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

def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            form = CustomUserChangeForm(instance=request.user)
        context = {'form': form}
        return render(request, 'registration/update.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # 암호가 변경되어도 로그아웃 되지 않음
            update_session_auth_hash(request, form.user)
            return redirect('/')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form,}
    return render(request, 'registration/change_password.html', context)

def delete(request):
    user = request.user
    user.delete()
    return redirect('/')