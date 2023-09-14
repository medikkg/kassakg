from django.db import models

class Task(models.Model):
    """Класс задачи"""
    title = models.CharField(max_length=250, null=False, blank=False, verbose_name='Наименование задачи')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание задачи')
    status = models.CharField(max_length=50, null=False, blank=False, verbose_name='Статус задачи')
    is_done = models.BooleanField(default=False, verbose_name='Выполнено') #галочка Выполнено
    manager = models.ForeignKey() #ответственный менеджер
    deadline = models.DateTimeField(null=True, blank=True, verbose_name='Крайний срок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')
    client = models.ForeignKey() #можно привязать клиента
    order = models.ForeignKey() #можно привязать заказ


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'



class Lead(models.Model):
    """Класс Лиды (предзаказы)"""
    order_type = models.CharField(max_length=100, null=False, blank=False, verbose_name='Тип лида')
    appeal_type = models.CharField(max_length=100, null=False, blank=False, verbose_name='Тип обращения')
    object_type = models.CharField(max_length=100, null=False, blank=False, verbose_name='Тип обращения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


