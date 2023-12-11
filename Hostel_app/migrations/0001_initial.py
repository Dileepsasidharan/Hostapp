# Generated by Django 4.2.3 on 2023-09-21 16:55

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Food",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "day",
                    models.CharField(
                        choices=[
                            ("Sunday", "Sunday"),
                            ("Monday", "Monday"),
                            ("Tuesday", "Tuesday"),
                            ("Wednesday", "Wednesday"),
                            ("Thursday", "Thursday"),
                            ("Friday", "Friday"),
                            ("Saturday", "Saturday"),
                        ],
                        max_length=50,
                    ),
                ),
                ("Breakfast", models.CharField(max_length=100)),
                ("Lunch", models.CharField(max_length=100)),
                ("Dinner", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Hostel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Hostel_name", models.CharField(max_length=50)),
                ("Hostel_address", models.CharField(max_length=100)),
                ("Email", models.EmailField(max_length=254)),
                ("Phone_no", models.CharField(max_length=10)),
                ("Hostel_Images", models.ImageField(upload_to="Hostel_images")),
                ("Total_room", models.CharField(max_length=50)),
                ("Occupied_room", models.CharField(max_length=100)),
                ("Room_rent", models.CharField(max_length=100)),
                ("Room_facilities", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Notifications",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("to", models.CharField(max_length=100)),
                ("notification", models.TextField(max_length=100)),
                ("time", models.TimeField()),
                ("timestamp", models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("is_warden", models.BooleanField(default=False)),
                ("is_student", models.BooleanField(default=False)),
                ("is_parent", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="student",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("address", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("Phone_no", models.CharField(max_length=10)),
                ("photo", models.ImageField(upload_to="profile")),
                ("approval_status", models.BooleanField(default=0)),
                ("course", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Warden",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.CharField(max_length=50)),
                ("Address", models.CharField(max_length=100)),
                ("Email", models.EmailField(max_length=254)),
                ("Phone_no", models.CharField(max_length=10)),
                ("Photo", models.ImageField(upload_to="wardenphoto")),
                ("date_of_joining", models.DateField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="warden",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Recap",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Date", models.DateField(auto_now_add=True)),
                ("Comments", models.CharField(max_length=100)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Complaint",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(auto_now_add=True)),
                ("complaint", models.CharField(max_length=100)),
                ("reply", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Date", models.DateField(auto_now_add=True)),
                ("Comments", models.CharField(max_length=100)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Hostel_app.student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Parent",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="parent",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("address", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("Phone_no", models.CharField(max_length=10)),
                ("photo", models.ImageField(upload_to="profile")),
                ("approval_status", models.BooleanField(default=0)),
                (
                    "Student_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Hostel_app.student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Leaveapp",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_application", models.DateField(auto_now_add=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("reason", models.CharField(max_length=100)),
                ("No_of_days_required", models.CharField(max_length=5)),
                ("status", models.IntegerField(default=0)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Hostel_app.student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="In_out",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(auto_now=True)),
                ("in_time", models.TimeField(blank=True, null=True)),
                ("out_time", models.TimeField()),
                ("reason", models.CharField(max_length=100)),
                ("status", models.IntegerField(default=0)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inOut",
                        to="Hostel_app.student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Fee_payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("from_date", models.DateField()),
                ("to_date", models.DateField()),
                ("due_date", models.DateField()),
                ("room_rent", models.FloatField(default=0)),
                ("mess_fee", models.FloatField(default=0)),
                ("amount", models.FloatField(default=0)),
                ("status", models.IntegerField(default=0)),
                ("paid_by", models.CharField(max_length=100)),
                ("paid_date", models.DateField(null=True)),
                ("payment", models.CharField(max_length=100)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fee_paymt",
                        to="Hostel_app.student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Bookroom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("booking_date", models.DateField()),
                ("status", models.IntegerField(default=0)),
                (
                    "booked_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Hostel_app.student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(auto_now=True)),
                ("time", models.TimeField()),
                ("status", models.CharField(max_length=100)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Hostel_app.student",
                    ),
                ),
            ],
        ),
    ]
