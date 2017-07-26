from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .utils import Parse
from .models import Order


@login_required()
def index(request):
    return render(request, 'parse/index.html')


@login_required()
def load(request, source):
    result = Parse.start_parse(source)
    Order.save_result(result, source)
    return HttpResponseRedirect(reverse('parse:index', args=()))


@login_required()
def show_result(request, source):
    data = Order.objects.filter(source=source)
    return render(request, 'parse/detail.html', {'data': data})


@login_required()
def sort_view(request):
    data = Order.objects.all().order_by('-time_place')
    return render(request, 'parse/detail.html', {'data': data})
