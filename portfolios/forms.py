from django import forms
from .models import TechStack, P_templates, Portfolios, Career, Pjts, Pjtimages, Mydatas, Links
from accounts.models import User
from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill
import os
from django.conf import settings
from django.core.validators import URLValidator

# BasicForm, PortfolioForm 중복을 피하기 위한 BaseForm
class BaseForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '포트폴리오 제목',
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '이름',
            }
        )
    )

    image = ProcessedImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'placeholder': '프로필 이미지',
            }
        ),
        spec_id='image_size',
    )

    job = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '직무',
            }
        )
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '휴대폰 번호',
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': '이메일',
            }
        )
    )

    introduction = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': '소개',
            }
        )
    )

    class Meta:
        abstract = True
        fields = ('title', 'username', 'image', 'job', 'phone', 'email', 'introduction')


class BasicForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Mydatas


class PortfolioForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Portfolios


class PjtForm(forms.ModelForm):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '프로젝트 제목',
            }
        )
    )

    pjts_content = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': '소개',
            }
        )
    )

    role = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': '역할 및 기능',
            }
        )
    )

    github = forms.URLField(
        required=False,
        validators=[URLValidator()],
        widget=forms.URLInput(
            attrs={
                'placeholder': 'github url',
            }
        )
    )

    web = forms.URLField(
        required=False,
        validators=[URLValidator()],
        widget=forms.URLInput(
            attrs={
                'placeholder': 'web url',
            }
        )
    )
    
    class Meta:
        model = Pjts
        fields = ('name', 'pjts_content', 'role', 'github', 'web',)

class PjtImageForm(forms.ModelForm):
    image = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True, 
                'placeholder': '프로젝트 이미지',
            }
        )
    )

    class Meta:
        model = Pjtimages
        fields = ('image',)

class DeletePjtImageForm(forms.Form):
    delete_images = forms.MultipleChoiceField(
        label='삭제할 이미지 선택',
        required = False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
    )

    def __init__(self, pjt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete_images'].choices = [
            (image.pk, image.image.url) for image in Pjtimages.objects.filter(pjt=pjt)
        ]


class CareerForm(forms.ModelForm):
    career_content = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '경력',
            }
        )
    )

    class Meta:
        model = Career
        fields = ('career_content',)

class LinkForm(forms.ModelForm):
    link = forms.ChoiceField(
        choices = Links.LINK_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                'placeholder': '선택',
            }
        )
    )

    link_content = forms.URLField(
        required=False,
        validators=[URLValidator()],
        widget=forms.URLInput(
            attrs={
                'placeholder': 'url',
            }
        )
    )
    class Meta:
        model = Links
        fields = ('link', 'link_content',)