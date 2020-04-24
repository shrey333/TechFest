from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.template.context_processors import csrf
from dbapp.models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from why.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from sendsms import api


def subscribe(request):
    subject = 'Welcome to TechFest 2020'
    message = '<h1>Thank you to joining us. You will receive regular TechFest 2020 update via this mail.<h1>'
    recepient = request.POST.get('newsletter')
    e = Newsletter(email=recepient)
    e.save()
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False, html_message=message)
    return render(request, 'demo.html', {'message': "You are subscribed"})


class index(TemplateView):
    def get(self, request, *args, **kwargs):
        c = {}
        c.update(csrf(request))
        return render(None, 'demo.html', c)


def eventlist(request):
    alldept = Event.objects.all()
    des = Department.objects.get(department=request.GET.get('dept')).description
    dept = Department.objects.get(department=request.GET.get('dept')).department
    evl = []
    for i in alldept:
        if i.department.department == dept:
            evl.append(i)
    return render(None, 'eventlist.html', {'evl': evl, 'dept': dept, 'des': des})


def event(request):
    all = Event.objects.all()
    myevent = []
    for i in all:
        print(i, " ", i.event_name, " ", request.GET.get('name'))
        if i.event_name == request.GET.get('name'):
            myevent = i
    print(myevent.event_name)
    return render(request, 'event.html', {'event': myevent})


def register(request):
    eventid = request.GET.get('event_id')
    c = {}
    c.update(csrf(request))
    return render(request, 'Register.html', {'c': c, 'eventid': eventid})


def login(request):
    c = {}
    c.update(csrf(request))
    return render(None, 'Login.html', c)


def auth_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/intermediate/')
    else:
        return HttpResponseRedirect('/login/')


@login_required(login_url='/login/')
def registerevent(request):
    if request.POST.get('show'):
        event = request.POST.get('event')
        if event != 'all':
            e = Event.objects.get(event_name=event)
            id = e.event_id
            r = None
            try:
                r = Participant.objects.filter(event_id=id)
            except Participant.DoesNotExist:
                msg = None
            if r is not None:
                return render(request, 'registerevent.html', {'p': r})
            else:
                return render(request, 'registerevent.html', {'null': 'True'})
        else:
            r = None
            try:
                r = Participant.objects.all()
            except Participant.DoesNotExist:
                msg = None
            if len(r) != 0:
                return render(request, 'registerevent.html', {'p': r})
            else:
                return render(request, 'registerevent.html', {'null': 'True'})
    elif request.POST.get('delete'):
        event = request.POST.get('event')
        if event == 'all':
            context = Event.objects.all()
            event = []
            for i in context:
                event.append(i.event_name)
            return render(request, 'intermediate.html', {'msg': 'you cannot select all for delete', 'event': event})
        else:
            Event.objects.get(event_name=event).delete()
            return render(request, 'registerevent.html', {'msg': event + ' Event deleted.'})
    elif request.POST.get('registered'):
        event = request.POST.get('event')
        c = {}
        c.update(csrf(request))
        return render(request, 'registerevent.html', {'c': c, 'registeredemail': event})
    if request.POST.get('newsletter'):
        c = {}
        c.update(csrf(request))
        return render(request, 'registerevent.html', {'c': c, 'newsletter': 'True'})
    elif request.POST.get('register'):
        c = {}
        c.update(csrf(request))
        return render(request, 'registerevent.html', {'c': c, 'register': 'True'})


@login_required(login_url='/login/')
def store(request):
    dept = Department(request.POST.get('dept'))
    image = request.FILES['image']
    fs = FileSystemStorage()
    name = fs.save(image.name, image)
    url = fs.url(name)
    print(url)
    e = Event(event_name=request.POST.get('event-name'),
              department=dept,
              img=request.FILES['image'],
              problem_statement=request.POST.get('statement'),
              event_date=request.POST.get('eventdate'),
              people_required=request.POST.get('requiredppl'),
              fees=request.POST.get('fees'),
              rules=request.POST.get('rules'), )
    e.save()
    e = Newsletter.objects.all()
    list = []
    for i in e:
        list.append(i.email)
    subject = 'From TechFest 2020'
    body = 'Hello Folks. New Event is added to ' + request.POST.get('dept') + ' named ' + request.POST.get(
        'event-name') + ' check out at our official website'
    send_mail(subject, body, EMAIL_HOST_USER, list, fail_silently=False)
    msg = 'Emails sent successfully'
    return HttpResponseRedirect('/eventlist/?dept=' + request.POST.get('dept'))


def storepart(request):
    eve = Event.objects.get(event_id=request.POST.get('eventid'))
    p = Participant(firstname=request.POST.get('fname'),
                    lastname=request.POST.get('lname'),
                    event_id=eve,
                    birthdate=request.POST.get('dob'),
                    college_name=request.POST.get('college'),
                    gender=request.POST.get('gender'),
                    department=Department(department=request.POST.get('dept')),
                    mobile=request.POST.get('mobile'),
                    email=request.POST.get('eid'),
                    )
    p.save()
    if request.POST.get('check'):
        e = Newsletter(email=request.POST.get('eid'))
        e.save()
    subject = 'Welcome to TechFest 2020'
    message = 'Thank you for participation in TechFest 2020. You will be notified for any changes in event that you ' \
              'registered. '
    send_mail(subject, message, EMAIL_HOST_USER, [request.POST.get('eid')], fail_silently=False, html_message=message)
    return render(request, 'success.html')


@login_required(login_url='/login/')
def intermediate(request):
    context = Event.objects.all()
    event = []
    for i in context:
        event.append(i.event_name)
    print(event)
    c = {}
    c.update(csrf(request))
    return render(request, 'intermediate.html', {'c': c, 'event': event})


@login_required(login_url='/login/')
def mail(request):
    if request.POST.get('registered'):
        event = request.POST.get('event')
        e = Event.objects.get(event_name=event)
        id = e.event_id
        r = None
        try:
            r = Participant.objects.get(event_id=id)
            list = []
            for i in r:
                list.append(i.email)
            send_mail(request.POST.get('subject'), request.POST.get('body'), EMAIL_HOST_USER, list, fail_silently=False)
            msg = 'Emails sent successfully'
        except Participant.DoesNotExist:
            msg = None
        return render(request, 'intermediate.html', {'msg1': msg})
    else:
        e = Newsletter.objects.all()
        list = []
        for i in e:
            list.append(i.email)
        send_mail(request.POST.get('subject'), request.POST.get('body'), EMAIL_HOST_USER, list, fail_silently=False)
        msg = 'Emails sent successfully'
        return render(request, 'intermediate.html', {'msg2': msg})


def logout(request):
    auth.logout(request)
    return render(request, 'login.html', None)
