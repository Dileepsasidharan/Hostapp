import stripe
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from Hostel_app.forms import bookroomform, complaintform, addreview, recapform
from Hostel_app.models import Hostel, Food, Notifications, Parent, Bookroom, Attendance, Warden, Complaint, Review, \
    Recap, In_out, Student, Fees


def view_hostelparent(request):
    data = Hostel.objects.all()
    return render(request,'parent/view_hostel.html', {'data': data})

def view_foodparent(request):
    data = Food.objects.all()
    return render(request,'parent/view_food.html',{'data': data})

def view_notifiparent(request):
    data = Notifications.objects.all()
    return render(request,'parent/view_notification.html',{'data': data})




def delete_profile(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        messages.info(request,'Your Account Deleted Successfully')
        return redirect('hostlogin')
    return render(request, 'parent/delete_profile.html')

def bookroom_parent(request):
    parent = Parent.objects.get(user=request.user)
    form = bookroomform()
    if request.method == 'POST':
        form = bookroomform(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.student = parent.Student_name
            book.booked_by = request.user
            student_qs = Bookroom.objects.filter(student=parent.Student_name)
            if student_qs.exists():
                messages.info(request, 'You have already booked room')
            else:
                book.save()
                messages.info(request, 'Successfully Booked Room')
                return redirect('bookstatus_par')
    return render(request, 'parent/bookroom_parent.html', {'form': form})


def bookstatus_par(request):
    parent = Parent.objects.get(user=request.user)
    status = Bookroom.objects.filter(student=parent.Student_name)
    return render(request,'parent/bookstatus_par.html',{'status':status})

def view_attendance(request):
    parent = Parent.objects.get(user=request.user)
    attendance = Attendance.objects.filter(student=parent.Student_name)
    return render(request,'parent/view_attendance.html',{'attendance':attendance})

def wardenview_par(request):
    data = Warden.objects.all()
    return render(request,'parent/wardenview_par.html',{'data':data})

def add_complaint_par(request):
    form = complaintform()
    u = request.user
    if request.method == 'POST':
        form = complaintform(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'complaint added successfully')
            return redirect('base2')
    return render(request, 'parent/add_complaint.html', {'form': form})


def view_complaint_par(request):
    data = Complaint.objects.filter(user=request.user)
    return render(request, 'parent/view_complaint.html', {'data': data})

def addreview_par(request):
    form = recapform()
    u = request.user
    if request.method == 'POST':
        form = recapform(request.POST)
        f = form.save(commit=False)
        f.user = u
        f.save()
        messages.info(request, 'Your review send successfully')
        return redirect('base2')
    return render(request,'parent/addreview.html',{'form':form})




def view_review_par(request):
    data= Recap.objects.all()
    return render(request,'parent/view_review.html', {'data': data})


def base2(request):
    return render(request,'parent/base.html')

def view_in_out_reg(request):
    parent = Parent.objects.get(user=request.user)
    status = In_out.objects.filter(student=parent.Student_name)
    return render(request,'parent/view_in_out.html',{'status':status})

def view_fee_p(request):
    parent = Parent.objects.get(user=request.user)
    data = Fees.objects.filter(student=parent.Student_name)
    return render(request, 'parent/view_fee.html', {'data': data})

def view_bill_detail_p(request,id):
    data1 = Fees.objects.get(id=id)
    student = Student.objects.filter(name=data1.student)
    return render(request, 'parent/view_bill_details.html', {'data1': data1, 'student': student})


def par_checkout_session(request, id):
    parent = Parent.objects.get(user=request.user)
    payment = Fees.objects.get(pk=id)

    stripe.api_key = stripe.api_key
    amount_in_cents = int(payment.get_total() * 100)
    student_email = parent.email
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/par_pay_success/?payment_id={}'.format(payment.id),
        cancel_url='http://127.0.0.1:8000/par_pay_cancel',
        payment_method_types=['card'],
        mode='payment',
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'unit_amount': amount_in_cents,
                'product_data': {
                    'name': payment.student,
                },
            },
            'quantity': 1,
        }],
        customer_email=student_email

    )
    return redirect(session.url, code=303)


def par_pay_success(request):
    payment_id=request.GET.get('payment_id')
    payment = get_object_or_404(Fees, pk=payment_id)
    payment.status = 1
    payment.save()
    return render(request,'parent/pay_success.html')

def par_pay_cancel(request):
    return render(request,'parent/pay_cancel.html')



