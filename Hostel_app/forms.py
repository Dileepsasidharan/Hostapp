import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import ModelForm, DateInput

from Hostel_app.models import Student, User, Parent, Hostel, Food, Notifications, Warden, Review, Complaint, Bookroom, \
    Attendance, Recap, Leaveapp, In_out, Fees

def phone_validation(value):
    if not re.compile(r'^[6-9]\d{9}$').match(value):
        raise ValidationError('Not Valid Number')


class UserRegister(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model= User
        fields = ('username','password1','password2')


class Studentform(forms.ModelForm):
    Phone_no = forms.CharField(validators=[phone_validation])
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Not Valid Email')])
    class Meta:
        model = Student
        exclude = ('user','approval_status')
    def clean_email(self):
        mail=self.cleaned_data["email"]
        email_qs = Student.objects.filter(email=mail)
        if email_qs.exists():
            raise forms.ValidationError("This email is already linked with another account")
        return mail
    def clean_Phone_no(self):
        phone=self.cleaned_data["Phone_no"]
        phone_qs = Student.objects.filter(Phone_no=phone)
        if phone_qs.exists():
            raise forms.ValidationError("This phone number  is already linked with another account")
        return phone
class Parentform(forms.ModelForm):
    Phone_no = forms.CharField(validators=[phone_validation])
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Not Valid Email')])
    class Meta:
        model = Parent
        exclude = ('user','approval_status')

    def clean_email(self):
        mail=self.cleaned_data["email"]
        email_qs = Parent.objects.filter(email=mail)
        if email_qs.exists():
            raise forms.ValidationError("This email is already linked with another account")
        return mail
    def clean_Phone_no(self):
        phone=self.cleaned_data["Phone_no"]
        phone_qs = Parent.objects.filter(Phone_no=phone)
        if phone_qs.exists():
            raise forms.ValidationError("This phone number  is already linked with another account")
        return phone


class add_hostel(forms.ModelForm):
    Phone_no = forms.CharField(validators=[phone_validation])
    Email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Not Valid Email')])
    class Meta:
        model = Hostel
        fields = '__all__'


class add_food(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'
class dateinput(forms.DateInput):
    input_type="date"

class timeinput(forms.TimeInput):
    input_type = "time"

class notification(forms.ModelForm):
    to=forms.DateField(widget=dateinput)
    time=forms.TimeField(widget=timeinput)


    class Meta:
        model=Notifications
        fields='__all__'

class add_warden(forms.ModelForm):
    Phone_no = forms.CharField(validators=[phone_validation])
    Email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Not Valid Email')])
    class Meta:
        model = Warden
        exclude = ('user',)

class addreview(forms.ModelForm):

    class Meta:
        model = Review
        exclude = ('student',)

class complaintform(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('complaint',)

class recapform(forms.ModelForm):
    class Meta:
        model = Recap
        fields = ('Comments',)


class bookroomform(forms.ModelForm):
    booking_date= forms.DateField(widget=dateinput)
    class Meta:
        model = Bookroom
        fields = ('booking_date',)

        def clean_date_joining(self):
            date = self.cleaned_data['booking_date']

            if date < datetime.date.today():
                raise forms.ValidationError("Invalid Date")
            return date

attendance_choice=(
    ('Present','Present'),
    ('Absent','Absent')
)
class attform(forms.ModelForm):
    status = forms.ChoiceField(choices=attendance_choice,widget=forms.RadioSelect)
    time=forms.TimeField(widget=timeinput)
    class Meta:
        model = Attendance
        fields =( 'student','time','status',)


class leaveappform(forms.ModelForm):
    start_date= forms.DateField(widget=dateinput)
    end_date = forms.DateField(widget=dateinput)
    class Meta:
        model = Leaveapp
        exclude = ('student','status','No_of_days_required',)

class in_outform(forms.ModelForm):
    out_time=forms.TimeField(widget=timeinput)
    class Meta:
        model = In_out
        exclude = ('status',)
        widgets = {
            'in_time': forms.TimeInput(attrs={'type':'time'}),
        }
        in_time = forms.TimeField(required=False)


class AddFee(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.filter(approval_status=True))
    from_date = forms.DateField(widget=dateinput)
    to_date = forms.DateField(widget=dateinput)
    room_rent = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    mess_bill = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Fees
        fields = ('student', 'from_date', 'to_date', 'room_rent', 'mess_bill')

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        if (from_date > datetime.date.today()):
            raise forms.ValidationError("Invalid From Date")
        if to_date <= from_date or to_date > datetime.date.today():
            raise forms.ValidationError("Invalid To Date")

        from_day = from_date.strftime("%d")
        from_m = from_date.strftime("%m")
        to_day = to_date.strftime("%d")
        print(from_m, to_day)

        if int(from_day) != 1:
            raise forms.ValidationError('Invalid From Date')
        if int(from_m) == 2:
            if int(to_day) not in [29, 28]:
                raise forms.ValidationError('Invalid To Date')

        else:

            if int(from_m) in [1, 3, 5, 7, 8, 10, 12]:
                if int(to_day) != 31:
                    raise forms.ValidationError('Invalid To Date')

            elif int(from_m) == [4, 6, 9, 11]:

                if int(to_day) != 30:
                    raise forms.ValidationError('Invalid To Date')

        return cleaned_data













