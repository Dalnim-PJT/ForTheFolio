from django.shortcuts import render, redirect
from .models import P_templates, Mydatas, Portfolios, Pjts, Pjtimages, Links, Career
from .forms import BasicForm, PortfolioForm, PjtForm, PjtImageForm, DeletePjtImageForm, LinkForm, CareerForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory


# Create your views here.
def index(request):
    templates = P_templates.objects.order_by('like_users')
    context = {
        'templates':templates,
    }
    return render(request, 'portfolios/index.html',context)


# 제공하는 템플릿
# def t_detail(request, title):
#     template = P_templates.objects.get(title=title)
#     context = {
#         'template': template,
#     }
#     return render(request, f'portfolios/{title}.html', context)


def likes(request, title):
    template = P_templates.objects.get(title=title)
    if request.user in template.like_users.all():
        template.like_users.remove(request.user)
        is_liked = False
    else:
        template.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
        'likes_count': template.like_users.count(),
    }
    return JsonResponse(context)

# LinkFormSet = formset_factory(LinkForm, extra=1, prefix='link')
# CareerFormSet = formset_factory(CareerForm, extra=1, prefix='career')
# PjtFormSet = formset_factory(PjtForm, extra=1, prefix='pjt')
# PjtImageFormSet = formset_factory(PjtImageForm, extra=1, prefix='pjtimage')

@login_required
def m_create(request):
    if request.method == 'POST':
        basic = BasicForm(request.POST, request.FILES)
        pjt = [PjtForm(request.POST, prefix=f'pjt-{i}') for i in range(10)]
        # pjt = PjtForm(request.POST)
        if request.FILES.getlist('image'):
            files = request.FILES.getlist('image')
        else:
            files = []
        career = CareerForm(request.POST)
        link = LinkForm(request.POST)

        if basic.is_valid() and career.is_valid() and link.is_valid():
            my_data = basic.save(commit=False)
            my_data.user = request.user
            my_data.save()

            for form in pjt:
                if form.is_valid():
                    name = form.cleaned_data['name']
                    if name:
                        my_pjt = form.save(commit=False)
                        my_pjt.mydata = my_data
                        my_pjt.save()
                    else:
                        break

                    if files:
                        for i in files:
                            Pjtimages.objects.create(image=i, pjt=my_pjt)

            my_career = career.save(commit=False)
            my_career.mydata = my_data
            my_career.save()

            my_link = link.save(commit=False)
            my_link.mydata = my_data
            my_link.save()
            
            return redirect('accounts:profile', request.user.pk)
    else:
        basic = BasicForm()
        pjt = [PjtForm(prefix=f'pjt-{i}') for i in range(10)]
        # pjt = PjtForm(prefix='pjt-0')
        pjtimage = PjtImageForm()
        career = CareerForm()
        link = LinkForm()
            
    context = {
        'basic': basic,
        'pjt': pjt,
        'pjtimage': pjtimage,
        'career': career,
        'link': link,
    }
    return render(request, 'portfolios/m_create.html', context)


@login_required
def m_update(request, mydata_title):
    my_data = Mydatas.objects.get(title=mydata_title)
    my_pjt = Pjts.objects.filter(mydata=my_data)
    my_career = Career.objects.filter(mydata=my_data).first()
    my_link = Links.objects.filter(mydata=my_data).first()
    if request.method == 'POST':
        basic = BasicForm(request.POST, request.FILES, instance=my_data)
        pjt = PjtForm(request.POST)
        delete_ids = request.POST.getlist('delete_images')
        delete = DeletePjtImageForm(pjt=pjt, data=request.POST)
        if request.FILES.getlist('image'):
            files = request.FILES.getlist('image')
        else:
            files = []
        
        career = CareerForm(request.POST)
        link = LinkForm(request.POST)
        
        if basic.is_valid() and pjt.is_valid() and career.is_valid() and link.is_valid() and delete.ids:
            my_data = basic.save(commit=False)
            my_data.user = request.user
            my_data.save()

            my_pjt = pjt.save(commit=False)
            my_pjt.mydata = my_data
            my_pjt.save()
            my_pjt.pjtimages_set.filter(pk__in=delete_ids).delete()
            if files:
                for i in files:
                    Pjtimages.objects.create(image=i, pjt=my_pjt)

            my_career = career.save(commit=False)
            my_career.mydata = my_data
            my_career.save()

            my_link = link.save(commit=False)
            my_link.mydata = my_data
            my_link.save()
            
            return redirect('accounts:profile', request.user.pk)
    else:
        basic = BasicForm(instance=my_data)
        pjt = [PjtForm(prefix=str(pjt.id), instance=pjt) for pjt in my_pjt]
        career = CareerForm(instance=my_career)
        link = LinkForm(instance=my_link)
        # delete = DeletePjtImageForm(pjt=pjt)
    
    if my_pjt.first().pjtimages_set.exists():
        pjtimage = PjtImageForm(instance=my_pjt.first().pjtimages_set.first())
    else:
        pjtimage = PjtImageForm()
    
    context = {
        'my_data': my_data,
        'basic': basic,
        'pjt': pjt,
        'pjtimage': pjtimage,
        'career': career,
        'link': link,
        # 'delete':delete,
    }
    return render(request, 'portfolios/m_update.html', context)


@login_required
def m_delete(request, mydata_title):
    return


@login_required
def p_create(request, title):
    return


@login_required
def p_detail(request, portfolio_pk):
    return


@login_required
def p_update(request, portfolio_pk):
    return


@login_required
def p_delete(request, portfolio_pk):
    return
