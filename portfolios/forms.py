from django import forms
from .models import TechStack, P_templates, Portfolios, Career, Pjts, Pjtimages, Mydatas, Links
from accounts.models import User
from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill
import os
from django.conf import settings
from django.core.validators import URLValidator
from django.forms.widgets import ClearableFileInput

# BasicForm, PortfolioForm 중복을 피하기 위한 BaseForm

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'portfolios/custom_clearable_file_input.html'

class BaseForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '포트폴리오 제목',
                'class' : 'basic--form',
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '이름',
                'class' : 'basic--form',
            }
        )
    )

    image = ProcessedImageField(
        widget=CustomClearableFileInput(
            attrs={
                'placeholder': '프로필 이미지',
                'class' : 'basic--img--form',
            }
        ),
        spec_id='image_size',
    )

    job = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '직무',
                'class' : 'basic--form',
            }
        )
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '휴대폰 번호',
                'class' : 'basic--form',
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': '이메일',
                'class' : 'basic--form',
            }
        )
    )

    introduction = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': '내 소개글(500자 이내)',
                'class' : 'basic--form',
            }
        )
    )

    class Meta:
        abstract = True
        fields = ('title', 'username', 'image', 'job', 'phone', 'email', 'introduction')


class BasicForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Mydatas

    def __init__(self, *args, **kwargs):
        super(BasicForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
                
        if instance and instance.image:
            self.fields['image'].initial = instance.image.url


class PortfolioForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Portfolios


class PjtForm(forms.ModelForm):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '프로젝트 제목',
                'class':'pjt--form',
            }
        )
    )

    pjts_content = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': '설명',
                'class':'pjt--form',
            }
        )
    )

    role = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': '역할 및 기능',
                'class':'pjt--form',
            }
        )
    )

    github = forms.URLField(
        required=False,
        validators=[URLValidator()],
        widget=forms.URLInput(
            attrs={
                'placeholder': 'github url',
                'class':'pjt--form',
            }
        )
    )

    web = forms.URLField(
        required=False,
        validators=[URLValidator()],
        widget=forms.URLInput(
            attrs={
                'placeholder': 'web url',
                'class':'pjt--form',
            }
        )
    )
    
    class Meta:
        model = Pjts
        fields = ('name', 'pjts_content', 'role', 'github', 'web',)

class PjtImageForm(forms.ModelForm):
    image = forms.FileField(
        label=False,
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True, 
                'placeholder': '프로젝트 이미지',
                'id': 'image-upload-0',
                'style': 'display:none;',
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
        widget=forms.CheckboxSelectMultiple(
        ),
        choices=[]
    )

    def __init__(self, pjt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete_images'].choices = [
            (image.pk, image.image.url) for image in Pjtimages.objects.filter(pjt=pjt)
        ]

    def clean(self):
        cleaned_data = super().clean()
        delete_ids = cleaned_data.get('delete_images')
        if delete_ids:
            images = Pjtimages.objects.filter(pk__in=delete_ids)
            for image in images:
                os.remove(os.path.join(settings.MEDIA_ROOT, image.image.path))
            images.delete()

class CareerForm(forms.ModelForm):
    career_content = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '경력',
                'class': 'career--content',
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
                'class':'link--content',
            }
        )
    )

    link_content = forms.URLField(
        required=False,
        validators=[URLValidator()],
        widget=forms.URLInput(
            attrs={
                'placeholder': 'url',
                'class':'link--content',
                'style': 'width:80%; margin-right:10px;'
            }
        )
    )
    class Meta:
        model = Links
        fields = ('link', 'link_content',)