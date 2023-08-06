from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label = '이메일',
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '이메일',
            }
        )
    )
    # username = forms.CharField(
    #     label='이름',
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': '유저네임',
    #         }
    #     )
    # )
    password1 = forms.CharField(
        label = '비밀번호',
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '비밀번호',
            }
        ),
    )

    password2 = forms.CharField(
        label = '비밀번호 확인',
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '비밀번호 확인',
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'image',)


class CustomAuthenticationForm(AuthenticationForm):
    # username = forms.CharField(required=False)
    username = forms.EmailField(
        label = False,
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '이메일',
            }
        )
    )

    password = forms.CharField(
        label = False,
        widget = forms.PasswordInput(
            attrs = {
                'class':'form-control',
                'placeholder': '비밀번호',
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password',)


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(
        label = False,
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '이메일',
            }
        )
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email', 'image',)


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password2',)
    old_password = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'signup--form','placeholder' : '기존 비밀번호'}))
    new_password1 = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'signup--form','placeholder' : '새 비밀번호'}))
    new_password2 = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'signup--form','placeholder' : '새 비밀번호 확인'}))