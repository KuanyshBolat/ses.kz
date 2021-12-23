from django import forms
from django.core.exceptions import ValidationError

from business.models import CompanyWorker, BusinessCenter


class CompanyWorkerForm(forms.ModelForm):
    def clean_position(self):
        position = int(self.data['position'])

        if position not in CompanyWorker.ALL_POSITIONS or position == CompanyWorker.CHOICE_POSITION:
            raise ValidationError('Выберите правильную должность')

        return position

    class Meta:
        model = CompanyWorker
        fields = ('position',)


class CompanyRegionForm(forms.Form):
    region = forms.IntegerField()

    def clean_region(self):
        region = int(self.data['region'])

        if region not in BusinessCenter.ALL_REGIONS or region == BusinessCenter.NOTHING:
            raise ValidationError('Выберите правильный район')

        return region
