from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm, CustomAuthenticationForm
from portfolios.models import Mydatas, Portfolios

# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect('main')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('main')
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('main')


def signup(request):
    if request.user.is_authenticated:
        return redirect('main')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def email_overlap_check(request):
    email = request.GET.get('email')
    try:
        user = User.objects.get(email=email)
    except:
        user = None
    if user is None:
        overlap = "pass"
    else:
        overlap = "fail"
    context = {'overlap': overlap}
    return JsonResponse(context)  


@login_required
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('main')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('accounts:profile', request.user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = CustomPasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             return redirect('main')
#     else:
#         form = CustomPasswordChangeForm(request.user)
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/change_password.html', context)


@login_required
def change_password(request):
    if request.is_ajax() and request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()

            
            update_session_auth_hash(request, user)
            return JsonResponse({"status": "success", "message": "암호가 성공적으로 변경되었습니다."}, status=200)
        else:
            errors = form.errors.as_json()
            return JsonResponse({"status": "error", "errors": errors}, status=400)
    
    # 일반 요청에 대한 처리는 이전과 동일하게 유지합니다.
    form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


# @login_required
# def profile(request, user_pk):
#     User = get_user_model()
#     person = User.objects.get(pk=user_pk)
#     mydata = Mydatas.objects.filter(user=person)
#     context = {
#         'person': person,
#         'mydata': mydata,
#     }
#     return render(request, 'accounts/profile.html', context)

@login_required
def profile(request, user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    mydata = Mydatas.objects.filter(user=person)
    myportfolio = Portfolios.objects.filter(user=person)
    user_payments = request.user.payment_set.all()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # 여기서는 프로필 편집 부분만 렌더링해서 반환하면 됩니다.
        return render(request, 'path_to_profile_edit_template.html', {'person': person})

    context = {
        'person': person,
        'mydata': mydata,
        'myportfolio': myportfolio,
        'user_payments': user_payments,
    }
    return render(request, 'accounts/profile.html', context)
