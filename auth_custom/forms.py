import re
import string

from django import forms
from django.core.exceptions import ValidationError

from business.models import Company, CompanyWorker
from auth_custom.models import User


class LoginForm(forms.ModelForm):
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('email', 'password')


class UserRegistrationForm(forms.ModelForm):
    repeat_password = forms.CharField(required=True)

    def clean_phone(self):
        phone = self.data['phone']

        is_right = True

        if len(phone) != 11:
            is_right = False
        if not all(ch in string.digits for ch in phone):
            is_right = False

        if not is_right:
            raise ValidationError("Введенный номер телефона имеет неверный формат")

        return phone

    def clean_repeat_password(self):
        password = self.data['password']
        repeat_password = self.data['repeat_password']

        if password != repeat_password:
            raise ValidationError('Введенные пароли не совпадают')

        return repeat_password

    def clean_email(self):
        email = self.data['email']

        is_right = True

        if re.match('^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$', email) is None:
            is_right = False

        elif User.objects.filter(email=email).first():
            raise ValidationError('Пользователь с такой почтой существует')

        if not is_right:
            raise ValidationError('Введенный email не правильный')

        return email

    def is_valid(self):
        is_valid = super().is_valid()
        self.instance.username = self.data['email']
        return is_valid

    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone', 'password', 'repeat_password')


class CompanyForm(forms.ModelForm):
    def clean_type(self):
        type = int(self.data['type'])

        is_right = True

        if not type:
            is_right = False

        if type not in Company.ALL_TYPES or type == 0:
            is_right = False

        if not is_right:
            raise ValidationError('Выберите корректный тип')

        return type

    def clean_bin_iin(self):
        bin_iin = self.data['bin_iin']

        is_right = True

        if len(bin_iin) != 12:
            is_right = False
        if not all(ch in string.digits for ch in bin_iin):
            is_right = False

        if not is_right:
            raise ValidationError("Введенный БИИ/ИИН имеет неверный формат")

        return bin_iin

    class Meta:
        model = Company
        fields = ('name', 'address', 'type', 'bin_iin', 'iik', 'bik', 'bank_name')


