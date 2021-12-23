from django.db import models


# Create your models here.
class Company(models.Model):
    NOTHING = 0
    TOO = 1
    IP = 2
    AO = 3

    TYPES_CHOICES = (
        (NOTHING, 'Выберите форму предпринимательства Вашей организации'),
        (TOO, 'ТОО'),
        (IP, 'ИП'),
        (AO, 'АО'),
    )

    ALL_TYPES = (TOO, IP, AO)

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=70)
    bin_iin = models.CharField(max_length=30)
    iik = models.CharField(max_length=100)
    bik = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    type = models.IntegerField(choices=TYPES_CHOICES)

    is_init = models.BooleanField(default=False)

    user = models.ForeignKey('auth_custom.User', on_delete=models.CASCADE, related_name="_company")


class CompanyWorker(models.Model):
    CHOICE_POSITION = 0
    BACKEND = 1
    FRONTEND = 2
    DESIGNER = 3

    POSITION_CHOICES = (
        (CHOICE_POSITION, 'Выберите должность'),
        (BACKEND, 'Back-end программист'),
        (FRONTEND, 'Front-end программист'),
        (DESIGNER, 'Web - дизайнер'),
    )

    ALL_POSITIONS = (CHOICE_POSITION,
                     BACKEND,
                     FRONTEND,
                     DESIGNER,
                     )

    position = models.IntegerField(choices=POSITION_CHOICES)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)


class BusinessCenter(models.Model):
    NOTHING = 0
    ALMALINSK = 1
    BOSTANTIK = 2

    REGION_CHOICES = (
        (NOTHING, 'Выберите р-н БЦ'),
        (ALMALINSK, 'Аламалинский р-н'),
        (BOSTANTIK, 'Бостандыкский р-н'),
    )

    ALL_REGIONS = (NOTHING, ALMALINSK, BOSTANTIK)

    name = models.CharField(max_length=50)
    region = models.IntegerField(choices=REGION_CHOICES)
    address = models.CharField(max_length=50)

    url = models.CharField(max_length=240)


class BusinessCenterOffice(models.Model):
    business_center = models.ForeignKey('BusinessCenter', on_delete=models.CASCADE, related_name='offices')

    url = models.CharField(max_length=240)

    room = models.IntegerField()
    area = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField()


class BusinessCenterOfficeToCompany(models.Model):
    offices = models.ForeignKey('BusinessCenterOffice', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)


class Things(models.Model):
    TABLE = 1
    PC = 2

    TYPE_CHOICES = (
        (TABLE, 'Стол'),
        (PC, 'Компьютер'),
    )

    CHOICE_POSITION = 0
    BACKEND = 1
    FRONTEND = 2
    DESIGNER = 3
    ALL = 4

    POSITION_CHOICES = (
        (CHOICE_POSITION, 'Выберите должность'),
        (BACKEND, 'Back-end программист'),
        (FRONTEND, 'Front-end программист'),
        (DESIGNER, 'Web - дизайнер'),
        (ALL, 'Для всех')
    )

    name = models.CharField(max_length=40)
    url = models.CharField(max_length=240)
    description = models.TextField()
    price = models.IntegerField()
    distributor = models.CharField(max_length=60)

    type = models.IntegerField(choices=TYPE_CHOICES)
    for_position = models.IntegerField(choices=POSITION_CHOICES)


class ThingToCompany(models.Model):
    thing = models.ForeignKey(Things, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Order(models.Model):
    NOT_READY = 0
    SUCCESS = 1
    DENIED = 2
    WAITING = 3

    STATUS_CHOICES = ((NOT_READY, 'Еще не соствавлен'),
                      (SUCCESS, 'Одобренно'),
                      (DENIED, 'Отклоненно'),
                      (WAITING, 'В ожидании'))

    status = models.IntegerField(choices=STATUS_CHOICES, default=WAITING)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)


class OfficesToOrder(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name='orders_to_order')
    office = models.ForeignKey("BusinessCenterOffice", on_delete=models.CASCADE)


class ThingsToOrder(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name='things_to_order')
    things = models.ForeignKey("Things", on_delete=models.CASCADE)
