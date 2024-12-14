from django.shortcuts import render, redirect
from .models import Schedule
from .forms import ScheduleForm, LoginForm, UserRegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from openpyxl import Workbook


class UserLoginView(LoginView):
    template_name = 'schedule/login.html'
    form_class = LoginForm

def home(request):
    return render(request, 'schedule/home.html')

def schedule_list(request):
    schedules = Schedule.objects.all()
    return render(request, 'schedule/schedule_list.html', {'schedules': schedules})


def add_schedule(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule_list')
    else:
        form = ScheduleForm()
    return render(request, 'schedule/add_schedule.html', {'form': form})

@login_required
def schedule_search(request):
    query = request.GET.get('q', '')
    results = None

    if query:
        results = Schedule.objects.filter(
            Q(subject__name__icontains=query) | 
            Q(subject__group__name__icontains=query) 
        ).select_related('subject')  

    return render(request, 'schedule/schedule_search.html', {'query': query, 'results': results})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user) 
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')  
    else:
        form = UserRegistrationForm()
    return render(request, 'schedule/register_user.html', {'form': form})


@login_required  
def office(request):
    user_groups = request.user.groups.all()
    schedule = Schedule.objects.filter(subject__group__name__in=[group.name for group in user_groups])
    return render(request, 'schedule/office.html', {'user': request.user, 'schedule': schedule})



def download_schedule(request):

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Расписание"


    sheet.append(["Название предмета", "Дата", "Время", "Кабинет"])


    schedules = Schedule.objects.all()


    for schedule in schedules:
        sheet.append([
            schedule.subject.name,
            schedule.date.strftime("%d-%m-%Y"),
            schedule.time.strftime("%H:%M"),
            schedule.cabinet or "—"
        ])


    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="schedule.xlsx"'
    workbook.save(response)

    return response