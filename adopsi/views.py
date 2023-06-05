from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import AdopsiForm
from .models import Adopsi, Register_Adopsi
from user.models import Customer, User
from django.conf import settings
from django.db import IntegrityError, connection
from django.db import connection
from datetime import datetime
import shortuuid

# Create your views here.
def is_authenticated(request):
    try:
        request.session['Username']
        return True
    except:
        return False

def create_adopsi(request):
    if is_authenticated(request):
        if request.session['Role'] == 'Karyawan':
            form = AdopsiForm()
            if request.method == 'POST':
                form = AdopsiForm(request.POST or None)
                if form.is_valid():
                    hewan = form.save(commit=False)
                    hewan.status = 'Belum diadopsi'
                    hewan.save()
                    success_message = 'Hewan adopsi berhasil ditambah!'
                    return render(request, 'adopt_success.html', {'success_message': success_message})
                else:
                    print("FORM ERROR:\n")
                    print(form.errors)
                    print("\nItu errornya di atas")
            return render(request, 'create_adopsi.html', {'form': form})
        else:
            context = {
            'error_message': 'Access denied!'}
            return render(request, 'adopt_error.html', context)
    else:
        return HttpResponseRedirect("/adopsi")

def list_hewan_adopsi(request):
    if request.session['Role'] == 'Customer':
        all_hewan = Adopsi.objects.filter(status="Belum diadopsi")
    else:
        all_hewan = Adopsi.objects.all().values

    context = {
        'all_hewan': all_hewan,
    }

    return render(request, 'list_hewan_adopsi.html', context)


def update_adopsi(request, user_id):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    # Mencari user
    cursor.execute("""
    SELECT *
    FROM adopsi_adopsi
    WHERE hewan_id = '{0}' ;
    """.format(user_id))
    user = cursor.fetchall()
    list_jenis = ["Kucing", "Anjing", "Kelinci"]
        
    response = {
            'user_id':user_id,
            'user':user,
            'list_jenis': list_jenis,}
    cursor.close()
    return render(request, 'update_adopsi.html', response)

def update_adopsi_handler(request, user_id):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    # get data dari form
    nama = request.GET.get('nama')
    jenis = request.GET.get('jenis')
    ras = request.GET.get('ras')
    warna = request.GET.get('warna')
    deskripsi = request.GET.get('deskripsi')

    try:
        # update
       cursor.execute("""
       UPDATE adopsi_adopsi
       SET nama = '{0}', jenis = '{1}', ras = '{2}', warna = '{3}', deskripsi = '{4}'
       WHERE hewan_id = '{5}';
       """.format(nama, jenis, ras, warna, deskripsi, user_id))
       success_message = 'Hewan berhasil diupdate!'
       return render(request, 'adopt_success.html', {'success_message': success_message})
    except IntegrityError:
        # If the field is not unique, return an error message
        error_message = 'There was an error.'
        cursor.execute("""
        SELECT *
        FROM user_user
        WHERE id = '{0}' ;
        """.format(user_id))
        user = cursor.fetchall()
        response = {
            'error_message': error_message,
            'user':user,
            'user_id': user_id}
        return render(request, 'update_adopsi.html', response)

        
    cursor.close()
    return HttpResponseRedirect('/adopsi')

def delete_adopsi(request, hewan_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Karyawan':
            hewan_adopsi = Adopsi.objects.get(hewan_id=hewan_id)

            hewan_adopsi.delete()
            return HttpResponseRedirect('/adopsi')
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/adopsi")

def read_adopsi(request, hewan_id):
    cursor = connection.cursor()
    response = {}
    
    if is_authenticated(request):
            if request.method != "POST":
                cursor.execute("SET SEARCH_PATH TO PUBLIC;")
                if len(request.session.keys()) == 0:
                        return redirect('/')
                
                # Fetch object Adopsi
                cursor.execute("""
                SET SEARCH_PATH TO PUBLIC;
                SELECT * 
                FROM adopsi_adopsi  
                WHERE hewan_id= '{0}';
                """.format(hewan_id))
                adopsi = cursor.fetchall()
    
                cursor.close()

                response['adopsi'] = adopsi
                response['hewan_id'] = hewan_id
                
                # Fetch data role user yang sedang login
                role = request.session['Role']
                response['role'] = role

                # Filter object Register_Adopsi hanya adopsi yang sedang dibuka
                reg_adopsi_filtered = Register_Adopsi.objects.filter(hewan_id=hewan_id)
                
                button_bool = 0 
                # Ambil customer yang sedang login
                if request.session['Role'] == 'Customer':
                    uname = request.session['Username']
                    user = User.objects.get(username=uname)
                    customer = Customer.objects.get(user_ptr=user)
                    for i in reg_adopsi_filtered:                         
                         if i.customer == customer: # Restrict button daftar adopsi untuk Customer yang telah mendaftar????
                            button_bool = 1 
                     


                for i in reg_adopsi_filtered:  
                    print(i.id)
                response['reg_adopsi'] = reg_adopsi_filtered
                response['button_bool'] = button_bool
                return render(request, 'read_adopsi.html', response)
    else:
        return HttpResponseRedirect("/login")
    

def register_adopsi(request, hewan_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Customer':
            # Filter object Register_Adopsi hanya adopsi yang sedang dibuka
            reg_adopsi_filtered = Register_Adopsi.objects.filter(hewan_id=hewan_id)

            # Fetch object Customer
            uname = request.session['Username']
            user = User.objects.get(username=uname)
            customer = Customer.objects.get(user_ptr=user)
            
            regist_bool = 0
            for i in reg_adopsi_filtered:
                if i.customer == customer: # Restrict fungsi daftar adopsi untuk Customer yang telah mendaftar???
                    regist_bool = 1 

            if regist_bool == 0:
                try:
                    adopsi = Adopsi.objects.get(hewan_id=hewan_id)
                except Adopsi.DoesNotExist:
                    return redirect('list_adopsi')

                response = {
                    'adopsi': adopsi,
                    'customer': customer
                }
                if request.method == 'POST':
                    date = datetime.now()
                    status = "Menunggu konfirmasi"
                    id = shortuuid.uuid()[:6]
                    alasan = request.POST.get('alasan')

                    register_adopsi = Register_Adopsi(customer=customer, hewan=adopsi, date=date)
                    # register_adopsi.save()
                    cursor = connection.cursor()
                    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

                    cursor.execute("""
                        INSERT INTO adopsi_register_adopsi(id, date, customer_id, hewan_id, status, date_adopted, alasan)
                        VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');
                        """.format(id, date, customer.id, hewan_id, status, date, alasan)) 
                    
                    reg_event_filtered = Register_Adopsi.objects.filter(hewan=adopsi)
                    jumlah_pendaftar= reg_event_filtered.count()
                    print(reg_event_filtered)
                    
                    cursor.execute("""
                    UPDATE adopsi_adopsi
                    SET quantity = '{0}'
                    WHERE hewan_id = '{1}';
                    """.format(jumlah_pendaftar, hewan_id))

                    
                    success_message = 'Berhasil mengajukan Adopsi!'
                    return render(request, 'adopt_success.html', {'success_message': success_message})

                return render(request, 'registration_adopsi.html', response)
            else:
                context = {
                'error_message': 'Akses Ditolak!'}
                return render(request, 'adopt_error.html', context)
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'adopt_error.html', context)
    else:
        return HttpResponseRedirect("/adopsi")


def list_adopsi_customer(request):
    uname = request.session['Username']
    user = User.objects.get(username=uname)
    customer = Customer.objects.get(user_ptr=user)
    
    reg_adopsi_filtered = Register_Adopsi.objects.filter(customer_id=customer.id)
    # list_adopsi_status = []
    # list_adopsi_customer = []
    # for i in reg_adopsi_filtered:
    #     hewan = Adopsi.objects.get(hewan_id=i.hewan_id) 
    #     list_adopsi_customer.append(hewan)
    #     list_adopsi_status.append(i.status)

    
    context = {
        # 'list_adopsi_customer': list_adopsi_customer,
        'reg_adopsi': reg_adopsi_filtered
    }

    return render(request, 'list_adopsi_customer.html', context)

def approve_adopsi(request, hewan_id, id):
    if is_authenticated(request):
        if request.session['Role'] == 'Karyawan':
            hewan = Adopsi.objects.get(hewan_id=hewan_id)
            reg_adopsi_filtered = Register_Adopsi.objects.filter(hewan_id=hewan_id)

            status = "Diadopsi"
            status_registeradopsi = "Disetujui"
            adopsi_time = datetime.now()
            cursor = connection.cursor()
            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            cursor.execute("""
                UPDATE adopsi_adopsi
                SET status = '{0}'
                WHERE hewan_id = '{1}';
                """.format(status, hewan_id)) 

            cursor.execute("""
                UPDATE adopsi_register_adopsi
                SET status = '{0}'
                WHERE id = '{1}';
                """.format(status_registeradopsi, id))

            cursor.execute("""
                UPDATE adopsi_register_adopsi
                SET date_adopted = '{0}'
                WHERE id = '{1}';
                """.format(adopsi_time, id))
            
            for i in reg_adopsi_filtered:
                if i.status == "Menunggu konfirmasi":
                    status_registeradopsi = "Tidak Disetujui"
                    cursor.execute("""
                    UPDATE adopsi_register_adopsi
                    SET status = '{0}'
                    WHERE id = '{1}';
                    """.format(status_registeradopsi, i.id))
                          
            success_message = 'Berhasil menyetujui Adopsi!'
            cursor.close()
            return render(request, 'adopt_success.html', {'success_message': success_message})
                     
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")

def disapprove_adopsi(request, hewan_id, id):
    if is_authenticated(request):
        if request.session['Role'] == 'Karyawan':
            
            status_registeradopsi = "Tidak disetujui"
            cursor = connection.cursor()
            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            cursor.execute("""
                UPDATE adopsi_register_adopsi
                SET status = '{0}'
                WHERE id = '{1}';
                """.format(status_registeradopsi, id))  
                          
            success_message = 'Berhasil menolak Adopsi!'
            cursor.close()
            return render(request, 'adopt_success.html', {'success_message': success_message})
                     
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")