import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import EventForm
from .models import Event
from datetime import datetime, timedelta, timezone
from django.contrib import messages
from django.db import IntegrityError, connection

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
            'error_message': 'Akses Ditolak!'}
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

def update_event(request, event_id):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    # Mencari user
    cursor.execute("""
    SELECT *
    FROM events_event
    WHERE id = '{0}' ;
    """.format(event_id))
    event = cursor.fetchall()
        
    response = {
            'event_id':event_id,
            'event':event,}
    cursor.close()
    return render(request, 'update_event.html', response)

def update_event_handler(request, event_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Karyawan':
            cursor = connection.cursor()
            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            # get data dari form
            title = request.GET.get('title')
            general_location = request.GET.get('general_location')
            specific_location = request.GET.get('specific_location')
            start_time = request.GET.get('start_time')
            end_time = request.GET.get('end_time')
            description = request.GET.get('description')
            isVIP = request.GET.get('isVIP')

            try:
                # update
                cursor.execute("""
                UPDATE events_event
                SET title = '{0}', general_location = '{1}', specific_location = '{2}', start_time = '{3}', end_time = '{4}', description = '{5}'
                WHERE id = '{6}';
                """.format(title, general_location, specific_location, start_time, end_time, description, event_id))                
                success_message = 'Event updated successfully!'
                cursor.close()
                return render(request, 'success_page.html', {'success_message': success_message})
            except IntegrityError:
                # If the field is not unique, return an error message
                error_message = 'Event is already taken. Please choose another one.'
                cursor.execute("""
                SELECT *
                FROM events_event
                WHERE id = '{0}' ;
                """.format(event_id))
                event = cursor.fetchall()
                response = {
                    'error_message': error_message,
                    'event':event,
                    'event_id': event_id}
                cursor.close()
                
                return render(request, 'update_event.html', response)
        else:
            context = {
            'error_message': 'Access denied!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")
   

   


def read_event(request, event_id):
        cursor = connection.cursor()
        
        if request.method != "POST":
                cursor.execute("SET SEARCH_PATH TO PUBLIC;")
                if len(request.session.keys()) == 0:
                        return redirect('/')
                if request.session['Role'] == 'Customer':
                    uname = request.session['Username']
                    cursor.execute("SET search_path TO public")
                    cursor.execute("""
                    SELECT user_customer.is_vip FROM user_customer
                    INNER JOIN user_user ON user_user.id = user_customer.user_ptr_id
                    WHERE user_user.username = %s;
                    """, [uname])
                    isvip_cust = cursor.fetchall()

                cursor.execute("""
                SET SEARCH_PATH TO PUBLIC;
                SELECT * 
                FROM events_event  
                WHERE ID= '{0}';
                """.format(event_id))
                event = cursor.fetchall()
    
                response = {'event': event, 
                            'event_id': event_id,
                            'isvip_cust': isvip_cust}
                cursor.close()
                return render(request, 'read_event.html', response)
       
def register_event(request):
    if is_authenticated(request):
        if request.session['Role'] == 'Customer':
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
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")
# Create your views here.
