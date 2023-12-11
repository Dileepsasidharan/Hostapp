import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse

from Hostel_app.forms import add_hostel, add_food, notification, add_warden, UserRegister, attform, AddFee
from Hostel_app.models import Hostel, Food, Notifications, Warden, User, Student, Parent, Review, Complaint, Bookroom, \
    Attendance, Recap, Fees


def addhostel(request):
    h_form = add_hostel()
    if request.method == 'POST':
        h_form = add_hostel(request.POST,request.FILES)
        if h_form.is_valid():
            h_form.save()
        return redirect('viewhostel')
    return render(request, 'admin/addhostel.html', {'h_form': h_form})

def viewhostel(request):
    data = Hostel.objects.all()
    return render(request, 'admin/viewhostel.html', {'data': data})

def updatehostel(request,id):
    data = Hostel.objects.get(id=id)
    form = add_hostel(instance=data)
    if request.method == 'POST':
        form = add_hostel(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('viewhostel')
    return render(request,'admin/updatehostel.html',{'form':form})
def deletehostel(request,id):
    Hostel.objects.get(id=id).delete()
    return redirect('viewhostel')

def addfood(request):
    h_form = add_food()
    if request.method == 'POST':
        h_form = add_food(request.POST,request.FILES)
        if h_form.is_valid():
            h_form.save()
        return redirect('viewfood')
    return render(request, 'admin/addfood.html', {'h_form': h_form})
def viewfood(request):
    data = Food.objects.all()
    return render(request, 'admin/viewfood.html', {'data': data})
def updatefood(request,id):
    data = Food.objects.get(id=id)
    form = add_food(instance=data)
    if request.method == 'POST':
        form = add_food(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('viewfood')
    return render(request,'admin/updatefood.html',{'form':form})
def deletefood(request,id):
    Food.objects.get(id=id).delete()
    return redirect('viewfood')


def add_notification():
    pass


def addnotification(request):
    h_form = notification()
    if request.method == 'POST':
        h_form = notification(request.POST,request.FILES)
        if h_form.is_valid():
            h_form.save()
        return redirect('admin_dash')
    return render(request, 'admin/addnotification.html', {'h_form': h_form})

def viewnotification(request):
    data = Notifications.objects.all()
    return render(request, 'admin/viewnotification.html', {'data': data})
def updatenotification(request,id):
    data = Notifications.objects.get(id=id)
    form = notification(instance=data)
    if request.method == 'POST':
        form = notification(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('viewnotification')
    return render(request,'admin/updatenotification.html',{'form':form})
def deletenotification(request,id):
    Notifications.objects.get(id=id).delete()
    return redirect('viewnotification')


def warden_details():
    pass


def addwarden(request):
    u_form = UserRegister()
    w_form = add_warden()
    if request.method == 'POST':
        u_form = UserRegister(request.POST)
        w_form = add_warden(request.POST,request.FILES)
        if u_form.is_valid() and w_form.is_valid():
            user = u_form.save(commit=False)
            user.is_warden = True
            user.save()
            warden = w_form.save(commit=False)
            warden.user = user
            warden.save()
            messages.info(request, "Warden registered successfully")
            return redirect('admin_dash')
    return render(request, 'admin/addwarden.html', {'u_form': u_form, 'w_form': w_form})

def viewwarden(request):
    data = Warden.objects.all()
    return render(request, 'admin/viewwarden.html', {'data': data})

def updatewarden(request,id):
    data = Warden.objects.get(id=id)
    w_form = add_warden(instance=data)
    if request.method == 'POST':
        w_form = add_warden(request.POST, instance=data)
        if w_form.is_valid():
            w_form.save()
            return redirect('viewwarden')
    return render(request,'admin/updatewarden.html',{'w_form':w_form})
def deletewarden(request,id):
   data1=Warden.objects.get(id=id)
   data = User.objects.get(warden=data1)
   if request.method=='POST':
       data.delete()
       return redirect('viewwarden')
   else:
       return redirect('viewwarden')

def viewregistration(request):
    data = Student.objects.all()
    data1 = Parent.objects.all()
    context = {
        'data': data,
        'data1': data1
    }
    return render(request, 'admin/viewregistration.html', context)

def approve_student(request,id):
    data = Student.objects.get(user_id=id)
    data.approval_status = True
    data.save()
    messages.info(request,'student approved successfully')
    return redirect('viewregistration')

def reject_student(request,id):
    data1 = Student.objects.get(user_id=id)
    data = User.objects.get(student=data1)
    if request.method == 'POST':
        data.delete()
        return redirect('viewregistration')
    else:
        return redirect('viewregistration')

def approve_parent(request,id):
    data1 = Parent.objects.get(user_id=id)
    data1.approval_status = True
    data1.save()
    messages.info(request,'Parent approved successfully')
    return redirect('viewregistration')

def reject_parent(request,id):
    data = Parent.objects.get(user_id=id)
    par = User.objects.get(parent=data)
    if request.method == 'POST':
        par.delete()
        return redirect('viewregistration')
    else:
        return redirect('viewregistration')

def viewreview_admin(request):
    data = Review.objects.all()
    data1 = Recap.objects.all()
    context = {
        'data': data,
        'data1': data1
    }
    return render(request, 'admin/viewreview.html',context)

def view_complaintadmin(request):
    data = Complaint.objects.all()
    return render(request,'admin/viewcomplaint.html', {'data':data})

def complaint_reply(request,id):
    f = Complaint.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST.get('reply')
        f.reply = r
        f.save()
        messages.info(request, 'Reply send for complaint')
        return redirect('complaint_view')
    return render(request, 'admin/complaint_reply.html', {'f': f})

def viewbookingstatus_admin(request):
    f = Bookroom.objects.all()
    return render(request,'admin/viewbookingstatus.html',{'f':f})

def confirm_booking(request,id):
    details_qs = Hostel.objects.all()
    if details_qs.exists():

        book = Bookroom.objects.get(id=id)
        book.status = 1
        book.save()

        hstl = Hostel.objects.all().last()
        occupied = hstl.Occupied_room
        hstl.Occupied_room = int(occupied) + 1
        hstl.save()
        messages.info(request,'Room booking confirmed')
        return redirect('viewbookingstatus_admin')
    else:
        messages.info(request,'Please update hostel details')
        return HttpResponseRedirect(reverse('viewbookingstatus_admin'))


def reject_booking(request,id):
    book = Bookroom.objects.all(id=id)
    if request.method == 'POST':
        book.status = 2
        book.save()
        messages.info(request,'Room booking rejected')
        return redirect('viewbookingstatus_admin')

def add_attendance(request):
    student = Student.objects.filter(approval_status=True)
    return render(request, 'admin/addattendance.html',{'student':student})


now=datetime.datetime.now()
def mark(request,id):
    user = Student.objects.get(user_id=id)
    att = Attendance.objects.filter(student=user, date=datetime.date.today())
    if att.exists():
        messages.info(request, "Todays attendance already marked for this student")
        return redirect('add_attendance')
    else:
        if request.method == 'POST':
            attndc = request.POST.get('attendance')
            Attendance(student=user, date=datetime.date.today(), status=attndc, time=now.time()).save()
            messages.info(request, 'Attendance added successfully')
            return redirect('add_attendance')
    return render(request, 'admin/mark_attendance.html')



def viewattendance_admin(request):
    value_list = Attendance.objects.values_list('date',flat=True).distinct()
    attendance = {}
    for i in value_list:
        attendance[i] = Attendance.objects.filter(date=i)
    return render(request,'admin/viewattendance.html',{'attendances':attendance})

def day_attendance(request,date):
    attendance = Attendance.objects.filter(date=date)
    context = {
        'attendance': attendance,
        'date': date
    }
    return render(request,'admin/day_attendance.html',context)


def add_fee(request):
    form = AddFee()
    if request.method == 'POST':
        form = AddFee(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill_qs = Fees.objects.filter(student=bill.student,from_date=bill.from_date, to_date=bill.to_date)
            if bill_qs.exists():
                messages.info(request, 'Bill Already added for the Student in this duration')
            else:
                bill.save()
                messages.info(request, 'Bill Added')
                return redirect('add_fee')

    return render(request, 'admin/add_fee.html', {'form': form})

def load_bill(request):
    student_id = request.GET.get('studentId')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    student = Student.objects.get(user_id=student_id)
    present_days = Attendance.objects.filter(student=student, date__range=[from_date, to_date]).count()
    amount = present_days * 60
    rent = 3000
    data = {
        'present_days': present_days,
        'mess_bill': amount,
        'room_rent': rent

    }

    return JsonResponse(data)

def view_fee(request):
    fee = Fees.objects.all()
    return render(request, 'admin/view_fee.html', {'fees': fee})


def view_bill_detail(request, id):
    data1 = Fees.objects.get(id=id)
    student = Student.objects.filter(name=data1.student)
    return render(request, 'admin/view_bill_details.html', {'data1': data1, 'student': student})





