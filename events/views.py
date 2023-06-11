import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from user.models import Customer, User
from .forms import EventForm
from .models import Event, Register_Event
from datetime import datetime, timedelta, timezone
from django.contrib import messages
from django.db import IntegrityError, connection
import shortuuid

def is_authenticated(request):
    try:
        request.session['Username']
        return True
    except:
        return False

def create_event(request):
    if is_authenticated(request):
        if request.session['Role'] == 'Karyawan':
            username = request.session['Username']
            form = EventForm()
            if request.method == 'POST':
                form = EventForm(request.POST or None)
                if form.is_valid():
                    form.save()
                    success_message = 'Berhasil membuat Event!'
                    return render(request, 'success_page.html', {'success_message': success_message})

            return render(request, 'create_event.html', {'form': form, 'username': username})
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
    startdate_upcoming = datetime.today()
    enddate_upcoming = startdate_upcoming + timedelta(days=99999)
    upcoming_events = Event.objects.filter(start_time__range=[startdate_upcoming, enddate_upcoming])

    # Filter Event Past
    enddate_past = datetime.combine(datetime.now().date(), datetime.today().time().max) - timedelta(days=1)
    startdate_past = enddate_past - timedelta(days=99999)
    past_events = Event.objects.filter(start_time__range=[startdate_past, enddate_past])

    all_events = Event.objects.all().values

    username = request.session['Username']
    context = {
        'all_events': all_events,
        'past_events': past_events,
        'today_events': today_events,
        'upcoming_events': upcoming_events,
        'username': username
    }

    if request.session['Role'] == 'Customer':
        uname = request.session['Username']
        user = User.objects.get(username=uname)
        customer = Customer.objects.get(user_ptr=user)
        cust_login_id = customer.id
        # Filter object Register_Event yang telah didaftarkan Customer (yang sedang login)
        reg_event_filtered = Register_Event.objects.filter(customer_id=cust_login_id)
        context['registered_events'] = reg_event_filtered
        context['customer_id'] = cust_login_id

    
    return render(request, 'list_event.html', context)

def read_event(request, event_id):
    cursor = connection.cursor()
    response = {}
    uname = request.session['Username']

    if is_authenticated(request):
            if request.method != "POST":
                cursor.execute("SET SEARCH_PATH TO PUBLIC;")
                if len(request.session.keys()) == 0:
                        return redirect('/')
                # Ambil isVIP value Customer untuk keperluan restict button daftar event VIP
                if request.session['Role'] == 'Customer':
                    cursor.execute("SET search_path TO public")
                    cursor.execute("""
                    SELECT user_customer.is_vip FROM user_customer
                    INNER JOIN user_user ON user_user.id = user_customer.user_ptr_id
                    WHERE user_user.username = %s;
                    """, [uname])
                    isvip_cust = cursor.fetchall()
                    response['isvip_cust'] = isvip_cust

                # Fetch object Event
                cursor.execute("""
                SET SEARCH_PATH TO PUBLIC;
                SELECT * 
                FROM events_event  
                WHERE ID= '{0}';
                """.format(event_id))
                event = cursor.fetchall()
    
                cursor.close()

                response['event'] = event
                response['event_id'] = event_id
                response['username'] = uname
                
                # Fetch data role user yang sedang login
                role = request.session['Role']
                response['role'] = role

                # Filter object Register_Event hanya event saat ini (yang sedang dibuka)
                reg_event_filtered = Register_Event.objects.filter(event_id=event_id)
                
                button_bool = 0 
                # Ambil customer yang sedang login
                if request.session['Role'] == 'Customer':
                    uname = request.session['Username']
                    user = User.objects.get(username=uname)
                    customer = Customer.objects.get(user_ptr=user)
                    for i in reg_event_filtered:
                         if i.customer == customer: # Restrict button daftar event untuk Customer yang telah mendaftar
                            button_bool = 1 

                response['reg_event'] = reg_event_filtered
                response['button_bool'] = button_bool
                return render(request, 'read_event.html', response)
    else:
        return HttpResponseRedirect("/login")
        
def register_event(request, event_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Customer':
            # Filter object Register_Event hanya event saat ini (yang sedang dibuka)
            reg_event_filtered = Register_Event.objects.filter(event_id=event_id)

            # Fetch object Customer
            uname = request.session['Username']
            user = User.objects.get(username=uname)
            customer = Customer.objects.get(user_ptr=user)
            
            regist_bool = 0
            for i in reg_event_filtered:
                if i.customer == customer: # Restrict fungsi daftar event untuk Customer yang telah mendaftar
                    regist_bool = 1 

            if regist_bool == 0:
                try:
                    event = Event.objects.get(id=event_id)
                except Event.DoesNotExist:
                    return redirect('list_event')

                response = {
                    'event': event,
                    'customer': customer,
                    'username': uname
                }
                if request.method == 'POST':
                    date = datetime.now()

                    register_event = Register_Event(customer=customer, event=event, date=date)
                    register_event.save()
                    
                    success_message = 'Berhasil mendaftar Event!'
                    reg_event_filtered = Register_Event.objects.filter(event_id=event_id)
                    jumlah_pendaftar= reg_event_filtered.count()
                    
                    cursor = connection.cursor()
                    cursor.execute("""
                    UPDATE events_event
                    SET quantity = '{0}'
                    WHERE id = '{1}';
                    """.format(jumlah_pendaftar+1, event_id))
                    return render(request, 'success_page.html', {'success_message': success_message})

                return render(request, 'registration_event.html', response)
            else:
                context = {
                'error_message': 'Akses Ditolak!'}
                return render(request, 'error_page.html', context)
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")
       
def tiket_event(request, tiket_id, customer_id):
    if is_authenticated(request):
        cursor = connection.cursor()
        response = {}
            
        cursor.execute("SET SEARCH_PATH TO PUBLIC;")
        if len(request.session.keys()) == 0:
            return redirect('/')

        # Ambil isVIP value Customer untuk keperluan restict button daftar event VIP
        if request.session['Role'] == 'Customer':

            customer = Customer.objects.get(id=customer_id)

            # Fetch object Customer login
            uname = request.session['Username']
            user = User.objects.get(username=uname)
            customer_login = Customer.objects.get(user_ptr=user)

            if customer_login.id == customer.id: 
                # Fetch object Register_Event
                cursor.execute("""
                SET SEARCH_PATH TO PUBLIC;
                SELECT * 
                FROM events_register_event  
                WHERE ID= '{0}';
                """.format(tiket_id))
                tiket_event = cursor.fetchall()

                event_id = tiket_event[0][3]

                # Fetch object Event
                cursor.execute("""
                SET SEARCH_PATH TO PUBLIC;
                SELECT * 
                FROM events_event  
                WHERE ID= '{0}';
                """.format(event_id))
                event = cursor.fetchall()

                response = {
                'tiket_event': tiket_event,
                'event': event,
                'customer': customer,
                'username': uname
                }
            
                cursor.close()

                return render(request, 'tiket_event.html', response)
            else:
                context = {
                'error_message': 'Akses Ditolak!'}
                return render(request, 'error_page.html', context)
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")
    

def delete_event(request, event_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Karyawan':
            event = Event.objects.get(id=event_id)

            reg_event_filtered = Register_Event.objects.filter(event_id=event_id)
            if reg_event_filtered:
                context = {
                    'error_message': 'Tidak bisa menghapus Event yang telah memiliki pendaftar.'}
                return render(request, 'error_page.html', context)
            else:
                event.delete()
                return HttpResponseRedirect('/event/')
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")
    

def update_event(request, event_id):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    username = request.session['Username']
    reg_event_filtered = Register_Event.objects.filter(event_id=event_id)
    if reg_event_filtered:
        context = {
            'error_message': 'Tidak bisa mengubah Event yang telah memiliki pendaftar.'}
        return render(request, 'error_page.html', context)
    else:
        # Mencari user
        cursor.execute("""
        SELECT *
        FROM events_event
        WHERE id = '{0}' ;
        """.format(event_id))
        event = cursor.fetchall()
            
        response = {
                'event_id':event_id,
                'event':event,
                'username': username}
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
            # isVIP = request.GET.get('isVIP')

            try:
                # update
                cursor.execute("""
                UPDATE events_event
                SET title = '{0}', general_location = '{1}', specific_location = '{2}', start_time = '{3}', end_time = '{4}', description = '{5}'
                WHERE id = '{6}';
                """.format(title, general_location, specific_location, start_time, end_time, description, event_id))                
                success_message = 'Data Event berhasil diubah!'
                cursor.close()
                return render(request, 'success_page.html', {'success_message': success_message})
            except IntegrityError:
                # If the field is not unique, return an error message
                error_message = 'Event sudah ada. Pilih nama lain.'
                cursor.execute("""
                SELECT *
                FROM events_event
                WHERE id = '{0}' ;
                """.format(event_id))
                event = cursor.fetchall()
                username = request.session['Username']
                response = {
                    'error_message': error_message,
                    'event':event,
                    'event_id': event_id,
                    'username': username}
                cursor.close()
                
                return render(request, 'update_event.html', response)
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")
   

   

        