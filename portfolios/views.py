from django.shortcuts import render, redirect
from .models import P_templates, Mydatas, Portfolios, Pjts, Pjtimages, Links, Career, TechStack, P_templates
from .forms import BasicForm, PortfolioForm, PjtForm, PjtImageForm, DeletePjtImageForm, LinkForm, CareerForm
from accounts.models import User
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
    my_data = Mydatas.objects.get(title=mydata_title, user_id=request.user.id)
    my_data_stacks = [stack.stack for stack in my_data.stack.all()]
    my_pjts = Pjts.objects.filter(mydata=my_data)
    my_careers = list(Career.objects.filter(mydata=my_data))
    my_links = list(Links.objects.filter(mydata=my_data))

    if request.method == 'POST':
        basic = BasicForm(request.POST, request.FILES, instance=my_data)
        update_pjt_ids = [k.split('-')[1] for k in request.POST if k.startswith('pjt-') and k.endswith('name')]
        # Delete pjts
        for my_pjt_id in [my_pjt.id for my_pjt in my_pjts]:
            if str(my_pjt_id) not in update_pjt_ids:
                Pjts.objects.get(id=my_pjt_id).delete()

        if basic.is_valid():
            # Update basic information
            my_data = basic.save(commit=False)
            my_data.user = request.user
            my_data.save()

            # Update or add stacks
            b_stacks = request.POST.getlist('b_stack_multi')
            for b_stack in b_stacks:
                my_data.stack.add(TechStack.objects.get(stack=b_stack))
            
            # Delete stacks
            for my_data_stack in my_data_stacks:
                if my_data_stack not in b_stacks:
                    my_data.stack.remove(TechStack.objects.get(stack=my_data_stack))

            # Update or add projects
            for i, pjt_id in enumerate(update_pjt_ids):
                pjt_instance = Pjts.objects.filter(pk=pjt_id).first()
                pjt_form = PjtForm(request.POST, prefix=f'pjt-{pjt_id}', instance=pjt_instance)
                pjt_image_form = PjtImageForm(request.POST, request.FILES, prefix=f'pjt-{pjt_id}')
                pjt_stack_form = [stack.stack for stack in pjt_instance.stack.all()] if pjt_instance else []

                if pjt_form.is_valid():
                    pjt_instance = pjt_form.save(commit=False)
                    pjt_instance.mydata = my_data
                    pjt_instance.save()

                    # Add stack
                    p_stacks = request.POST.getlist(f'p_stack_multi-{i}')
                    for p_stack in p_stacks:
                        pjt_instance.stack.add(TechStack.objects.get(stack=p_stack))
                    
                    # Delete stack
                    for my_pjt_stack in pjt_stack_form:
                        if my_pjt_stack not in p_stacks:
                            pjt_instance.stack.remove(TechStack.objects.get(stack=my_pjt_stack))
                    
                    # Add images
                    if pjt_image_form.is_valid():
                        images = request.FILES.getlist(f'pjt-{pjt_instance.id}-image') or request.FILES.getlist(f'pjt-{i}-image')
                        for image in images:
                            Pjtimages.objects.create(image=image, mydata=my_data, pjt=pjt_instance)
                    
                    # Delete images
                    pjt_image_delete_form = DeletePjtImageForm(prefix=f'delete-pjt-{pjt_id}', pjt=pjt_instance, data=request.POST)
                    if pjt_instance and pjt_image_delete_form.is_valid():
                        pjt_instance.pjtimages_set.filter(pk__in=pjt_image_delete_form.cleaned_data['delete_images']).delete()

            # Update or add careers
            update_career_ids = [k.split('-')[1] for k in request.POST if k.startswith('career-') and k.endswith('career_content')]
            for career_id in update_career_ids:
                c_form = CareerForm(request.POST, prefix=f'career-{career_id}', instance=Career.objects.filter(pk=career_id).first())
                if c_form.is_valid():
                    name = c_form.cleaned_data['career_content']
                    if name:
                        career_instance = c_form.save(commit=False)
                        career_instance.mydata = my_data
                        career_instance.save()
            
            # Delete careers
            for career in my_careers:
                if str(career.id) not in update_career_ids:
                    career.delete()

            # Update or add links
            update_link_ids = [k.split('-')[1] for k in request.POST if k.startswith('link-') and k.endswith('link_content')]
            for link_id in update_link_ids:
                l_form = LinkForm(request.POST, prefix=f'link-{link_id}', instance=Links.objects.filter(pk=link_id).first())
                if l_form.is_valid():
                    link_instance = l_form.save(commit=False)
                    if link_instance.link_content:
                        link_instance.mydata = my_data
                        link_instance.save()
            
            # Delete links
            for link in my_links:
                if str(link.id) not in update_link_ids:
                    link.delete()

            return redirect('accounts:profile', request.user.pk)

    else:
        basic = BasicForm(instance=my_data)
        pjts = [[
                PjtForm(prefix=f'pjt-{pjt.id}', instance=pjt),
                PjtImageForm(prefix=f'pjt-{pjt.id}'),
                DeletePjtImageForm(prefix=f'delete-pjt-{pjt.id}', pjt=pjt),
                [stack.stack for stack in pjt.stack.all()]] 
                for pjt in my_pjts] or [[PjtForm(prefix='pjt-0'), PjtImageForm(prefix='pjt-0')]]
        careers = [CareerForm(prefix=f'career-{str(career.id)}', instance=career) for career in my_careers] or [CareerForm(prefix='career-0')]
        links = [LinkForm(prefix=f'link-{str(link.id)}', instance=link) for link in my_links] or [LinkForm(prefix='link-0')]

    context = {
        'stacks': TechStack.STACK_CHOICES,
        'my_data': my_data,
        'basic': basic,
        'pjts': pjts,
        'careers': careers,
        'links': links,
        'my_data_stacks': my_data_stacks,
    }
    return render(request, 'portfolios/m_update.html', context)


@login_required
def m_delete(request, mydata_title):
    my_data = Mydatas.objects.get(title=mydata_title)
    if request.user == my_data.user:
        my_data.delete()
    return redirect('accounts:profile', request.user.pk)


@login_required
def p_create(request, template_name):
    test_mydata = Mydatas.objects.get(user_id=User.objects.get(username='admin'))
    mydata = Mydatas.objects.filter(user_id=request.user.id)
    selected_data = request.GET.get('data_title', '포트폴리오 예시')
    if selected_data == '포트폴리오 예시':
        selected_mydata = Mydatas.objects.get(user_id=User.objects.get(username='admin'))
    else:
        selected_mydata = Mydatas.objects.get(user_id=request.user.id, title=selected_data)
    selected_mydata_stacks = [stack.stack for stack in selected_mydata.stack.all()]
    my_pjts = Pjts.objects.filter(mydata=selected_mydata)
    selected_my_careers = list(Career.objects.filter(mydata=selected_mydata))
    selected_my_links = list(Links.objects.filter(mydata=selected_mydata))
    if request.method == 'POST':
        basic = BasicForm(request.POST, request.FILES, instance=selected_mydata)
        portfolio = PortfolioForm()
        update_pjt_ids = [k.split('-')[1] for k in request.POST if k.startswith('pjt-') and k.endswith('name')]
        update_career_ids = [k.split('-')[1] for k in request.POST if k.startswith('career-') and k.endswith('career_content')]
        update_link_ids = [k.split('-')[1] for k in request.POST if k.startswith('link-') and k.endswith('link_content')]

        if basic.is_valid():
            # Update basic information
            portfolio_data = portfolio.save(commit=False)
            portfolio_data.user = request.user
            portfolio_data.title = basic.cleaned_data['title']
            portfolio_data.username = basic.cleaned_data['username']
            portfolio_data.image = basic.cleaned_data['image']
            portfolio_data.job = basic.cleaned_data['job']
            portfolio_data.phone = basic.cleaned_data['phone']
            portfolio_data.email = basic.cleaned_data['email']
            portfolio_data.introduction = basic.cleaned_data['introduction']
            portfolio_data.template_id = P_templates.objects.get(title=template_name).id
            portfolio_data.save()

            b_stacks = request.POST.getlist('b_stack_multi')
            for b_stack in b_stacks:
                portfolio_data.stack.add(TechStack.objects.get(stack=b_stack))

            for i, pjt_id in enumerate(update_pjt_ids):
                pjt_instance = Pjts.objects.filter(pk=pjt_id).first()
                pjt_form = PjtForm(request.POST, prefix=f'pjt-{pjt_id}', instance=pjt_instance)
                new_pjt = PjtForm()
                pjt_image_form = PjtImageForm(request.POST, request.FILES, prefix=f'pjt-{pjt_id}')

                if pjt_form.is_valid():
                    pjt_data = new_pjt.save(commit=False)
                    pjt_data.name = pjt_form.cleaned_data['name']
                    pjt_data.pjts_content = pjt_form.cleaned_data['pjts_content']
                    pjt_data.role = pjt_form.cleaned_data['role']
                    pjt_data.github = pjt_form.cleaned_data['github']
                    pjt_data.web = pjt_form.cleaned_data['web']
                    pjt_data.portfolio_id = portfolio_data.id
                    pjt_data.save()

                    # Add stack
                    p_stacks = request.POST.getlist(f'p_stack_multi-{i}')
                    for p_stack in p_stacks:
                        pjt_data.stack.add(TechStack.objects.get(stack=p_stack))
                    
                    # Add images
                    if pjt_image_form.is_valid():
                        images = request.FILES.getlist(f'pjt-{pjt_instance.id}-image') or request.FILES.getlist(f'pjt-{i}-image')
                        for image in images:
                            Pjtimages.objects.create(image=image, portfolio=portfolio_data, pjt=pjt_data)

                        pjt_image_delete_form = DeletePjtImageForm(prefix=f'delete-pjt-{pjt_id}', pjt=pjt_instance, data=request.POST)
                        if pjt_instance and pjt_image_delete_form.is_valid():
                            for image in pjt_instance.pjtimages_set.exclude(pk__in=pjt_image_delete_form.cleaned_data['delete_images']):
                                Pjtimages.objects.create(image=image.image, portfolio=portfolio_data, pjt=pjt_data)
            
            # 커리어 저장
            for career_id in update_career_ids:
                c_form = CareerForm(request.POST, prefix=f'career-{career_id}', instance=Career.objects.filter(pk=career_id).first())
                if c_form.is_valid():
                    c_content = c_form.cleaned_data['career_content']
                    if c_content:
                        Career.objects.create(career_content=c_content, portfolio=portfolio_data)
            
            # 링크 저장
            for link_id in update_link_ids:
                l_form = LinkForm(request.POST, prefix=f'link-{link_id}', instance=Links.objects.filter(pk=link_id).first())
                if l_form.is_valid():
                    l_content = l_form.cleaned_data['link_content']
                    if l_content:
                        Links.objects.create(link=l_form.cleaned_data['link'], link_content=l_content, portfolio=portfolio_data)

        return redirect('accounts:profile', request.user.pk)
    else:
        basicform = BasicForm(instance=selected_mydata)
        pjtsform = [[
                PjtForm(prefix=f'pjt-{pjt.id}', instance=pjt),
                PjtImageForm(prefix=f'pjt-{pjt.id}'),
                DeletePjtImageForm(prefix=f'delete-pjt-{pjt.id}', pjt=pjt),
                [stack.stack for stack in pjt.stack.all()]] 
                for pjt in my_pjts] or [[PjtForm(prefix='pjt-0'), PjtImageForm(prefix='pjt-0')]]
        careersform = [CareerForm(prefix=f'career-{str(career.id)}', instance=career) for career in selected_my_careers] or [CareerForm(prefix='career-0')]
        linksform = [LinkForm(prefix=f'link-{str(link.id)}', instance=link) for link in selected_my_links] or [LinkForm(prefix='link-0')]
            
    context = {
        'test_mydata': test_mydata,
        'mydata': mydata,
        'selected_data': selected_data,
        'selected_mydata': selected_mydata,
        'stacks': TechStack.STACK_CHOICES,
        'basicform': basicform,
        'pjtsform': pjtsform,
        'careersform': careersform,
        'linksform': linksform,
        'selected_mydata_stacks': selected_mydata_stacks,
    }
    return render(request, f'portfolios/temp_portfolio/{template_name}.html', context)


@login_required
def p_detail(request, portfolio_name):
    my_portfolio = Portfolios.objects.get(user=request.user, title=portfolio_name)
    my_portfolio_stacks = [stack.stack for stack in my_portfolio.stack.all()]
    my_careers = list(Career.objects.filter(portfolio=my_portfolio))
    my_links = list(Links.objects.filter(portfolio=my_portfolio))
    pjts = [
        [my_pjt,
        Pjtimages.objects.filter(portfolio=my_portfolio, pjt=my_pjt),
        [stack.stack for stack in my_pjt.stack.all()]]
        for my_pjt in Pjts.objects.filter(portfolio=my_portfolio)
    ]
    context = {
        'my_portfolio': my_portfolio,
        'pjts': pjts,
        'careers': my_careers,
        'links': my_links,
        'my_portfolio_stacks': my_portfolio_stacks,
    }
    return render(request, f'portfolios/p_detail.html', context)


@login_required
def p_update(request, portfolio_name):
    my_portfolio = Portfolios.objects.get(title=portfolio_name, user=request.user)
    my_portfolio_stacks = [stack.stack for stack in my_portfolio.stack.all()]
    my_pjts = Pjts.objects.filter(portfolio=my_portfolio)
    my_careers = list(Career.objects.filter(portfolio=my_portfolio))
    my_links = list(Links.objects.filter(portfolio=my_portfolio))

    if request.method == 'POST':
        portfolio = PortfolioForm(request.POST, request.FILES, instance=my_portfolio)
        update_pjt_ids = [k.split('-')[1] for k in request.POST if k.startswith('pjt-') and k.endswith('name')]

        # Delete pjts
        for my_pjt_id in [my_pjt.id for my_pjt in my_pjts]:
            if str(my_pjt_id) not in update_pjt_ids:
                Pjts.objects.get(id=my_pjt_id).delete()

        if portfolio.is_valid():
            # Update basic information
            my_portfolio = portfolio.save(commit=False)
            my_portfolio.user = request.user
            my_portfolio.save()

            # Update or add stacks
            b_stacks = request.POST.getlist('b_stack_multi')
            for b_stack in b_stacks:
                my_portfolio.stack.add(TechStack.objects.get(stack=b_stack))
            
            # Delete stacks
            for my_portfolio_stack in my_portfolio_stacks:
                if my_portfolio_stack not in b_stacks:
                    my_portfolio.stack.remove(TechStack.objects.get(stack=my_portfolio_stack))

            # Update or add projects
            for i, pjt_id in enumerate(update_pjt_ids):
                pjt_instance = Pjts.objects.filter(pk=pjt_id).first()
                pjt_form = PjtForm(request.POST, prefix=f'pjt-{pjt_id}', instance=pjt_instance)
                pjt_image_form = PjtImageForm(request.POST, request.FILES, prefix=f'pjt-{pjt_id}')
                pjt_stack_form = [stack.stack for stack in pjt_instance.stack.all()] if pjt_instance else []

                if pjt_form.is_valid():
                    pjt_instance = pjt_form.save(commit=False)
                    pjt_instance.portfolio = my_portfolio
                    pjt_instance.save()

                    # Add stack
                    p_stacks = request.POST.getlist(f'p_stack_multi-{i}')
                    for p_stack in p_stacks:
                        pjt_instance.stack.add(TechStack.objects.get(stack=p_stack))
                    
                    # Delete stack
                    for my_pjt_stack in pjt_stack_form:
                        if my_pjt_stack not in p_stacks:
                            pjt_instance.stack.remove(TechStack.objects.get(stack=my_pjt_stack))
                    
                    # Add images
                    if pjt_image_form.is_valid():
                        images = request.FILES.getlist(f'pjt-{pjt_instance.id}-image') or request.FILES.getlist(f'pjt-{i}-image')
                        for image in images:
                            Pjtimages.objects.create(image=image, portfolio=my_portfolio, pjt=pjt_instance)
                    
                    # Delete images
                    pjt_image_delete_form = DeletePjtImageForm(prefix=f'delete-pjt-{pjt_id}', pjt=pjt_instance, data=request.POST)
                    if pjt_instance and pjt_image_delete_form.is_valid():
                        pjt_instance.pjtimages_set.filter(pk__in=pjt_image_delete_form.cleaned_data['delete_images']).delete()

            # Update or add careers
            update_career_ids = [k.split('-')[1] for k in request.POST if k.startswith('career-') and k.endswith('career_content')]
            for career_id in update_career_ids:
                c_form = CareerForm(request.POST, prefix=f'career-{career_id}', instance=Career.objects.filter(pk=career_id).first())
                if c_form.is_valid():
                    name = c_form.cleaned_data['career_content']
                    if name:
                        career_instance = c_form.save(commit=False)
                        career_instance.portfolio = my_portfolio
                        career_instance.save()
            
            # Delete careers
            for career in my_careers:
                if str(career.id) not in update_career_ids:
                    career.delete()

            # Update or add links
            update_link_ids = [k.split('-')[1] for k in request.POST if k.startswith('link-') and k.endswith('link_content')]
            for link_id in update_link_ids:
                l_form = LinkForm(request.POST, prefix=f'link-{link_id}', instance=Links.objects.filter(pk=link_id).first())
                if l_form.is_valid():
                    link_instance = l_form.save(commit=False)
                    if link_instance.link_content:
                        link_instance.portfolio = my_portfolio
                        link_instance.save()
            
            # Delete links
            for link in my_links:
                if str(link.id) not in update_link_ids:
                    link.delete()
            
            return redirect('portfolios:p_detail', portfolio_name)
    else:
        portfolioform = PortfolioForm(instance=my_portfolio)
        pjts = [[
                PjtForm(prefix=f'pjt-{pjt.id}', instance=pjt),
                PjtImageForm(prefix=f'pjt-{pjt.id}'),
                DeletePjtImageForm(prefix=f'delete-pjt-{pjt.id}', pjt=pjt),
                [stack.stack for stack in pjt.stack.all()]] 
                for pjt in my_pjts] or [[PjtForm(prefix='pjt-0'), PjtImageForm(prefix='pjt-0')]]
        careers = [CareerForm(prefix=f'career-{str(career.id)}', instance=career) for career in my_careers] or [CareerForm(prefix='career-0')]
        links = [LinkForm(prefix=f'link-{str(link.id)}', instance=link) for link in my_links] or [LinkForm(prefix='link-0')]

    context = {
        'my_portfolio': my_portfolio,
        'stacks': TechStack.STACK_CHOICES,
        'my_portfolio_stacks': my_portfolio_stacks,
        'portfolioform': portfolioform,
        'pjts': pjts,
        'careers': careers,
        'links': links,
    }
    return render(request, 'portfolios/p_update.html', context)


@login_required
def p_delete(request, portfolio_name):
    my_portfolio = Portfolios.objects.get(title=portfolio_name, user=request.user)
    if request.user == my_portfolio.user:
        my_portfolio.delete()
    return redirect('accounts:profile', request.user.pk)

