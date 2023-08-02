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
        update_pjt_ids = [k.split('-')[1] for k in request.POST if k.startswith('pjt-') and k.endswith('name')]
        update_pjts = []
        my_pjts_id = [ my_pjt.id for my_pjt in my_pjts ]
        for my_pjt_id in my_pjts_id:
            if str(my_pjt_id) not in update_pjt_ids:
                Pjts.objects.get(id=my_pjt_id).delete()
        for pjt_id in update_pjt_ids:
            pjt_instance = None
            try:
                pjt_instance = Pjts.objects.get(pk=pjt_id)
            except Pjts.DoesNotExist:
                pass
            if pjt_instance:
                pjt_form = PjtForm(request.POST, prefix=f'pjt-{pjt_id}', instance=pjt_instance)
                pjt_image_form = PjtImageForm(request.POST, request.FILES, prefix=f'pjt-{pjt_id}')
                pjt_image_delete_form = DeletePjtImageForm(prefix=f'delete-pjt-{pjt_id}', pjt=pjt_instance, data=request.POST) 
                pjt_stack_form = [stack.stack for stack in pjt_instance.stack.all()]
            else:
                pjt_form = PjtForm(request.POST, prefix=f'pjt-{pjt_id}')
                pjt_image_form = PjtImageForm(request.POST, request.FILES, prefix=f'pjt-{pjt_id}')
                pjt_image_delete_form = False
                pjt_stack_form = []

            update_pjts.append([pjt_form, pjt_image_form, pjt_image_delete_form, pjt_stack_form])


        update_career_ids = [k.split('-')[1] for k in request.POST if k.startswith('career-') and k.endswith('career_content')]
        update_careers = []
        for career_id in update_career_ids:
            career_instance = None
            try:
                career_instance = Career.objects.get(pk=career_id)
            except Career.DoesNotExist:
                pass

            if career_instance:
                career_form = CareerForm(request.POST, prefix=f'career-{career_id}', instance=career_instance)
            else:
                career_form = CareerForm(request.POST, prefix=f'career-{career_id}')

            update_careers.append(career_form)

        update_link_ids = [k.split('-')[1] for k in request.POST if k.startswith('link-') and k.endswith('link_content')]
        update_links = []
        for link_id in update_link_ids:
            link_instance = None
            try:
                link_instance = Links.objects.get(pk=link_id)
            except Links.DoesNotExist:
                pass

            if link_instance:
                link_form = LinkForm(request.POST, prefix=f'link-{link_id}', instance=link_instance)
            else:
                link_form = LinkForm(request.POST, prefix=f'link-{link_id}')

            update_links.append(link_form)

        if basic.is_valid():
            # Update basic information
            my_data = basic.save(commit=False)
            my_data.user = request.user
            my_data.save()
            b_stacks = request.POST.getlist('b_stack_multi')
            for b_stack in b_stacks:
                my_data.stack.add(TechStack.objects.get(stack=b_stack))
            
            for my_data_stack in my_data_stacks:
                if my_data_stack not in b_stacks:
                    my_data.stack.remove(TechStack.objects.get(stack=my_data_stack))

            # Update or add projects
            for i, (p_form, pjt_image_form, delete_pjt_image_form, p_stack_list) in enumerate(update_pjts):
                if p_form.is_valid():
                    pjt_instance = p_form.save(commit=False)
                    pjt_instance.mydata = my_data
                    pjt_instance.save()

                    p_stacks = request.POST.getlist(f'p_stack_multi-{i}')
                    for p_stack in p_stacks:
                        pjt_instance.stack.add(TechStack.objects.get(stack=p_stack))
                    
                    for my_pjt_stack in p_stack_list:
                        if my_pjt_stack not in p_stacks:
                            pjt_instance.stack.remove(TechStack.objects.get(stack=my_pjt_stack))
                    
                    # Handle project images
                    if pjt_image_form.is_valid():
                        images = request.FILES.getlist(f'pjt-{pjt_instance.id}-image')
                        if images:
                            pass
                        else:
                            images = request.FILES.getlist(f'pjt-{i}-image')
                        for image in images:
                            Pjtimages.objects.create(image=image, mydata=my_data, pjt=pjt_instance)

                    delete_ids = request.POST.getlist('delete_images')

                    # Handle deleted project images
                    if delete_pjt_image_form:
                        if delete_pjt_image_form.is_valid():
                            pjt_instance.pjtimages_set.filter(pk__in=delete_ids).delete()

            # Update or add careers
            for c_form in update_careers:
                if c_form.is_valid():
                    career_instance = c_form.save(commit=False)
                    if career_instance.career_content:
                        career_instance.mydata = my_data
                        career_instance.save()
            
            # Delete careers
            for career in my_careers:
                if str(career.id) not in update_career_ids:
                    career.delete()

            # Update or add links
            for l_form in update_links:
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
        pjts = [[PjtForm(prefix=f'pjt-{pjt.id}', instance=pjt),
                PjtImageForm(prefix=f'pjt-{pjt.id}'),
                DeletePjtImageForm(prefix=f'delete-pjt-{pjt.id}', pjt=pjt),
                [stack.stack for stack in pjt.stack.all()]] for pjt in my_pjts]
        if not pjts:
            pjts = [[PjtForm(prefix='pjt-0'), PjtImageForm(prefix='pjt-0'), DeletePjtImageForm(prefix='pjt-0'), []]]
        careers = [CareerForm(prefix=f'career-{str(career.id)}', instance=career) for career in my_careers]
        if not careers:
            careers = [CareerForm(prefix='career-0')]
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
    test_mydata = Mydatas.objects.get(user_id=9)
    mydata = Mydatas.objects.filter(user_id=request.user.id)
    selected_data = None
    selected_mydata = Mydatas.objects.get(user_id=9)
    if request.method == 'POST':
        selected_mydata = Mydatas.objects.get(user_id=request.user.id, title=selected_data)
        
    else:
        selected_data = request.GET.get('data_title', '개발자정토리')
        if selected_data == '개발자정토리':
            selected_mydata = Mydatas.objects.get(user_id=9)
        else:
            selected_mydata = Mydatas.objects.get(user_id=request.user.id, title=selected_data)
            
    mylinks = selected_mydata.links_set.all()
    mycareers = selected_mydata.career_set.all()
    mypjts = selected_mydata.pjts_set.all()
    # mydata_title = 
    # my_data = Mydatas.objects.get(title=mydata_title)
    context = {
        'test_mydata': test_mydata,
        'mydata': mydata,
        'selected_data': selected_data,
        'selected_mydata': selected_mydata,
        'mylinks': mylinks,
        'mycareers': mycareers,
        'mypjts': mypjts,
    }
    return render(request, f'portfolios/{template_name}.html', context)


@login_required
def p_detail(request, portfolio_pk):
    return


@login_required
def p_update(request, portfolio_pk):
    return


@login_required
def p_delete(request, portfolio_pk):
    return



