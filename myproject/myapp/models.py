from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class ManagerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now

class Manager(AbstractBaseUser):
    CATEGORY_CHOICES = [
        ('unassigned', 'Unassigned'),
        ('hotel', 'Hotel'),
        ('transport', 'Transport'),
        ('park', 'Park'),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='unassigned')
    otp = models.CharField(max_length=6, null=True, blank=True)  # OTP field
    otp_created_at = models.DateTimeField(null=True, blank=True)  # Timestamp for OTP validity
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = ManagerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name



class GamePark(models.Model):
    park_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    size = models.FloatField()
    visit_amount = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    image_1 = models.ImageField(upload_to='gameparks/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='gameparks/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='gameparks/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='gameparks/', blank=True, null=True)
    image_5 = models.ImageField(upload_to='gameparks/', blank=True, null=True)

    def __str__(self):
        return self.park_name

class SearchDeal(models.Model):
    destination = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    hotel = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Deal for {self.destination} from {self.start_date} to {self.end_date}"

class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class PlaceToVisit(models.Model):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, related_name='places', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    visit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_info = models.CharField(max_length=255)
    place_to_visit = models.ForeignKey(
        PlaceToVisit,
        related_name='hotels',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='hotel_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    place_to_visit = models.ForeignKey(PlaceToVisit, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='booking_images/', blank=True, null=True)
    transport = models.CharField(
        max_length=50,
        choices=[('bus', 'Bus'), ('car', 'Car'), ('bike', 'Bike'), ('walk', 'Walk')],
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    def __str__(self):
        return f"Booking for {self.name or 'Unnamed'} at {self.location.name} - Status: {self.status}"