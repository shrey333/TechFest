from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.views import generic
from django.core.files.storage import FileSystemStorage
from django.template.context_processors import csrf
from dbapp.models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required


class index(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(None, 'demo.html', context=None)


def eventlist(request):
    alldept = Event.objects.all()
    des = Department.objects.get(department=request.GET.get('dept')).description
    dept = Department.objects.get(department=request.GET.get('dept')).department
    evl = []
    img = []
    for i in alldept:
        if i.department.department == dept:
            img.append(i.img)
            evl.append(i.event_name)
    return render(None, 'eventlist.html', {'evl': evl, 'img': img, 'dept': dept, 'des': des})


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
    c = {}
    c.update(csrf(request))
    return render(None, 'Register.html', c)


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
        return HttpResponseRedirect('/registerevent/')
    else:
        return HttpResponseRedirect('/login/')


@login_required(login_url='/login/')
def registerevent(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'registerevent.html', c)


@login_required(login_url='login/')
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
    return HttpResponseRedirect('/eventlist/?dept=' + request.POST.get('dept'))


def storepart(request):
    p = Participant(firstname=request.POST.get('fname'),
                    lastname=request.POST.get('lname'),
                    event_id=request.GET.get(''),
                    birthdate=request.POST.get('dob'),
                    college_name=request.POST.get('college'),
                    gender=request.POST.get('gender'),
                    department=request.POST.get('dept'),
                    mobile=request.POST.get('mobile'),
                    email=request.POST.get('eid'),
                    )
    p.save()
    return HttpResponseRedirect()
