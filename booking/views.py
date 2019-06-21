from .models import *
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


# from django.contrib.auth.mixins import LoginRequiredMixin


class ListView(generic.ListView):
    template_name = 'booking/list.html'
    queryset = Restaurant.objects.filter(total_seats__gt=0).order_by('total_seats')


class SeatingView(generic.DetailView):
    model = Restaurant
    template_name = 'booking/seating.html'


class MenuView(generic.DetailView):
    model = Restaurant
    template_name = 'booking/menu.html'


# class OwnerView(generic.DetailView):  # , LoginRequiredMixin
#     model = Restaurant
#     template_name = 'booking/owner.html'
#
#     def get_queryset(self):
#         return Restaurant.objects.filter(owner=self.request.user)

def owner(request, user_id):
    user = User.objects.get(id=user_id)
    restaurant = Restaurant.objects.filter(owner=user)[0]
    tables = restaurant.table_set.order_by('reserved', 'seat_count')
    reservations = []
    for table in tables:
        reservations.extend(table.reservation_set.all())
    return render(request, 'booking/owner.html',
                  {'restaurant': restaurant, 'tables': tables, 'reservations': reservations})


def menu_add(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'booking/menu_add.html', {'restaurant': restaurant})


def menu_add_save(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    items = []
    give_price_error = False
    error_contents = []
    for i in '12345':
        content_unicode = request.POST.get('content' + i, u'')
        content = content_unicode.encode("utf-8")
        price = request.POST.get('price' + i)
        if content:
            if price == '':
                give_price_error = True
                error_contents.append(content)
                continue
            item = (content, int(price))
            items.append(item)

    if items == []:
        return render(request, 'booking/menu_add.html',
                      {'restaurant': restaurant,
                       'error_message': "Please enter at least one item to add or be sure to put the prices",
                       'error_contents': error_contents})
    for item in items:
        Menu.objects.create(content=item[0], price=item[1], restaurant=restaurant)

    if give_price_error:
        return render(request, 'booking/menu_add.html',
                      {'restaurant': restaurant, 'error_message': "Please enter the price for each item and try again",
                       'error_contents': error_contents})

    return HttpResponseRedirect(reverse('booking:owner', args=(restaurant.owner.id,)))


def menu_delete(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'booking/menu_delete.html', {'restaurant': restaurant})


def menu_delete_save(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    chosen_ids = request.POST.getlist('item')
    if chosen_ids == []:
        return render(request, 'booking/menu_delete.html',
                      {'restaurant': restaurant, 'error_message': "Please chose at least one item to delete"})
    for id in chosen_ids:
        item = Menu.objects.get(id=id)
        item.delete()

    return HttpResponseRedirect(reverse('booking:owner', args=(restaurant.owner.id,)))


def table_add(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'booking/table_add.html', {'restaurant': restaurant})


def table_add_save(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    tables = []
    for i in range(10):
        people = request.POST.get('people' + str(i + 1))
        if people != '':
            tables.append(int(people))

    if tables == []:
        return render(request, 'booking/table_add.html',
                      {'error_message': "Please enter at least one table to add"})

    for people in tables:
        Table.objects.create(seat_count=people, restaurant=restaurant)

    return HttpResponseRedirect(reverse('booking:owner', args=(restaurant.owner.id,)))


def table_delete(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'booking/table_delete.html',
                  {'restaurant': restaurant, 'tables': restaurant.table_set.order_by('seat_count')})


def table_delete_save(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    chosen_ids = request.POST.getlist('table')
    if chosen_ids == []:
        return render(request, 'booking/table_delete.html',
                      {'restaurant': restaurant, 'error_message': "Please chose at least one table to delete"})
    for id in chosen_ids:
        table = Table.objects.get(id=id)
        table.delete()

    return HttpResponseRedirect(reverse('booking:owner', args=(restaurant.owner.id,)))


def cancel_reservation(request, reservation_id, restaurant_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    reservation.delete()
    return HttpResponseRedirect(reverse('booking:owner', args=(restaurant.owner.id,)))

def reserve(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    people = int(request.POST.get('people', 1))
    reservation_name = request.POST.get('name')
    if not reservation_name:
        return render(request, 'booking/seating.html',
                      {'restaurant': restaurant, 'error_message': "Please give a reservation_name"})
    tables_to_check = list(Table.objects.filter(restaurant=restaurant, reserved=False).order_by('seat_count'))
    tables = get_tables(restaurant, people, tables_to_check)
    for table in tables:
        Reservation.objects.create(table=table, name=reservation_name, people=people)
        table.reserved = True
        table.save()

    return HttpResponseRedirect(reverse('booking:done', args=(restaurant_id,)))


def done(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    reservation = Reservation.objects.order_by('-id')[0]
    name = reservation.name
    return render(request, 'booking/done.html', {'restaurant': restaurant, 'reservation_name': name})


def get_tables(restaurant, num_of_people, tables_to_check, tables_to_reserve=[]):
    if tables_to_check == [] or num_of_people <= 0:
        return tables_to_reserve

    for table in tables_to_check:
        if num_of_people <= table.seat_count:
            tables_to_reserve.append(table)
            tables_to_check.remove(table)
            return tables_to_reserve

    tables_to_reserve.append(tables_to_check[-1])
    return get_tables(restaurant, num_of_people - tables_to_check[-1].seat_count, tables_to_check[:-1],
                      tables_to_reserve)
