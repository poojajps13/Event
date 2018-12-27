from datetime import date

from django.shortcuts import render

from event.models import *


def home(request):
    event_list = EventRecord.objects.all().order_by('-pk')
    return render(request, 'index.html', {'event_list': event_list, 'now': date.today()})


def structural_design(request):
    return render(request, 'static1.html')


def cisco_networking_academy(request):
    return render(request, 'static2.html')


def texas(request):
    return render(request, 'static3.html')


def smc_india(request):
    return render(request, 'static4.html')


def automation_research(request):
    return render(request, 'static5.html')


def vlsi_design(request):
    return render(request, 'static6.html')


def big_data(request):
    return render(request, 'static7.html')


def innovation_centre(request):
    return render(request, 'static8.html')


def mobile_application(request):
    return render(request, 'static9.html')


def software_development(request):
    return render(request, 'static10.html')
