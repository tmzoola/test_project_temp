from django.db import models
from django.db.models import Count


class Client(models.Model):
    full_name = models.CharField(max_length=255)
    birthdate = models.DateField()
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)


    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = "Clients"
        verbose_name = "Client"


class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    birthdate = models.DateField()


    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = "Employees"
        verbose_name = "Employee"



    def get_statistics(self, month, year):
        orders = Order.objects.filter(employee=self, date__month=month, date__year=year)
        response = orders.aggregate(clients=Count('client', distinct=True))

        products = 0
        sales = 0
        for order in orders:
            products += order.products.all().count()
            sales += order.price

        return {
            'full_name': self.full_name,
            'clients': response['clients'],
            'products': products,
            'sales': sales
        }

class Order(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pk:
            for product in self.products.all():
                print(product)
                product.quantity -= 1
                product.save()

class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.quantity}"


