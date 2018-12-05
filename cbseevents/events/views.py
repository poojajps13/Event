from io import BytesIO

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views.generic import TemplateView
from xhtml2pdf import pisa

from event.models import *
from events.models import *
from .forms import *


def some_view(request):
    # return render(request, 'report.html')
    list = User.objects.all()
    template = get_template('report.html')
    context = {
        'event': 'Workshop',
        'student_list': list,
    }
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = "Report.pdf"
        content = "inline; filename='%s'" % (filename)
        # content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


def edit_workshopamount(request, paymentid):
    try:
        p = StudentRecordWorkshop.objects.get(payment_id=paymentid)
        if request.method == "POST":
            p.paid = request.POST['paid']
            p.save(update_fields=['paid'])
    except ObjectDoesNotExist:
        messages.error(request, 'Edit not allowed!!!')
    return render(request, 'edit_amount.html', {'p': p})


def edit_seminaramount(request, paymentid):
    try:
        p = StudentRecordSeminar.objects.get(payment_id=paymentid)
        if request.method == "POST":
            p.paid = request.POST['paid']
            p.save(update_fields=['paid'])
    except ObjectDoesNotExist:
        messages.error(request, 'Edit not allowed!!!')
    return render(request, 'edit_amount.html', {'p': p})


def edit_trainingamount(request, paymentid):
    try:
        p = StudentRecordTraining.objects.get(payment_id=paymentid)
        if request.method == "POST":
            p.paid = request.POST['paid']
            p.save(update_fields=['paid'])
    except ObjectDoesNotExist:
        messages.error(request, 'Edit not allowed!!!')
    return render(request, 'edit_amount.html', {'p': p})


def edit_competitionamount(request, paymentid):
    try:
        p = StudentRecordCompetition.objects.get(payment_id=paymentid)
        if request.method == "POST":
            p.paid = request.POST['paid']
            p.save(update_fields=['paid'])
    except ObjectDoesNotExist:
        messages.error(request, 'Edit not allowed!!!')
    return render(request, 'edit_amount.html', {'p': p})


def edit_guestlectureamount(request, paymentid):
    try:
        p = StudentRecordGuestLecture.objects.get(payment_id=paymentid)
        if request.method == "POST":
            p.paid = request.POST['paid']
            p.save(update_fields=['paid'])
    except ObjectDoesNotExist:
        messages.error(request, 'Edit not allowed!!!')
    return render(request, 'edit_amount.html', {'p': p})


def home(request):
    event_list = EventRecord.objects.all().order_by('-pk')
    print(event_list)
    work = WorkshopRecord.objects.all().order_by('-pk')
    semi = SeminarRecord.objects.all().order_by('-pk')
    train = TrainingRecord.objects.all().order_by('-pk')
    comp = CompetitionRecord.objects.all().order_by('-pk')
    guest = GuestLectureRecord.objects.all().order_by('-pk')
    return render(request, 'index.html',
                  {'event_list': event_list, 'work': work, 'semi': semi, 'train': train, 'comp': comp, 'guest': guest})


class Registration(TemplateView):

    def get(self, request, *args, **kwargs):
        event = kwargs['type']
        if event == 'workshop':
            work = WorkshopRecord.objects.get(slug=kwargs['slug'])
            StudentRecordWorkshop.objects.create(name=request.user, registered_event_code=work, c_o_e=work.c_o_e)
        elif event == 'seminar':
            work = SeminarRecord.objects.get(slug=kwargs['slug'])
            StudentRecordSeminar.objects.create(name=request.user, registered_event_code=work, c_o_e=work.c_o_e)
        elif event == 'training':
            work = TrainingRecord.objects.get(slug=kwargs['slug'])
            StudentRecordTraining.objects.create(name=request.user, registered_event_code=work, c_o_e=work.c_o_e)
        elif event == 'competition':
            work = CompetitionRecord.objects.get(slug=kwargs['slug'])
            StudentRecordCompetition.objects.create(name=request.user, registered_event_code=work, c_o_e=work.c_o_e)
        else:
            work = GuestLectureRecord.objects.get(slug=kwargs['slug'])
            StudentRecordGuestLecture.objects.create(name=request.user, registered_event_code=work, c_o_e=work.c_o_e)
        messages.success(request, 'Successfully Registered')
        return redirect('home')


def workshop(request):
    workshop_list = WorkshopRecord.objects.all().order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordworkshop.objects.all()
    return render(request, 'workshop.html',
                  {'event_list': workshop_list, 'year_list': year_list, 'months_list': months_list})


def workshop_description(request, slug):
    workshop = WorkshopRecord.objects.get(slug=slug)
    return render(request, 'description.html', {'obj': workshop, 'event': 'workshop'})


def workshop_search(request, year, month):
    workshop_list = WorkshopRecord.objects.filter(event_year=year, event_month=month).order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordworkshop.objects.all()
    return render(request, 'workshop.html',
                  {'event_list': workshop_list, 'year_list': year_list, 'months_list': months_list})


def update_workshop(request, slug):
    try:
        event = WorkshopRecord.objects.get(slug=slug)
        if event.user == request.user:
            if request.method == "POST":
                event.event_name = request.POST['event_name']
                event.duration = request.POST['duration']
                event.description = request.POST['description']
                event.resource_person = request.POST['resource_person']
                event.resource_person_data = request.POST['resource_person_data']
                event.registration_start = request.POST['registration_start']
                event.registration_end = request.POST['registration_end']
                event.event_date = request.POST['event_date']
                event.event_month = request.POST['event_month']
                event.event_year = request.POST['event_year']
                event.eligible_branches = request.POST['eligible_branches']
                event.outside_student = request.POST['outside_student']
                event.venue = request.POST['venue']
                event.fees = request.POST['fees']
                event.save(
                    update_fields=['event_name', 'description', 'duration', 'resource_person', 'resource_person_data',
                                   'registration_start', 'registration_end', 'event_date', 'event_month', 'event_year',
                                   'eligible_branches', 'outside_student', 'venue', 'fees'])
            return render(request, 'update.html', {'event': event})
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Workshop does not exist')
    except PermissionDenied:
        messages.error(request, 'Permission Denied')
    return redirect('home')


def delete_workshop(request, slug):
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordworkshop.objects.all()
    try:
        obj = WorkshopRecord.objects.get(slug=slug)
        if obj.user == request.user:
            obj.delete()
            messages.success(request, 'Workshop deleted')
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Workshop does not exist')
    except PermissionDenied:
        messages.error(request, 'Workshop does not exist !!!')
    workshop_list = WorkshopRecord.objects.all().order_by('-pk')
    return render(request, 'workshop.html',
                  {'event_list': workshop_list, 'year_list': year_list, 'months_list': months_list})


def seminar(request):
    seminar_list = SeminarRecord.objects.all().order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordseminar.objects.all()
    return render(request, 'seminar.html',
                  {'event_list': seminar_list, 'year_list': year_list, 'months_list': months_list})


def seminar_description(request, slug):
    seminar = SeminarRecord.objects.get(slug=slug)
    return render(request, 'description.html', {'obj': seminar, 'event': 'seminar'})


def seminar_search(request, year, month):
    seminar_list = SeminarRecord.objects.filter(event_year=year, event_month=month).order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordseminar.objects.all()
    return render(request, 'seminar.html',
                  {'event_list': seminar_list, 'year_list': year_list, 'months_list': months_list})


def update_seminar(request, slug):
    try:
        event = SeminarRecord.objects.get(slug=slug)
        if event.user == request.user:
            if request.method == "POST":
                event.event_name = request.POST['event_name']
                event.duration = request.POST['duration']
                event.description = request.POST['description']
                event.resource_person = request.POST['resource_person']
                event.resource_person_data = request.POST['resource_person_data']
                event.registration_start = request.POST['registration_start']
                event.registration_end = request.POST['registration_end']
                event.event_date = request.POST['event_date']
                event.event_month = request.POST['event_month']
                event.event_year = request.POST['event_year']
                event.eligible_branches = request.POST['eligible_branches']
                event.outside_student = request.POST['outside_student']
                event.venue = request.POST['venue']
                event.fees = request.POST['fees']
                event.save(
                    update_fields=['event_name', 'description', 'duration', 'resource_person', 'resource_person_data',
                                   'registration_start', 'registration_end', 'event_date', 'event_month', 'event_year',
                                   'eligible_branches',
                                   'outside_student', 'venue', 'fees'])
            return render(request, 'update.html', {'event': event})
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Seminar does not exist')
    except PermissionDenied:
        messages.error(request, 'Permission Denied')
    return redirect('home')


def delete_seminar(request, slug):
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordseminar.objects.all()
    try:
        obj = SeminarRecord.objects.get(slug=slug)
        if obj.user == request.user:
            obj.delete()
            messages.success(request, 'Seminar deleted')
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Seminar does not exist')
    except PermissionDenied:
        messages.error(request, 'Seminar does not exist !!!')
    seminar_list = SeminarRecord.objects.all().order_by('-pk')
    return render(request, 'seminar.html',
                  {'event_list': seminar_list, 'year_list': year_list, 'months_list': months_list})


def training(request):
    training_list = TrainingRecord.objects.all().order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordtraining.objects.all()
    return render(request, 'training.html',
                  {'event_list': training_list, 'year_list': year_list, 'months_list': months_list})


def training_description(request, slug):
    training = TrainingRecord.objects.get(slug=slug)
    return render(request, 'description.html', {'obj': training, 'event': 'training'})


def training_search(request, year, month):
    training_list = TrainingRecord.objects.filter(event_year=year, event_month=month).order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordtraining.objects.all()
    return render(request, 'training.html',
                  {'event_list': training_list, 'year_list': year_list, 'months_list': months_list})


def update_training(request, slug):
    try:
        event = TrainingRecord.objects.get(slug=slug)
        if event.user == request.user:
            if request.method == "POST":
                event.event_name = request.POST['event_name']
                event.duration = request.POST['duration']
                event.description = request.POST['description']
                event.resource_person = request.POST['resource_person']
                event.resource_person_data = request.POST['resource_person_data']
                event.registration_start = request.POST['registration_start']
                event.registration_end = request.POST['registration_end']
                event.event_date = request.POST['event_date']
                event.event_month = request.POST['event_month']
                event.event_year = request.POST['event_year']
                event.eligible_branches = request.POST['eligible_branches']
                event.outside_student = request.POST['outside_student']
                event.venue = request.POST['venue']
                event.fees = request.POST['fees']
                event.save(
                    update_fields=['event_name', 'description', 'duration', 'resource_person', 'resource_person_data',
                                   'registration_start', 'registration_end', 'event_date', 'event_month', 'event_year',
                                   'eligible_branches',
                                   'outside_student', 'venue', 'fees'])
            return render(request, 'update.html', {'event': event})
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Training does not exist')
    except PermissionDenied:
        messages.error(request, 'Permission Denied')
    return redirect('home')


def delete_training(request, slug):
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordtraining.objects.all()
    try:
        obj = TrainingRecord.objects.get(slug=slug)
        if obj.user == request.user:
            obj.delete()
            messages.success(request, 'Training deleted')
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Training does not exist')
    except PermissionDenied:
        messages.error(request, 'Training does not exist !!!')
    training_list = TrainingRecord.objects.all().order_by('-pk')
    return render(request, 'training.html',
                  {'event_list': training_list, 'year_list': year_list, 'months_list': months_list})


def competition(request):
    competition_list = CompetitionRecord.objects.all().order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordcompetition.objects.all()
    return render(request, 'competition.html',
                  {'event_list': competition_list, 'year_list': year_list, 'months_list': months_list})


def competition_description(request, slug):
    competition = CompetitionRecord.objects.get(slug=slug)
    return render(request, 'description.html', {'obj': competition, 'event': 'competition'})


def competition_search(request, year, month):
    competition_list = CompetitionRecord.objects.filter(event_year=year, event_month=month).order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordcompetition.objects.all()
    return render(request, 'competition.html',
                  {'event_list': competition_list, 'year_list': year_list, 'months_list': months_list})


def update_competition(request, slug):
    try:
        event = CompetitionRecord.objects.get(slug=slug)
        if event.user == request.user:
            if request.method == "POST":
                event.event_name = request.POST['event_name']
                event.duration = request.POST['duration']
                event.description = request.POST['description']
                event.resource_person = request.POST['resource_person']
                event.resource_person_data = request.POST['resource_person_data']
                event.registration_start = request.POST['registration_start']
                event.registration_end = request.POST['registration_end']
                event.event_date = request.POST['event_date']
                event.event_month = request.POST['event_month']
                event.event_year = request.POST['event_year']
                event.eligible_branches = request.POST['eligible_branches']
                event.outside_student = request.POST['outside_student']
                event.venue = request.POST['venue']
                event.fees = request.POST['fees']
                event.save(
                    update_fields=['event_name', 'description', 'duration', 'resource_person', 'resource_person_data',
                                   'registration_start', 'registration_end', 'event_date', 'event_month', 'event_year',
                                   'eligible_branches',
                                   'outside_student', 'venue', 'fees'])
            return render(request, 'update.html', {'event': event})
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Workshop does not exist')
    except PermissionDenied:
        messages.error(request, 'Permission Denied')
    return redirect('home')


def delete_competition(request, slug):
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordcompetition.objects.all()
    try:
        obj = CompetitionRecord.objects.get(slug=slug)
        if obj.user == request.user:
            obj.delete()
            messages.success(request, 'Workshop deleted')
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Competition does not exist')
    except PermissionDenied:
        messages.error(request, 'Competition does not exist !!!')
    competition_list = CompetitionRecord.objects.all().order_by('-pk')
    return render(request, 'competition.html',
                  {'event_list': competition_list, 'year_list': year_list, 'months_list': months_list})


def guest_lecture(request):
    guest_lecture_list = GuestLectureRecord.objects.all().order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordguest_lecture.objects.all()
    print(year_list, months_list)
    return render(request, 'guest_lecture.html',
                  {'event_list': guest_lecture_list, 'year_list': year_list, 'months_list': months_list})


def guest_lecture_description(request, slug):
    guest_lecture = GuestLectureRecord.objects.get(slug=slug)
    return render(request, 'description.html', {'obj': guest_lecture, 'event': 'guest_lecture'})


def guest_lecture_search(request, year, month):
    guest_lecture_list = GuestLectureRecord.objects.filter(event_year=year, event_month=month).order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordguest_lecture.objects.all()
    return render(request, 'guest_lecture.html',
                  {'event_list': guest_lecture_list, 'year_list': year_list, 'months_list': months_list})


def update_guestlecture(request, slug):
    try:
        event = GuestLectureRecord.objects.get(slug=slug)
        if event.user == request.user:
            if request.method == "POST":
                event.event_name = request.POST['event_name']
                event.duration = request.POST['duration']
                event.description = request.POST['description']
                event.resource_person = request.POST['resource_person']
                event.resource_person_data = request.POST['resource_person_data']
                event.registration_start = request.POST['registration_start']
                event.registration_end = request.POST['registration_end']
                event.event_date = request.POST['event_date']
                event.event_month = request.POST['event_month']
                event.event_year = request.POST['event_year']
                event.eligible_branches = request.POST['eligible_branches']
                event.outside_student = request.POST['outside_student']
                event.venue = request.POST['venue']
                event.fees = request.POST['fees']
                event.save(
                    update_fields=['event_name', 'description', 'duration', 'resource_person', 'resource_person_data',
                                   'registration_start', 'registration_end', 'event_date', 'event_month', 'event_year',
                                   'eligible_branches',
                                   'outside_student', 'venue', 'fees'])
            return render(request, 'update.html', {'event': event})
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Workshop does not exist')
    except PermissionDenied:
        messages.error(request, 'Workshop does not exist !!!')
    return render(request, 'update.html')


def delete_guestlecture(request, slug):
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordguest_lecture.objects.all()
    try:
        obj = GuestLectureRecord.objects.get(slug=slug)
        if obj.user == request.user:
            obj.delete()
            messages.success(request, 'Guest Lecture deleted')
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Guest Lecture does not exist')
    except PermissionDenied:
        messages.error(request, 'Guest Lecture  does not exist !!!')
    guestlecture_list = GuestLectureRecord.objects.all().order_by('-pk')
    return render(request, 'guest_lecture.html',
                  {'event_list': guestlecture_list, 'year_list': year_list, 'months_list': months_list})


def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        try:
            if form.is_valid():
                select_event = form.cleaned_data['select_event']
                c_o_e = form.cleaned_data['c_o_e']
                event_name = form.cleaned_data['event_name']
                description = form.cleaned_data['description']
                duration = form.cleaned_data['duration']
                resource_person = form.cleaned_data['resource_person']
                resource_person_data = form.cleaned_data['resource_person_data']
                registration_start = form.cleaned_data['registration_start']
                registration_end = form.cleaned_data['registration_end']
                event_date = form.cleaned_data['event_date']
                event_month = form.cleaned_data['event_month']
                event_year = form.cleaned_data['event_year']
                eligible_branches = form.cleaned_data['eligible_branches']
                outside_student = form.cleaned_data['outside_student']
                venue = form.cleaned_data['venue']
                fees = form.cleaned_data['fees']
                if select_event == 'workshop':
                    WorkshopRecord.objects.create(c_o_e=c_o_e, event_name=event_name, duration=duration,
                                                  description=description, resource_person=resource_person,
                                                  resource_person_data=resource_person_data,
                                                  registration_start=registration_start,
                                                  registration_end=registration_end,
                                                  event_date=event_date, event_month=event_month, event_year=event_year,
                                                  eligible_branches=eligible_branches,
                                                  outside_student=outside_student, venue=venue, fees=fees,
                                                  user=request.user)
                if select_event == 'seminar':
                    SeminarRecord.objects.create(c_o_e=c_o_e, event_name=event_name, duration=duration,
                                                 description=description, resource_person=resource_person,
                                                 resource_person_data=resource_person_data,
                                                 registration_start=registration_start,
                                                 registration_end=registration_end,
                                                 event_date=event_date, event_month=event_month, event_year=event_year,
                                                 eligible_branches=eligible_branches,
                                                 outside_student=outside_student, venue=venue, fees=fees,
                                                 user=request.user)
                if select_event == 'training':
                    TrainingRecord.objects.create(c_o_e=c_o_e, event_name=event_name, duration=duration,
                                                  description=description, resource_person=resource_person,
                                                  resource_person_data=resource_person_data,
                                                  registration_start=registration_start,
                                                  registration_end=registration_end,
                                                  event_date=event_date, event_month=event_month, event_year=event_year,
                                                  eligible_branches=eligible_branches,
                                                  outside_student=outside_student, venue=venue, fees=fees,
                                                  user=request.user)
                if select_event == 'competition':
                    CompetitionRecord.objects.create(c_o_e=c_o_e, event_name=event_name, duration=duration,
                                                     description=description, resource_person=resource_person,
                                                     resource_person_data=resource_person_data,
                                                     registration_start=registration_start,
                                                     registration_end=registration_end,
                                                     event_date=event_date, event_month=event_month,
                                                     event_year=event_year,
                                                     eligible_branches=eligible_branches,
                                                     outside_student=outside_student, venue=venue, fees=fees,
                                                     user=request.user)
                if select_event == 'guest lecture':
                    GuestLectureRecord.objects.create(c_o_e=c_o_e, event_name=event_name, duration=duration,
                                                      description=description, resource_person=resource_person,
                                                      resource_person_data=resource_person_data,
                                                      registration_start=registration_start,
                                                      registration_end=registration_end,
                                                      event_date=event_date, event_month=event_month,
                                                      event_year=event_year,
                                                      eligible_branches=eligible_branches,
                                                      outside_student=outside_student, venue=venue, fees=fees,
                                                      user=request.user)
                try:
                    YearRecord.objects.get(year=event_year)
                except ObjectDoesNotExist:
                    YearRecord.objects.create(year=event_year)
                if select_event == 'workshop':
                    try:
                        MonthRecordworkshop.objects.get(month_code=event_month)
                    except ObjectDoesNotExist:
                        MonthRecordworkshop.objects.create(month_code=event_month)
                if select_event == 'training':
                    try:
                        MonthRecordtraining.objects.get(month_code=event_month)
                    except ObjectDoesNotExist:
                        MonthRecordtraining.objects.create(month_code=event_month)
                if select_event == 'seminar':
                    try:
                        MonthRecordseminar.objects.get(month_code=event_month)
                    except ObjectDoesNotExist:
                        MonthRecordseminar.objects.create(month_code=event_month)
                if select_event == 'competition':
                    try:
                        MonthRecordcompetition.objects.get(month_code=event_month)
                    except ObjectDoesNotExist:
                        MonthRecordcompetition.objects.create(month_code=event_month)
                if select_event == 'guest lecture':
                    try:
                        MonthRecordguest_lecture.objects.get(month_code=event_month)
                    except ObjectDoesNotExist:
                        MonthRecordguest_lecture.objects.create(month_code=event_month)
                messages.success(request, 'Successfully added Event')
            else:
                messages.error(request, 'Invalid form')
        except Exception:
            messages.error(request, 'Try again')
        return render(request, 'add_event.html', {'form': form})
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


def studentlist_workshop(request, registered_event_code):
    event = WorkshopRecord.objects.get(slug=registered_event_code)
    lists = StudentRecordWorkshop.objects.filter(registered_event_code=event)
    return render(request, 'studentlist.html', {'lists': lists, 'workshop': True})


def studentlist_seminar(request, registered_event_code):
    event = SeminarRecord.objects.get(slug=registered_event_code)
    lists = StudentRecordSeminar.objects.filter(registered_event_code=event)
    return render(request, 'studentlist.html', {'lists': lists, 'seminar': True})


def studentlist_training(request, registered_event_code):
    event = TrainingRecord.objects.get(slug=registered_event_code)
    lists = StudentRecordTraining.objects.filter(registered_event_code=event)
    return render(request, 'studentlist.html', {'lists': lists, 'training': True})


def studentlist_competition(request, registered_event_code):
    event = CompetitionRecord.objects.get(slug=registered_event_code)
    lists = StudentRecordCompetition.objects.filter(registered_event_code=event)
    return render(request, 'studentlist.html', {'lists': lists, 'competition': True})


def studentlist_guestlecture(request, registered_event_code):
    event = GuestLectureRecord.objects.get(slug=registered_event_code)
    lists = StudentRecordGuestLecture.objects.filter(registered_event_code=event)
    return render(request, 'studentlist.html', {'lists': lists, 'guest_lecture': True})


def excellence_center(request):
    return render(request, 'excellence_center.html')


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
