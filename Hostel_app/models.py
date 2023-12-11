from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    is_warden = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

class Student(models.Model):
     user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='student')
     name = models.CharField(max_length=50)
     address = models.CharField(max_length=100)
     email = models.EmailField()
     Phone_no=models.CharField(max_length=10)
     photo = models.ImageField(upload_to='profile')
     approval_status = models.BooleanField(default=0)
     course = models.CharField(max_length=50)

     def __str__(self):
         return self.name


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name='parent')
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    Student_name=models.ForeignKey(Student,on_delete=models.CASCADE)
    Phone_no = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='profile')
    approval_status = models.BooleanField(default=0)


    def __str__(self):
        return self.name

class Hostel(models.Model):
    Hostel_name = models.CharField(max_length=50)
    Hostel_address = models.CharField(max_length=100)
    Email = models.EmailField()
    Phone_no = models.CharField(max_length=10)
    Hostel_Images = models.ImageField(upload_to='Hostel_images')
    Total_room = models.CharField(max_length=50)
    Occupied_room = models.CharField(max_length=100)
    Room_rent = models.CharField(max_length=100)
    Room_facilities = models.CharField(max_length=100)

    def __str__(self):
        return self.Hostel_name

DAYS=(
    ('Sunday','Sunday'),
    ('Monday','Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday')
)
class Food(models.Model):
    day=models.CharField(max_length=50, choices=DAYS)
    Breakfast=models.CharField(max_length=100)
    Lunch=models.CharField(max_length=100)
    Dinner=models.CharField(max_length=100)

    def __str__(self):
        return self.day

class Notifications(models.Model):
    to = models.CharField(max_length=100)
    notification=models.TextField(max_length=100)
    time = models.TimeField()
    timestamp = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.to

class Warden(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='warden')
    Name = models.CharField(max_length=50)
    Address = models.CharField(max_length=100)
    Email = models.EmailField()
    Phone_no = models.CharField(max_length=10)
    Photo = models.ImageField(upload_to='wardenphoto')
    date_of_joining = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Name
class Review(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    Date= models.DateField(auto_now_add=True)
    Comments = models.CharField(max_length=100)

class Recap(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Date= models.DateField(auto_now_add=True)
    Comments = models.CharField(max_length=100)

class Complaint(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    complaint = models.CharField(max_length=100)
    reply = models.CharField(max_length=100,null=True,blank=True)


class Bookroom(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    booking_date = models.DateField()
    status = models.IntegerField(default=0)
    booked_by = models.ForeignKey(User,on_delete=models.CASCADE)


class Attendance(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    time = models.TimeField()

    status = models.CharField(max_length=100)

class Leaveapp(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    date_application = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=100)

    No_of_days_required=models.CharField(max_length=5)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.reason

    @property
    def date_diff(self):
        if self.start_date and self.end_date:
            d = self.end_date - self.start_date
            return d.days +1
        return None

class In_out(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='inOut')
    date = models.DateField(auto_now=True)
    in_time = models.TimeField(null=True,blank=True)
    out_time = models.TimeField()
    reason = models.CharField(max_length=100)
    status = models.IntegerField(default=0)

def billdue_date():
    due_date = datetime.now() + timedelta(days=15)
    return due_date.strftime('%Y-%m-%d')

class Fees(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    room_rent = models.FloatField(default=0)
    mess_bill = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    status = models.IntegerField(default=0)
    paid_by = models.CharField(max_length=100)
    paid_date = models.DateField(null=True)
    payment = models.CharField(max_length=100)

    def __str__(self):
        return self.from_date

    def get_total(self):
        return self.room_rent + self.mess_bill


















