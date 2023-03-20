import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import EventForm
from .models import Event
from datetime import datetime, timedelta, timezone
from django.contrib import messages

def is_authenticated(request):
    try:
        request.session['Username']
        return True
    except:
        return False

def create_event(request):
    if is_authenticated(request):
        if request.session['Role'] == 'Karyawan':
            form = EventForm()
            if request.method == 'POST':
                form = EventForm(request.POST or None)
                if form.is_valid():
                    form.save()
                    success_message = 'Event created successfully!'
                    return render(request, 'success_page.html', {'success_message': success_message})

            return render(request, 'create_event.html', {'form': form})
        else:
            context = {
            'error_message': 'Access denied!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")

    
    

def list_event(request):
    # Filter Event Today
    current_date_min = datetime.combine(datetime.now().date(), datetime.today().time().min)
    current_date_max = datetime.combine(datetime.now().date(), datetime.today().time().max)
    today_events = Event.objects.filter(start_time__range=[current_date_min, current_date_max])

    # Filter Event Upcoming
    startdate_upcoming = datetime.today() + timedelta(days=1)
    enddate_upcoming = startdate_upcoming + timedelta(days=99999)
    upcoming_events = Event.objects.filter(start_time__range=[startdate_upcoming, enddate_upcoming])

    # Filter Event Past
    enddate_past = datetime.combine(datetime.now().date(), datetime.today().time().max) - timedelta(days=1)
    startdate_past = enddate_past - timedelta(days=99999)
    past_events = Event.objects.filter(start_time__range=[startdate_past, enddate_past])

    all_events = Event.objects.all().values

    context = {
        'all_events': all_events,
        'past_events': past_events,
        'today_events': today_events,
        'upcoming_events': upcoming_events,
    }

    
    return render(request, 'list_event.html', context)

# Create your views here.