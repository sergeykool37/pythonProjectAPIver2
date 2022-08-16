from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import make_aware

class Deal(models.Model):
    customer = models.CharField(max_length=200)  # логин покупателя
    item = models.CharField(max_length=200)  # наименование товара
    total = models.PositiveSmallIntegerField()  # сумма сделки
    quantity = models.PositiveSmallIntegerField()  # количество    товара, шт
    date = models.DateTimeField()  # дата и время регистрации сделки

    def create_deals_of_line(self, line: bytes):
        str_line = line.decode("utf-8")
        str_line = str_line.split(',')
        customer = str_line[0]
        item = str_line[1]
        try:
            total = int(str_line[2])
        except ValueError:
            return
        try:
            quantity = int(str_line[3])
        except ValueError:
            return
        try:
            date = datetime.strptime(str_line[4].rstrip(), '%Y-%m-%d %H:%M:%S.%f')
            date = make_aware(date)
        except ValueError:
            return

        self.customer = customer
        self.item = item
        self.total = total
        self.quantity = quantity
        self.date = date
        self.save()

class Client(models.Model):
    username = models.CharField(max_length=200)  # логин клиента
    spent_money = models.PositiveSmallIntegerField()  # сумма потраченных средств за весь период;
    gems = models.CharField(max_length=200)  # список из названий камней, которые купили как
    # минимум двое из списка "5 клиентов, потративших
    # наибольшую сумму за весь период", и данный клиент
    # является одним из этих покупателей


