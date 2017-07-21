from django.db import models
from django.db import IntegrityError


class Order(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.CharField(max_length=30)
    url = models.URLField(unique=True)
    time_place = models.DateField()
    responses = models.IntegerField(default=0)
    view = models.IntegerField(default=0)
    source = models.CharField(max_length=50, default='')

    def save_result(result, source):
        for order_page in result:
            for order in order_page:
                title = order['title']
                description = order['description']
                price = order['price'][:30]
                time = order['time']
                url = order['url']
                try:
                    responses = int(order['responses'])
                except:
                    responses = 0
                try:
                    views = int(order['views'])
                except KeyError:
                    views = 0
                try:
                    cur_order = Order(title=title, description=description, price=price,
                                      time_place=time, url=url, responses=responses,
                                      view=views, source=source)
                    cur_order.save()
                except IntegrityError:
                    continue

    def __str__(self):
        return self.title
