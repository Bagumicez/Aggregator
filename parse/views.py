from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .utils import Parse
from .models import Order


def index(request):
    return render(request, 'parse/index.html')


def load(request, source):
    Order.objects.filter(source=source).delete()
    result = Parse.start_parse(source)
    print(result)
    Order.save_result(result, source)
    return HttpResponseRedirect(reverse('parse:index', args=()))


def show_result(request, source):
    data = Order.objects.filter(source=source)
    return render(request, 'parse/detail.html', {'data': data})


def sort_view(request):
    data = Order.objects.all().order_by('-time_place')
    return render(request, 'parse/detail.html', {'data': data})
