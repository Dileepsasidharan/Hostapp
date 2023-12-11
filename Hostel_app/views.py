from django.contrib import auth, messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from Hostel_app.forms import UserRegister, Studentform, Parentform


# Create your views here.
def hostapp(request):
    return render(request,'index.html')
def hostlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password= request.POST.get('password')
        user=auth.authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            login(request,user)
            return redirect('admin_dash')
        elif user is not None and user.is_warden:
            login(request, user)
            return redirect('warden_dash')
        elif user is not None and user.is_student:
            if user.student.approval_status == True:
                login(request, user)
                return redirect('base1')
            else:
                messages.info(request,"You are not aproved to login")
        elif user is not None and user.is_parent:
            if user.parent.approval_status == True:
                login(request, user)
                return redirect('parent_dash')
        else:
            messages.info(request,"Not registrated user")
    return render(request,'log-in.html')


class Studentreg:
    pass


def signupreg(request):

    return render(request,'studentsign-up.html')

def admin_dash(request):
    return render(request,'adminindex.html')

def student_signupreg(request):
    u_form = UserRegister(request.POST)
    s_form = Studentform(request.POST)
    if request.method == 'POST':
        u_form = UserRegister(request.POST)
        s_form = Studentform(request.POST,request.FILES)
        if u_form.is_valid() and s_form.is_valid():
            user = u_form.save(commit=False)
            user.is_student = True
            user.save()
            student = s_form.save(commit=False)
            student.user = user
            student.save()
            messages.info(request, "Student registered successfully")
            return redirect('hostlogin')
    return render(request, 'studentsign-up.html', {'u_form': u_form, 's_form': s_form})


def warden_signupreg(request):
    return render(request,'wardensign-up.html')
def parent_signupreg(request):
    u_form = UserRegister(request.POST)
    p_form = Parentform(request.POST)
    if request.method == 'POST':
        u_form = UserRegister(request.POST)
        p_form = Parentform(request.POST,request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save(commit=False)
            user.is_parent = True
            user.save()
            parent = p_form.save(commit=False)
            parent.user = user
            parent.save()
            messages.info(request, "Parent registered successfully")
            return redirect('hostlogin')
    return render(request, 'parentsign-up.html', {'u_form': u_form, 'p_form': p_form})

def parent_dash(request):
    return render(request,'parentadmindash.html')
def student_dash(request):
    return render(request,'studentadmindash.html')

def warden_dash(request):
    return render(request,'wardenadmindash.html')
def log_out(request):
    logout(request)
    return redirect('hostapp')
