from django.shortcuts import render, redirect
from .models import P_templates, Mydatas, Portfolios, Pjts, Pjtimages, Links, Career, TechStack
from .forms import BasicForm, PortfolioForm, PjtForm, PjtImageForm, DeletePjtImageForm, LinkForm, CareerForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

PjtImageFormSet = formset_factory(PjtImageForm, extra=1)

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


@login_required
def m_create(request):
    if request.method == 'POST':
        basic = BasicForm(request.POST, request.FILES)
        pjt = [PjtForm(request.POST, prefix=f'pjt-{i}') for i in range(int([k for k in request.POST if k.startswith('pjt-')][-1][4])+1)]
        career = [CareerForm(request.POST, prefix=f'career-{i}') for i in range(int([k for k in request.POST if k.startswith('career-')][-1][7])+1)]
        link = [LinkForm(request.POST, prefix=f'link-{i}') for i in range(int([k for k in request.POST if k.startswith('link-')][-1][5])+1)]
        pjtimage = [PjtImageForm(request.POST, request.FILES, prefix=f'pjt-{i}') for i in range(int([k for k in request.POST if k.startswith('pjt-')][-1][4])+1)]

        if basic.is_valid():
            title = basic.cleaned_data.get('title')
            if Mydatas.objects.filter(title=title, user=request.user).exists():
                message = '이미 생성된 정보입니다.'
                messages.error(request, message)
                return redirect('accounts:profile', request.user.pk)
            
            my_data = basic.save(commit=False)
            my_data.user = request.user
            my_data.save()
            b_stacks = request.POST.getlist('b_stack_multi')
            for b_stack in b_stacks:
                my_data.stack.add(TechStack.objects.get(stack=b_stack))

            for i, p_form in enumerate(pjt):
                if p_form.is_valid():
                    name = p_form.cleaned_data['name']
                    # pjt 저장
                    if name:
                        my_pjt = p_form.save(commit=False)
                        my_pjt.mydata = my_data
                        my_pjt.save()

                        # 기술 스택 저장
                        for p_stack in request.POST.getlist(f'p_stack_multi-{i}'):
                            my_pjt.stack.add(TechStack.objects.get(stack=p_stack))
                    
                        # 다중이미지 저장
                        if pjtimage[i].is_valid():
                            images = request.FILES.getlist(f'pjt-{i}-image')
                            if images:
                                for image in images:
                                    Pjtimages.objects.create(image=image, mydata=my_data, pjt=my_pjt)
    
            for c_form in career:
                if c_form.is_valid():
                    name = c_form.cleaned_data['career_content']
                    if name:
                        my_career = c_form.save(commit=False)
                        my_career.mydata = my_data
                        my_career.save()

            for l_form in link:
                if l_form.is_valid():
                    name = l_form.cleaned_data['link_content']
                    if name:
                        my_link = l_form.save(commit=False)
                        my_link.mydata = my_data
                        my_link.save()

            return redirect('accounts:profile', request.user.pk)
    else:
        basic = BasicForm()
        pjt = PjtForm(prefix='pjt-0')
        pjtimage = PjtImageForm(prefix='pjt-0')
        career = CareerForm(prefix='career-0')
        link = LinkForm(prefix='link-0')
        
    context = {
        'stacks': TechStack.STACK_CHOICES,
        'basic': basic,
        'pjt': pjt,
        'pjtimage': pjtimage,
        'career': career,
        'link': link,
    }
    return render(request, 'portfolios/m_create.html', context)


def check(request):
    title = request.GET.get('title')
    pk = request.GET.get('origin_title')

    if Mydatas.objects.filter(title=title, user=request.user).exists():
        if Mydatas.objects.filter(title=title, pk=pk).exists():
            response_data = {'duplicate': False}
        else:
            response_data = {'duplicate': True}
    else:
        response_data = {'duplicate': False}
    return JsonResponse(response_data)


@login_required
def m_update(request, mydata_title):
    my_data = Mydatas.objects.get(title=mydata_title)
    my_data_stacks = [stack.stack for stack in my_data.stack.all()]
    my_pjts = Pjts.objects.filter(mydata=my_data)
    my_careers = Career.objects.filter(mydata=my_data)
    my_links = Links.objects.filter(mydata=my_data)
    if request.method == 'POST':
        basic = BasicForm(request.POST, request.FILES, instance=my_data)
        pjt = PjtForm(request.POST)
        link = [LinkForm(request.POST, prefix=f'link-{i}') for i in [k.split('-')[1] for k in request.POST if k.endswith('link_content')]]
        print("링크", link)
        print('asdasdasd', [k.split('-')[1] for k in request.POST if k.endswith('link_content')])
        # delete_ids = request.POST.getlist('delete_images')
        # delete = DeletePjtImageForm(pjt=pjt, data=request.POST)
        # if request.FILES.getlist('image'):
        #     files = request.FILES.getlist('image')
        # else:
        #     files = []
        
        career = CareerForm(request.POST)
        # link = LinkForm(request.POST)
        if basic.is_valid():
            my_data = basic.save(commit=False)
            my_data.user = request.user
            my_data.save()

            # my_pjt = pjt.save(commit=False)
            # my_pjt.mydata = my_data
            # my_pjt.save()
            # # my_pjt.pjtimages_set.filter(pk__in=delete_ids).delete()
            # if files:
            #     for i in files:
            #         Pjtimages.objects.create(image=i, pjt=my_pjt)

            # my_career = career.save(commit=False)
            # my_career.mydata = my_data
            # my_career.save()

            # for l_form in link:
            #     if l_form.is_valid():
            #         print(l_form)
            #         name = l_form.cleaned_data['link_content']
            #         print(name)
            #         if name:
            #             my_link = l_form.save(commit=False)
            #             my_link.mydata = my_data
            #             my_link.save()

            for l_form in link:
                if l_form.is_valid():
                    if l_form.cleaned_data['link_content']:
                        print(1)
                        # Handle modification of existing value
                        link_instance = l_form.save(commit=False)
                        existing_link = Links.objects.get(id=l_form.cleaned_data['id'])
                        existing_link.link_content = link_instance.link_content
                        existing_link.save()
                    else:
                        print(2)
                        # Handle new addition
                        # my_link = l_form.save(commit=False)
                        # my_link.mydata = my_data
                        # my_link.save()

            return redirect('accounts:profile', request.user.pk)
    else:
        basic = BasicForm(instance=my_data)
        pjts = [[PjtForm(prefix=str(pjt.id), instance=pjt), PjtImageForm(prefix=str(pjt.id)), DeletePjtImageForm(prefix=str(pjt.id),pjt=pjt), [stack.stack for stack in pjt.stack.all()]] for pjt in my_pjts]
        if not pjts:
            pjts = [PjtForm(prefix='link-0')]
        careers = [CareerForm(prefix=str(career.id), instance=career) for career in my_careers]
        if not careers:
            careers = [CareerForm(prefix='link-0')]
        links = [LinkForm(prefix=f'link-{str(link.id)}', instance=link) for link in my_links]
        if not links:
            links = [LinkForm(prefix='link-0')]

    context = {
        'stacks': TechStack.STACK_CHOICES,
        'my_data': my_data,
        'basic': basic,
        'pjts': pjts,
        'careers': careers,
        'links': links,
        'my_data_stacks' : my_data_stacks,
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
