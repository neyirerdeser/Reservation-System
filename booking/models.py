from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    total_seats = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    seat_count = models.IntegerField()
    reserved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        old_state = True
        if self.id:
            old_state = Table.objects.get(id=self.id).reserved

        super(Table, self).save(*args, **kwargs)
        new_state = self.reserved
        if old_state is False and new_state is True:
            print('F --> T')
            self.restaurant.total_seats -= self.seat_count
            self.restaurant.save()

        if old_state is True and new_state is False:
            print('T --> F')
            self.restaurant.total_seats += self.seat_count
            self.restaurant.save()

    def __str__(self):
        return str(self.restaurant) + ', seats:' + str(self.seat_count) + ' reserved: ' + str(self.reserved)


class Menu(models.Model):
    content = models.CharField(max_length=1000)
    price = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant)

    def __str__(self):
        return str(self.content) + ': ' + str(self.price)


class Reservation(models.Model):
    table = models.ForeignKey(Table)
    people = models.IntegerField(default=1)
    name = models.CharField(max_length=200, null=True, blank=True)

    def delete(self, *args, **kwargs):
        table = self.table
        table.reserved = False
        table.save()
        super(Reservation, self).delete(*args, **kwargs)

    def create(self, table, *args, **kwargs):
        table.reserved = True
        table.save()
        super(Reservation, self).create(table=table, *args, **kwargs)

    def __str__(self):
        return str(self.name) + ' at ' + str(self.table.restaurant.name) + ' for ' + str(self.people)

# def reset_day():
#     for reservation in Reservation.objects.all():
#         reservation.delete()
#     # just in case some random stuff was done via admin page
#     for table in Table.objects.filter(reserved=True):
#         table.reserved=False
#         table.save()

