import payment as payment
import stripe
from django.conf import settings
from django.contrib import messages
from django.core.mail import message
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from Hostel_app.forms import addreview, complaintform, bookroomform, leaveappform
from Hostel_app.models import Hostel, Food, Notifications, Review, Student, Complaint, Bookroom, Attendance, Leaveapp, \
    In_out, Fees


def view_hostel(request):
    data = Hostel.objects.all()
    return render(request,'student/view_hostel.html', {'data': data})

def view_food(request):
    data = Food.objects.all()
    return render(request,'student/view_food.html',{'data': data})
def view_notification(request):
    data = Notifications.objects.all()
    return render(request,'student/view_notification.html',{'data': data})
def base1(request):
    return render(request,'student/base.html')

def attendance_view(request):
    student = Student.objects.get(user=request.user)
    attendance = Attendance.objects.filter(student=student)
    return render(request,'student/attendance_view.html',{'attendance':attendance})


def add_review(request):
    s=Student.objects.get(user=request.user)
    r_form = addreview()
    if request.method == 'POST':
        r_form = addreview(request.POST)
        f=r_form.save(commit=False)
        f.student =s
        f.save()
        messages.info(request, 'Your review send successfully')
        return redirect('base1')
    return render(request,'student/addreview.html',{'r_form':r_form})

def view_review(request):
    data= Review.objects.all()
    return render(request,'student/view_review.html', {'data': data})

def update_review(request,id):
    data = Review.objects.get(id=id)
    r_form = addreview(instance=data)
    if request.method == 'POST':
        r_form = addreview(request.POST, instance=data)
        if r_form.is_valid():
            r_form.save()
            return redirect('view_review')
    return render(request,'student/update_review.html',{'r_form':r_form})

def delete_review(request,id):
    Review.objects.get(id=id).delete()
    return redirect('view_review')

def add_complaint(request):
    form = complaintform()
    u = request.user
    if request.method == 'POST':
        form = complaintform(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'complaint added successfully')
            return redirect('base1')
    return render(request, 'student/add_complaint.html', {'form': form})


def view_complaint(request):
    data = Complaint.objects.filter(user=request.user)
    return render(request, 'student/view_complaint.html', {'data': data})




def add_bookroom(request):
    form = bookroomform()
    if request.method =='POST':
        form = bookroomform(request.POST)
        if form.is_valid():
            book = form.save(commit=False)

            book.student = Student.objects.get(user=request.user)
            book.booking_date = form.cleaned_data.get("booking_date")
            book.booked_by = request.user
            student_qs = Bookroom.objects.filter(student=Student.objects.get(user=request.user))
            if student_qs.exists():
                messages.info(request,'You have already  booked room')
            else:
                book.save()
                messages.info(request, 'Successfully Booked Room')
                return redirect('base1')
    return render(request,'student/add_bookroom.html', {'form': form})

def view_bookingstatus(request):
    student = Student.objects.get(user=request.user)
    status = Bookroom.objects.filter(student=student)
    return render(request, 'student/view_bookingstatus.html', {'status': status})

def add_leaveapp(request):
    s = Student.objects.get(user=request.user)
    form = leaveappform()

    if request.method == 'POST':
        form = leaveappform(request.POST)
        f = form.save(commit=False)
        f.student = s
        f.save()
        messages.info(request, 'Your leave application send successfully')
        return redirect('base1')
    return render(request, 'student/add_leaveapp.html', {'form': form})



def view_leaveapp(request):
    student = Student.objects.get(user=request.user)
    status = Leaveapp.objects.filter(student=student)
    return render(request,'student/view_leaveapp.html',{'status':status})

def in_out_view(request):
    student = Student.objects.get(user=request.user)
    status = In_out.objects.filter(student=student)
    return render(request,'student/in_out_view.html',{'status':status})


def view_fee_st(request):
    student = Student.objects.get(user=request.user)
    data = Fees.objects.filter(student=student)
    return render(request, 'student/view_fee_st.html', {'data': data})

def view_bill_detail_s(request,id):
    data1 = Fees.objects.get(id=id)
    student = Student.objects.filter(name=data1.student)
    return render(request, 'student/view_bill_details.html', {'data1': data1, 'student': student})

stripe.api_key = 'sk_test_51NvZmeSDvM8krbirTzPuPORerOIKYduIA3qRZSROVutAy7MY2tv7zy9rYDoDkZsBJ9vCNmdJmNkjWOcIwjqSOcfO00pck0Zzhf'
def checkout_session(request,id):
  student = Student.objects.get(user=request.user)
  payment = Fees.objects.get(pk=id)
  messages.info(request, 'Paid Successfullly!!!')
  stripe.api_key = stripe.api_key
  amount_in_cents = int(payment.get_total() * 100)
  session = stripe.checkout.Session.create(
      success_url='http://127.0.0.1:8000/pay_success/?payment_id={}'.format(payment.id),
      cancel_url='http://127.0.0.1:8000/pay_cancel',
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

)
  return redirect(session.url, code=303)

def pay_success(request):
    payment_id=request.GET.get('payment_id')
    payment = get_object_or_404(Fees, pk=payment_id)
    payment.status = 1
    payment.save()
    return render(request,'student/pay_success.html')

def pay_cancel(request):
    return render(request,'student/pay_cancel.html')

