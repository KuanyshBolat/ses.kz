from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout

from . import forms
from auth_custom.models import User
from business.models import Company


def login(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = forms.LoginForm()

    error = ''

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            user = User.objects.filter(email=form.data['email']).first()
            if user is not None and user.check_password(form.data['password']):
                if user.is_active:
                    django_login(request, user)
                    if not form.data.get('remember_me', False):
                        request.session.set_expiry(0)

                    return redirect('/')
                else:
                    error = 'Ваш аккаунт на данный момент не активен'
            else:
                error = 'Пользователя с такими данными не существует'

    return render(template_name='sign.html', request=request, context={'error': error, 'form': form})


def logout(request):
    if request.user.is_authenticated:
        django_logout(request)
    return redirect('/')


@transaction.atomic
def registration_company(request):
    if request.user.is_authenticated:
        return redirect('/')

    form_company = forms.CompanyForm()
    form_user = forms.UserRegistrationForm()

    if request.method == 'POST':
        form_user = forms.UserRegistrationForm(request.POST)
        form_company = forms.CompanyForm(request.POST)

        if form_user.is_valid() and form_company.is_valid():
            user = form_user.instance
            user.set_password(form_user.data['password'])
            user.is_active = False
            user.role = User.COMPANY

            company = form_company.instance
            company.user = user

            user.save()
            company.save()

            return redirect('/?registration=true')

    return render(template_name='company_sign.html', request=request,
                  context={'form_user': form_user, 'form_company': form_company, 'company_class': Company})


def registration_investor(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = forms.UserRegistrationForm()

    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.instance
            user.set_password(form.data['password'])
            user.is_active = False
            user.role = User.INVESTOR

            user.save()

            return redirect('/?registration=true')

    return render(template_name='investor_sign.html', request=request, context={'form': form})


def select_pc(request):
    return render(template_name='select_pc.html', request=request)
