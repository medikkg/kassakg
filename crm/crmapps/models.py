from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from .choice import ClientTypeChoice

class Service(models.Model):
    category = models.CharField(max_length=100, null=False, blank=False, verbose_name='Категория')
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='Услуга')
    unit = models.CharField(max_length=100, null=True, blank=True, verbose_name='Единица измерения', default='штука')
    price = models.PositiveIntegerField(null=False, blank=False, verbose_name='Цена за единицу')

    def __str__(self):
        return f'{self.name}, {self.price} сом/{self.unit}'

    class Meta:
        db_table = 'service'
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Client(models.Model):
    first_name = models.CharField(max_length=70, null=False, blank=False, verbose_name='Имя клиента')
    last_name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Фамилия клиента')
    client_type = models.CharField(max_length=20, choices=ClientTypeChoice.choices, default='Физ.лицо',  null=False, blank=False, verbose_name='Тип клиента')
    phone = PhoneNumberField(region='KG', max_length=15, verbose_name='Номер телефона')
    email = models.EmailField(null=True, blank=True, verbose_name='Email')
    organization = models.CharField(max_length=255, null=True, blank=True, verbose_name='Организация')
    payment_type = models.CharField(max_length=25, null=False, blank=False, default='cash', verbose_name='Тип оплаты')

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.phone}'

    class Meta:
        db_table = 'client'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class ClientAddress(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Клиент')
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name='Город')
    micro_district = models.CharField(max_length=255, null=True, blank=True, verbose_name='Микрорайон, ж/м, ж/к')
    street = models.CharField(max_length=255, null=True, blank=True, verbose_name='Улица')
    house = models.CharField(max_length=255, null=True, blank=True, verbose_name='Дом')
    apartment = models.CharField(max_length=255, null=True, blank=True, verbose_name='Квартира')
    apartment_entrance = models.CharField(max_length=255, null=True, blank=True, verbose_name='Подъезд')
    building = models.CharField(max_length=255, null=True, blank=True, verbose_name='Строение')
    floor = models.CharField(max_length=255, null=True, blank=True, verbose_name='Этаж')
    block = models.CharField(max_length=255, null=True, blank=True, verbose_name='Блок')

    def __str__(self):
        return f'{self.city}'  # Уточнить момент, как вернуть все поля разом

    class Meta:
        db_table = 'client_address'
        verbose_name = 'Адрес клиента'
        verbose_name_plural = 'Адреса клиента'


class Task(models.Model):
    """Класс задачи"""
    title = models.CharField(max_length=250, null=False, blank=False, verbose_name='Наименование задачи')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание задачи')
    status = models.CharField(max_length=50, null=False, blank=False, verbose_name='Статус задачи')
    is_done = models.BooleanField(default=False, verbose_name='Выполнено')  # галочка Выполнено
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
                                verbose_name='Ответственный менеджер')
    deadline = models.DateTimeField(null=True, blank=True, verbose_name='Крайний срок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Клиент')  # можно привязать клиента
    lead = models.ForeignKey('Lead', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Лид')

    # order = models.ForeignKey('') #или можно привязать заказ

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Lead(models.Model):
    """Класс Лиды (предзаказы)"""
    order_type = models.CharField(max_length=100, null=False, blank=False, verbose_name='Тип лида')
    appeal_type = models.CharField(max_length=100, null=False, blank=False, verbose_name='Тип обращения')
    object_type = models.CharField(max_length=100, null=False, blank=False, verbose_name='Тип обращения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания лида')
    work_start = models.DateTimeField(null=False, blank=False, verbose_name='Дата начала работ')
    work_end = models.DateTimeField(null=False, blank=False, verbose_name='Дата окончания работ')
    client_info = models.ForeignKey('Client', on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='Информация о клиенте')
    client_address = models.ForeignKey(
        'ClientAddress',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='lead_client_address',
        verbose_name='Адрес клиента')
    address_description = models.TextField(null=True, blank=True, verbose_name='Дополнительно')
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name='Город')
    micro_district = models.CharField(max_length=255, null=True, blank=True, verbose_name='Микрорайон, ж/м, ж/к')
    street = models.CharField(max_length=255, null=True, blank=True, verbose_name='Улица')
    house = models.CharField(max_length=255, null=True, blank=True, verbose_name='Дом')
    apartment = models.CharField(max_length=255, null=True, blank=True, verbose_name='Квартира')
    apartment_entrance = models.CharField(max_length=255, null=True, blank=True, verbose_name='Подъезд')
    building = models.CharField(max_length=255, null=True, blank=True, verbose_name='Строение')
    floor = models.CharField(max_length=255, null=True, blank=True, verbose_name='Этаж')
    block = models.CharField(max_length=255, null=True, blank=True, verbose_name='Блок')
    services = models.ManyToManyField('Service', verbose_name='Услуга')
    payment_type = models.CharField(max_length=25, null=False, blank=False, default='cash', verbose_name='Тип оплаты')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Создал')
    total = models.IntegerField(null=True, blank=True, verbose_name='Сумма заказа')
    lead_status = models.CharField(max_length=25, null=True, blank=True, default='new', verbose_name='Статус лида')
    client_comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lead_manager',
        verbose_name='Ответственный менеджер')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Примечание')

    def __str__(self):
        return f'Лид №{self.pk} {self.client_address}'

    class Meta:
        db_table = 'lead'
        verbose_name = 'ЛИД'
        verbose_name_plural = 'ЛИДЫ'
