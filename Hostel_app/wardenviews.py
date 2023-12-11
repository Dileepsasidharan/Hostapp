from django.contrib import messages
from django.shortcuts import render, redirect

from Hostel_app.forms import in_outform
from Hostel_app.models import Student, Parent, Leaveapp, In_out


def studentview_ward(request):
    data = Student.objects.all()
    return render(request,'warden/student_view.html',{'data':data})

def parentview_ward(request):
    data = Parent.objects.all()
    return render(request,'warden/parent_view.html',{'data':data})

def leave_view(request):
    data = Leaveapp.objects.all()
    context = {
        'data': data,
    }
    return render(request,'warden/leave_view.html',context)

def approve_leave(request,id):
    data = Leaveapp.objects.get(id=id)
    data.status = 1
    data.save()
    messages.info(request, 'student approved successfully')
    return redirect('leave_view')

def reject_leave(request,id):
    leave = Leaveapp.objects.get(id=id)
    leave.status = 2
    leave.save()
    messages.info(request,'Leave rejected')
    return redirect('leave_view')

def in_outmark(request):
    form = in_outform()
    if request.method == 'POST':
        form = in_outform(request.POST)
        if form.is_valid():
            form.save()
        return redirect('view_inout')
    return render(request, 'warden/markin_out.html', {'form':form})

def view_inout(request):
    data = In_out.objects.all()
    context = {
        'data': data,
    }
    return render(request, 'warden/view_inout.html', context)


def update_in_reg(request,id):
    data = In_out.objects.get(id=id)
    form = in_outform(instance=data)
    if request.method == 'POST':
        form = in_outform(request.POST, instance=data)
        if form.is_valid():
            form.instance.status=1
            form.save()
            return redirect('view_inout')
    return render(request,'warden/intime_reg.html',{'form':form})

def register_inout_status(request,id):
    data = In_out.objects.get(id=id)
    data.status = 1
    data.save()
    messages.info(request, 'student entered the hostel')
    return redirect('view_inout')



